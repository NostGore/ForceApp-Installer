from .library import *
from .adb import ADBManager, DeviceInfo
from .translations import tr, trf


class InstallWorker(QObject):
    started = Signal(str)
    progress = Signal(int, int)
    finished = Signal(bool, str)
    log = Signal(str)

    def __init__(self, adb: ADBManager, serial: str, apk_paths: List[str],
                 options: dict, parent=None):
        super().__init__(parent)
        self._adb = adb
        self._serial = serial
        self._apk_paths = apk_paths
        self._options = options
        self._cancelled = False

    def cancel(self):
        self._cancelled = True

    def run(self):
        if not self._apk_paths:
            self.finished.emit(False, 'No hay APKs seleccionados')
            return

        n = len(self._apk_paths)
        mode = 'carpeta' if n > 1 else 'archivo'
        self.started.emit(f'Instalando {n} APK(s) ({mode})')
        self.log.emit(trf('log_installing_on', self._serial))

        for i, apk in enumerate(self._apk_paths):
            if self._cancelled:
                self.log.emit(tr('log_cancelled_by_user'))
                self.finished.emit(False, 'Cancelado')
                return

            self.progress.emit(i + 1, n)
            self.log.emit(f'[{i+1}/{n}] {os.path.basename(apk)}')
            success, msg = self._adb.install_apk(
                self._serial, apk, **self._options
            )
            if not success:
                self.log.emit(trf('log_abort_operation', msg))
            else:
                self.log.emit('  [OK]')

        self.finished.emit(True, f'Instalados {n} APK(s)')


class UninstallWorker(QObject):
    started = Signal(str)
    finished = Signal(bool, str)
    log = Signal(str)

    def __init__(self, adb: ADBManager, serial: str,
                 package_name: str, keep_data=False, parent=None):
        super().__init__(parent)
        self._adb = adb
        self._serial = serial
        self._package = package_name
        self._keep = keep_data

    def run(self):
        msg = trf('log_uninstalling', self._package)
        self.started.emit(msg)
        self.log.emit(msg)
        success, msg = self._adb.uninstall(self._serial, self._package, self._keep)
        if success:
            self.log.emit(tr('log_uninstalled_ok'))
        else:
            self.log.emit(f'[FALLO] Error: {msg}')
        self.finished.emit(success, msg)


class Backend(QObject):
    device_selected = Signal(object)
    device_list_updated = Signal(list)
    operation_started = Signal(str)
    operation_finished = Signal(bool, str)
    progress_updated = Signal(int, int)
    log_line = Signal(str)
    status_message = Signal(str)
    adb_status_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self.adb = ADBManager()
        self.current_device: Optional[DeviceInfo] = None
        self._install_worker: Optional[InstallWorker] = None
        self._uninstall_worker: Optional[UninstallWorker] = None
        self._install_thread: Optional[QThread] = None
        self._uninstall_thread: Optional[QThread] = None

        self.adb.devices_changed.connect(self._on_devices_changed)
        self.adb.output_line.connect(self.log_line.emit)
        self.adb.adb_error.connect(self._on_adb_error)
        self.status_message.emit('Inicializando...')

    # ── Inicialización ─────────────────────────────────────────────

    def start(self):
        if self.adb.adb_path != 'adb' or self._check_adb_in_path():
            self.adb_status_changed.emit(True)
            self.log_line.emit(tr('log_adb_ok'))
        else:
            self.adb_status_changed.emit(False)
            self.log_line.emit(tr('log_adb_not_found'))
        self.adb.start_monitoring()
        self.status_message.emit('Listo')

    def stop(self):
        self.adb.stop_monitoring()

    def _check_adb_in_path(self) -> bool:
        try:
            r = subprocess.run(['adb', 'version'], capture_output=True, text=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
            return r.returncode == 0
        except Exception:
            return False

    # ── Slots internos ─────────────────────────────────────────────

    def _on_devices_changed(self, devices: List[DeviceInfo]):
        self.device_list_updated.emit(devices)
        if self.current_device:
            still = [d for d in devices if d.serial == self.current_device.serial]
            if not still:
                self.current_device = None
                self.device_selected.emit(None)
                self.status_message.emit('Dispositivo desconectado')
        count = len(devices)
        self.log_line.emit(trf('log_devices_connected', count))

    def _on_adb_error(self, msg: str):
        self.log_line.emit(f'[!] {msg}')
        self.adb_status_changed.emit(False)

    def select_device(self, serial: str):
        devices = self.adb.get_devices()
        for d in devices:
            if d.serial == serial:
                self.current_device = d
                self.device_selected.emit(d)
                label = d.model or d.product or d.serial
                self.status_message.emit(f'Dispositivo seleccionado: {label}')
                self.log_line.emit(trf('log_selected_device', label, d.serial))
                return
        self.log_line.emit(trf('log_device_not_found', serial))

    def refresh_devices(self):
        devices = self.adb.get_devices()
        self.device_list_updated.emit(devices)

    def reset_adb(self):
        self.log_line.emit('[i] Reiniciando servidor ADB...')
        self.adb.reset_server()

    # ── Instalación ────────────────────────────────────────────────

    def install_apks(self, apk_paths: List[str], **options):
        if not self.current_device:
            self.log_line.emit(tr('log_sel_device_first'))
            return
        if not apk_paths:
            self.log_line.emit(tr('log_sel_apk_first'))
            return

        self._install_thread = QThread()
        self._install_worker = InstallWorker(
            self.adb, self.current_device.serial, apk_paths, options
        )
        self._install_worker.moveToThread(self._install_thread)

        self._install_thread.started.connect(self._install_worker.run)
        self._install_worker.finished.connect(self._install_thread.quit)
        self._install_worker.finished.connect(self._install_worker.deleteLater)
        self._install_thread.finished.connect(self._install_thread.deleteLater)
        self._install_worker.started.connect(self.operation_started.emit)
        self._install_worker.finished.connect(self._on_install_finished)
        self._install_worker.log.connect(self.log_line.emit)
        self._install_worker.progress.connect(self._on_install_progress)

        self._install_thread.start()

    def cancel_install(self):
        if self._install_worker:
            self._install_worker.cancel()

    def _on_install_progress(self, current: int, total: int):
        self.progress_updated.emit(current, total)
        self.status_message.emit(f'Instalando {current}/{total}')

    def _on_install_finished(self, success: bool, msg: str):
        self.operation_finished.emit(success, msg)
        if success:
            self.status_message.emit('Instalación completada')
        else:
            self.status_message.emit(f'Error: {msg}')

    # ── Desinstalación ─────────────────────────────────────────────

    def uninstall_package(self, package_name: str, keep_data=False):
        if not self.current_device:
            self.log_line.emit(tr('log_sel_device_first'))
            return
        if not package_name.strip():
            self.log_line.emit(tr('log_enter_package'))
            return

        self._uninstall_thread = QThread()
        self._uninstall_worker = UninstallWorker(
            self.adb, self.current_device.serial, package_name.strip(), keep_data
        )
        self._uninstall_worker.moveToThread(self._uninstall_thread)

        self._uninstall_thread.started.connect(self._uninstall_worker.run)
        self._uninstall_worker.finished.connect(self._uninstall_thread.quit)
        self._uninstall_worker.finished.connect(self._uninstall_worker.deleteLater)
        self._uninstall_thread.finished.connect(self._uninstall_thread.deleteLater)
        self._uninstall_worker.started.connect(self.operation_started.emit)
        self._uninstall_worker.finished.connect(self._on_uninstall_finished)
        self._uninstall_worker.log.connect(self.log_line.emit)

        self._uninstall_thread.start()

    def _on_uninstall_finished(self, success: bool, msg: str):
        self.operation_finished.emit(success, msg)
        if success:
            self.status_message.emit('Desinstalación completada')
        else:
            self.status_message.emit(f'Error: {msg}')

    # ── Utilidad ───────────────────────────────────────────────────

    def get_package_name(self, apk_path: str) -> Optional[str]:
        return self.adb.get_package_name(apk_path)

    def get_apk_files(self, paths: List[str]) -> List[str]:
        apks: List[str] = []
        for p in paths:
            p = os.path.normpath(p)
            if os.path.isfile(p) and p.lower().endswith('.apk'):
                apks.append(p)
            elif os.path.isdir(p):
                for f in sorted(os.listdir(p)):
                    if f.lower().endswith('.apk'):
                        apks.append(os.path.join(p, f))
        return apks
