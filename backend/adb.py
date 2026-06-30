from .library import *


class ADBManager(QObject):
    devices_changed = Signal(list)
    output_line = Signal(str)
    adb_error = Signal(str)

    def __init__(self):
        super().__init__()
        self.adb_path = self._locate_adb()
        self._monitoring = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._known_devices: List[DeviceInfo] = []

    # ── Localizar ADB ──────────────────────────────────────────────

    def _locate_adb(self) -> str:
        try:
            r = subprocess.run(['adb', 'version'], capture_output=True, text=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
            if r.returncode == 0:
                self.output_line.emit('ADB encontrado en el PATH')
                return 'adb'
        except Exception:
            pass

        candidates = [
            r'C:\Program Files\Android\Android Studio\platform-tools\adb.exe',
            r'C:\Program Files (x86)\Android\Android Studio\platform-tools\adb.exe',
            r'C:\Android\platform-tools\adb.exe',
            r'C:\Android\sdk\platform-tools\adb.exe',
            r'C:\Android\Sdk\platform-tools\adb.exe',
            os.path.expanduser(r'~\AppData\Local\Android\Sdk\platform-tools\adb.exe'),
            os.path.expanduser(r'~\AppData\Local\Android\platform-tools\adb.exe'),
            os.path.expanduser(r'~\.android\platform-tools\adb.exe'),
        ]
        for p in candidates:
            if os.path.exists(p):
                self.output_line.emit(f'ADB encontrado en: {p}')
                return p

        self.adb_error.emit('ADB no encontrado. Instala Android SDK platform-tools.')
        return 'adb'

    def _locate_aapt(self) -> Optional[str]:
        base = os.path.dirname(self.adb_path) if self.adb_path != 'adb' else ''
        if base:
            for root, dirs, files in os.walk(os.path.join(base, '..')):
                for f in files:
                    if f.lower() == 'aapt.exe':
                        return os.path.join(root, f)
        # buscar en build-tools
        sdk = os.path.dirname(os.path.dirname(self.adb_path)) if self.adb_path != 'adb' else ''
        build_tools = os.path.join(sdk, 'build-tools')
        if os.path.isdir(build_tools):
            for ver in sorted(os.listdir(build_tools), reverse=True):
                aapt = os.path.join(build_tools, ver, 'aapt.exe')
                if os.path.exists(aapt):
                    return aapt
        return None

    # ── Dispositivos ───────────────────────────────────────────────

    def get_devices(self) -> List[DeviceInfo]:
        devices: List[DeviceInfo] = []
        try:
            result = subprocess.run(
                [self.adb_path, 'devices', '-l'],
                capture_output=True, text=True, timeout=10,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            lines = result.stdout.strip().split('\n')
            for line in lines[1:]:
                line = line.strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    serial = parts[0]
                    status = parts[1]
                    model = ''
                    product = ''
                    device_name = ''
                    for part in parts[2:]:
                        if part.startswith('model:'):
                            model = part[6:]
                        elif part.startswith('product:'):
                            product = part[8:]
                        elif part.startswith('device:'):
                            device_name = part[7:]
                    devices.append(DeviceInfo(serial, status, model, product, device_name))
        except subprocess.TimeoutExpired:
            self.adb_error.emit('Timeout al ejecutar adb devices')
        except FileNotFoundError:
            self.adb_error.emit('ADB no encontrado en el sistema')
        except Exception as e:
            self.adb_error.emit(f'Error al listar dispositivos: {e}')
        return devices

    # ── Monitor en segundo plano ───────────────────────────────────

    def start_monitoring(self):
        if self._monitoring:
            return
        self._monitoring = True
        # Primer refresh inmediato
        devices = self.get_devices()
        self._known_devices = devices
        self.devices_changed.emit(devices)
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def stop_monitoring(self):
        self._monitoring = False

    def _monitor_loop(self):
        while self._monitoring:
            try:
                devices = self.get_devices()
                if devices != self._known_devices:
                    self._known_devices = devices
                    self.devices_changed.emit(devices)
            except Exception:
                pass
            time.sleep(2)

    # ── Reset ADB ───────────────────────────────────────────────────

    def reset_server(self):
        """Kill and restart the ADB server, then refresh devices."""
        try:
            subprocess.run([self.adb_path, 'kill-server'], capture_output=True, text=True, timeout=5, creationflags=subprocess.CREATE_NO_WINDOW)
            self.output_line.emit('ADB server detenido')
        except Exception as e:
            self.output_line.emit(f'[!] Error al detener ADB: {e}')
        try:
            subprocess.run([self.adb_path, 'start-server'], capture_output=True, text=True, timeout=10, creationflags=subprocess.CREATE_NO_WINDOW)
            self.output_line.emit('ADB server reiniciado')
        except Exception as e:
            self.output_line.emit(f'[!] Error al iniciar ADB: {e}')
        # Forzar actualización inmediata
        devices = self.get_devices()
        self._known_devices = devices
        self.devices_changed.emit(devices)

    # ── Instalación ────────────────────────────────────────────────

    def install_apk(self, serial: str, apk_path: str,
                    replace=True, downgrade=True, test=True,
                    streaming=True) -> Tuple[bool, str]:
        cmd = [self.adb_path, '-s', serial, 'install']
        if replace:
            cmd.append('-r')
        if downgrade:
            cmd.append('-d')
        if test:
            cmd.append('-t')
        if not streaming:
            cmd.append('--no-streaming')
        cmd.append(apk_path)

        self.output_line.emit(f'> {" ".join(cmd)}')
        return self._run_cmd(cmd)

    def install_multiple(self, serial: str, apk_paths: List[str],
                         **options) -> List[Tuple[str, bool, str]]:
        results: List[Tuple[str, bool, str]] = []
        total = len(apk_paths)
        for idx, apk in enumerate(apk_paths):
            self.output_line.emit(f'[{idx+1}/{total}] Instalando: {os.path.basename(apk)}')
            success, msg = self.install_apk(serial, apk, **options)
            results.append((apk, success, msg))
            status = 'OK' if success else 'FALLÓ'
            self.output_line.emit(f'  → {status}: {msg}')
        return results

    # ── Desinstalación ─────────────────────────────────────────────

    def uninstall(self, serial: str, package_name: str,
                  keep_data=False) -> Tuple[bool, str]:
        cmd = [self.adb_path, '-s', serial, 'uninstall']
        if keep_data:
            cmd.append('-k')
        cmd.append(package_name)
        self.output_line.emit(f'> {" ".join(cmd)}')
        return self._run_cmd(cmd)

    # ─── Parsear package name del APK ─────────────────────────────

    def get_package_name(self, apk_path: str) -> Optional[str]:
        aapt = self._locate_aapt()
        if aapt:
            try:
                r = subprocess.run(
                    [aapt, 'dump', 'badging', apk_path],
                    capture_output=True, text=True, timeout=30,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                m = re.search(r"package: name='([^']+)'", r.stdout)
                if m:
                    return m.group(1)
            except Exception:
                pass
        # fallback con aapt2
        base = os.path.dirname(self.adb_path) if self.adb_path != 'adb' else ''
        if base:
            for root, dirs, files in os.walk(os.path.join(base, '..')):
                for f in files:
                    if f.lower() == 'aapt2.exe':
                        try:
                            r = subprocess.run(
                                [os.path.join(root, f), 'dump', 'badging', apk_path],
                                capture_output=True, text=True, timeout=30,
                                creationflags=subprocess.CREATE_NO_WINDOW
                            )
                            m = re.search(r"package: name='([^']+)'", r.stdout)
                            if m:
                                return m.group(1)
                        except Exception:
                            pass
                        return None
        return None

    # ── Comando interno ────────────────────────────────────────────

    def _run_cmd(self, cmd: List[str]) -> Tuple[bool, str]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180, creationflags=subprocess.CREATE_NO_WINDOW)
            out = result.stdout.strip()
            err = result.stderr.strip()
            if result.returncode == 0:
                if out:
                    self.output_line.emit(out)
                return True, out or 'Success'
            else:
                self.output_line.emit(f'ERROR: {err}')
                return False, err or 'Unknown error'
        except subprocess.TimeoutExpired:
            self.output_line.emit('ERROR: Timeout (180s)')
            return False, 'Timeout'
        except Exception as e:
            self.output_line.emit(f'ERROR: {e}')
            return False, str(e)
