from PySide6.QtCore import QObject, Signal


STRINGS = {

    # Window
    'window_title':          {'es': 'ForceApp - Instalador Forzado de APKs',  'en': 'ForceApp - APK Force Installer'},

    # Toolbar
    'refresh':               {'es': 'Refrescar',                              'en': 'Refresh'},
    'refresh_tt':            {'es': 'Actualizar lista de dispositivos',       'en': 'Refresh device list'},
    'about':                 {'es': 'Acerca de',                              'en': 'About'},

    # Left panel — devices
    'devices':               {'es': 'Dispositivos',                           'en': 'Devices'},
    'update_devices':        {'es': ' Actualizar',                            'en': ' Refresh'},

    # Right panel — install
    'install_apks':          {'es': 'Instalación de APKs',                    'en': 'APK Installation'},
    'apk_file':              {'es': 'Archivo APK:',                           'en': 'APK file:'},
    'select_apk':            {'es': 'Selecciona un archivo .apk...',          'en': 'Select an .apk file...'},
    'browse':                {'es': ' Examinar',                              'en': ' Browse'},
    'apk_folder':            {'es': 'Carpeta de APKs:',                       'en': 'APK folder:'},
    'select_folder':         {'es': 'Selecciona una carpeta con .apk...',     'en': 'Select a folder with .apk...'},
    'apks_selected':         {'es': 'APKs seleccionados:',                    'en': 'APKs selected:'},
    'count_zero':            {'es': '0 archivos',                             'en': '0 files'},
    'options_title':         {'es': 'Opciones de instalación forzada',        'en': 'Force install options'},
    'opt_replace':           {'es': 'Reemplazar app existente (-r)',          'en': 'Replace existing app (-r)'},
    'opt_downgrade':         {'es': 'Permitir downgrade (-d)',                'en': 'Allow downgrade (-d)'},
    'opt_test':              {'es': 'Permitir APK de test (-t)',              'en': 'Allow test APK (-t)'},
    'opt_no_stream':         {'es': 'Deshabilitar streaming',                 'en': 'Disable streaming'},
    'install_btn':           {'es': ' INSTALAR',                              'en': ' INSTALL'},
    'cancel_btn':            {'es': ' Cancelar',                              'en': ' Cancel'},

    # Uninstall
    'uninstall':             {'es': 'Desinstalación',                         'en': 'Uninstall'},
    'package_name':          {'es': 'Package name:',                          'en': 'Package name:'},
    'package_hint':          {'es': 'ej: com.example.app',                    'en': 'e.g. com.example.app'},
    'uninstall_btn':         {'es': ' DESINSTALAR',                           'en': ' UNINSTALL'},
    'pkg_hint':              {'es': 'Selecciona un APK para detectar su package name',
                                                               'en': 'Select an APK to detect its package name'},
    'detect_pkg':            {'es': ' Detectar package del APK seleccionado',  'en': ' Detect package from selected APK'},

    # Console
    'console':               {'es': 'Consola',                                'en': 'Console'},
    'progress_ready':        {'es': '(%v/%m) preparado',                      'en': '(%v/%m) ready'},
    'progress_starting':     {'es': '(%v/%m) iniciando...',                   'en': '(%v/%m) starting...'},
    'progress_installing':   {'es': '(%v/%m) instalando...',                  'en': '(%v/%m) installing...'},
    'clear':                 {'es': ' Limpiar',                               'en': ' Clear'},

    # Status bar
    'devices_count':         {'es': '0 dispositivos',                         'en': '0 devices'},
    'adb_verifying':         {'es': 'ADB: verificando...',                    'en': 'ADB: checking...'},
    'starting':              {'es': 'Iniciando...',                           'en': 'Starting...'},

    # Messages
    'msg_no_files':          {'es': 'Sin archivos',                           'en': 'No files'},
    'msg_no_files_body':     {'es': 'Selecciona un archivo o carpeta con APKs.',
                                                                 'en': 'Select a file or folder with APKs.'},
    'msg_no_device':         {'es': 'Sin dispositivo',                        'en': 'No device'},
    'msg_no_device_body':    {'es': 'Conecta y selecciona un dispositivo Android.',
                                                               'en': 'Connect and select an Android device.'},
    'msg_no_pkg':            {'es': 'Sin paquete',                            'en': 'No package'},
    'msg_no_pkg_body':       {'es': 'Ingresa el nombre del paquete a desinstalar.',
                                                                 'en': 'Enter the package name to uninstall.'},
    'msg_no_apk':            {'es': 'Sin APK',                                'en': 'No APK'},
    'msg_no_apk_body':       {'es': 'Selecciona primero un archivo APK.',     'en': 'Select an APK file first.'},
    'msg_not_detected':      {'es': 'No detectado',                           'en': 'Not detected'},
    'msg_not_detected_body': {'es': 'No se pudo extraer el package name.\nInstala Android SDK Build-Tools o ingresa manualmente.',
                                                               'en': 'Could not extract the package name.\nInstall Android SDK Build-Tools or enter it manually.'},

    # About
    'about_title':           {'es': 'Acerca de ForceApp',                     'en': 'About ForceApp'},
    'about_body':            {'es': '<b>ForceApp v1.0</b><br><br>Instalador forzado de APKs vía ADB.<br><br>Desarrollado con Python + PySide6<br><br>Créditos: <b>zdxniel</b><br>TikTok: @DevBujito',
                                                               'en': '<b>ForceApp v1.0</b><br><br>APK force installer via ADB.<br><br>Developed with Python + PySide6<br><br>Credits: <b>zdxniel</b><br>TikTok: @DevBujito'},

    # Log messages
    'log_updating':          {'es': 'Actualizando dispositivos...',           'en': 'Updating devices...'},
    'log_selected':          {'es': '[OK] Dispositivo seleccionado: {0}',     'en': '[OK] Device selected: {0}'},
    'log_no_device':         {'es': '[!] Ningún dispositivo seleccionado',    'en': '[!] No device selected'},
    'log_detecting':         {'es': 'Detectando package name de: {0}',        'en': 'Detecting package name of: {0}'},
    'log_detected':          {'es': '[OK] Package detectado: {0}',            'en': '[OK] Package detected: {0}'},
    'log_not_detected':      {'es': '[!] No se pudo detectar el package name (necesitas aapt)',
                                                                 'en': '[!] Could not detect package name (need aapt)'},
    'log_cancelling':        {'es': 'Cancelando instalación...',              'en': 'Cancelling installation...'},
    'log_adb_ok':            {'es': '[OK] ADB disponible',                    'en': '[OK] ADB available'},
    'log_adb_not_found':     {'es': '[!] ADB no encontrado',                  'en': '[!] ADB not found'},
    'log_devices_connected': {'es': 'Dispositivos conectados: {0}',           'en': 'Devices connected: {0}'},
    'log_selected_device':   {'es': '[OK] Seleccionado: {0} ({1})',           'en': '[OK] Selected: {0} ({1})'},
    'log_device_not_found':  {'es': '[!] Dispositivo {0} no encontrado',      'en': '[!] Device {0} not found'},
    'log_sel_device_first':  {'es': '[!] Selecciona un dispositivo primero',  'en': '[!] Select a device first'},
    'log_sel_apk_first':     {'es': '[!] Selecciona al menos un APK',         'en': '[!] Select at least one APK'},
    'log_enter_package':     {'es': '[!] Ingresa el nombre del paquete',      'en': '[!] Enter the package name'},
    'log_installing_on':     {'es': 'Iniciando instalación en {0}...',        'en': 'Starting installation on {0}...'},
    'log_cancelled_by_user': {'es': 'Instalación cancelada por el usuario.',  'en': 'Installation cancelled by user.'},
    'log_uninstalling':      {'es': 'Desinstalando {0}...',                   'en': 'Uninstalling {0}...'},
    'log_uninstalled_ok':    {'es': '[OK] Desinstalado correctamente',        'en': '[OK] Uninstalled successfully'},
    'log_installing':        {'es': 'Instalando {0}/{1} - {2}',               'en': 'Installing {0}/{1} - {2}'},
    'log_unknown_error':     {'es': 'Error desconocido',                      'en': 'Unknown error'},
    'log_abort_operation':   {'es': '[FALLO] {0}',                            'en': '[FAIL] {0}'},
    'log_op_completed':      {'es': '[OK] {0}',                               'en': '[OK] {0}'},
}

LANGUAGES = {
    'es': 'Español',
    'en': 'English',
}


class Translator(QObject):
    language_changed = Signal()

    def __init__(self):
        super().__init__()
        self._lang = 'es'

    @property
    def lang(self):
        return self._lang

    @lang.setter
    def lang(self, code: str):
        if code in LANGUAGES and code != self._lang:
            self._lang = code
            self.language_changed.emit()

    def get(self, key: str) -> str:
        return STRINGS.get(key, {}).get(self._lang, key)

    def fmt(self, key: str, *args) -> str:
        s = self.get(key)
        if args:
            return s.format(*args)
        return s


_translator = Translator()


def tr(key: str) -> str:
    return _translator.get(key)


def trf(key: str, *args) -> str:
    return _translator.fmt(key, *args)


def set_language(code: str):
    _translator.lang = code


def get_language() -> str:
    return _translator.lang


def get_translator() -> Translator:
    return _translator
