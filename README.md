# ForceApp

ForceApp is a desktop utility for Android application management via ADB (Android Debug Bridge). It provides a graphical interface for APK installation and package uninstallation on connected Android devices, with support for batch operations, language switching, and real-time device monitoring.

---

## Table of Contents

- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Device Management](#device-management)
  - [APK Installation](#apk-installation)
  - [Package Uninstallation](#package-uninstallation)
  - [Package Name Detection](#package-name-detection)
  - [Console and Logging](#console-and-logging)
  - [Language Switching](#language-switching)
- [Build Process](#build-process)
- [Project Structure](#project-structure)

---

## Architecture

ForceApp follows a layered architecture separating the graphical interface, business logic, and low-level ADB interaction.

**Presentation Layer (ui.py):** The `MainWindow` class defines the entire user interface: layout, styling, event handling, and signal connections. It communicates with the backend exclusively through Qt signals and slots, ensuring thread safety. `DeviceItemWidget` is a custom widget representing a single connected device in the device list.

**Controller Layer (backend/main.py):** The `Backend` class orchestrates all operations. It manages device selection, coordinates installation and uninstallation workflows through background workers (`InstallWorker`, `UninstallWorker`), and relays status updates to the UI via signals. Each worker runs in its own `QThread` to keep the interface responsive.

**Service Layer (backend/adb.py):** The `ADBManager` class handles all direct interaction with the ADB executable. It locates `adb.exe` on the system, monitors connected devices through periodic polling, builds and executes ADB commands, and parses command output. All subprocess calls use the `CREATE_NO_WINDOW` flag to prevent console windows from appearing during execution.

**Support Modules:**
- `backend/library.py` -- Centralized import hub and `DeviceInfo` namedtuple definition.
- `backend/translations.py` -- Internationalization system supporting Spanish and English through a singleton `Translator` object.
- `backend/icons.py` -- Programmatic icon generation from inline SVG strings, eliminating external icon file dependencies (except the application window icon).

---

## Requirements

- Python 3.13 or later
- Android SDK Platform Tools (ADB) installed and accessible in PATH, or installed in any of the standard SDK locations
- PySide6 (for development)
- PyInstaller (for compiling to executable)

---

## Installation

### From Source

```bash
pip install PySide6 pyinstaller
python __init__.py
```

### Compiled Executable

A pre-built `ForceApp.exe` is available in the project root directory. No Python installation is required to run it.

---

## Usage

### Device Management

**Device Discovery:** The application continuously monitors connected Android devices with ADB debugging enabled. The device list updates automatically every two seconds, and changes are reflected in real time on the left panel.

- **Refresh Device List:** Click the "Refrescar" toolbar button or the "Actualizar" button in the Devices panel to force an immediate refresh.
- **Reset ADB Server:** Click the small refresh button (28x28, located next to "Actualizar") to execute `adb kill-server` followed by `adb start-server`. This resolves most ADB connectivity issues.
- **Select a Device:** Click on any device card in the list to select it as the target for installation or uninstallation operations. The status bar updates to reflect the active device.

Each device card displays:
- A green indicator dot for devices with `device` status, or an orange hollow dot for offline devices.
- The device model name or product identifier.
- The device serial number and connection status.

### APK Installation

**File Selection:**

1. Click "Examinar" next to "Archivo APK" to select a single APK file via a file dialog.
2. Click "Examinar" next to "Carpeta de APKs" to select a directory. The application scans the directory recursively for all `.apk` files.

Selecting one method clears the other. The label next to "APKs seleccionados" displays the number of APKs or the filename of a single file.

**Installation Options (checkboxes):**

| Option | ADB Flag | Default | Description |
|---|---|---|---|
| Reemplazar app existente | `-r` | Off | Replaces an already installed application. |
| Permitir downgrade | `-d` | On | Allows installing a version lower than the installed one. |
| Permitir APK de test | `-t` | On | Allows APKs built with the `testOnly` flag. |
| Deshabilitar streaming | `--no-streaming` | Off | Disables streaming push for large APKs. |

**Execution:**

After selecting a target device and at least one APK, click "INSTALAR" to begin. The installation proceeds sequentially through all selected APKs:

- A progress bar appears showing the current APK index.
- The console displays timestamps for each operation: `[index/total] filename.apk` followed by the result (`OK` or `FALLO`).
- If an installation fails, the process stops and reports the error.
- Click "Cancelar" at any time to abort the remaining installations.

### Package Uninstallation

1. Enter the Android package name in the text field (e.g., `com.example.app`).
2. Click "DESINSTALAR" to remove the package from the selected device.

The `-k` flag (keep data and cache directories) is available in the underlying `uninstall()` method but is not exposed in the current user interface.

### Package Name Detection

To identify the package name of an APK without manual inspection:

1. Select an APK file via the "Examinar" button in the Installation panel.
2. Click "Detectar package del APK seleccionado."

The application attempts to extract the package name using `aapt dump badging` (or `aapt2` as a fallback), which must be available through the Android SDK build-tools directory. If successful, the detected package name is automatically entered into the uninstallation text field.

### Console and Logging

The console panel at the bottom of the window displays all operations with timestamps in `[HH:MM:SS]` format. Each ADB command, status change, and operation result is logged here. Click "Limpiar" to clear the console output. The console retains up to 5000 lines.

The status bar provides at-a-glance information:
- Number of connected devices.
- ADB availability status.
- Current operation status.

### Language Switching

The toolbar includes a language selector button displaying the current language name. Click it to open a dropdown menu with available languages:

- Spanish (Español)
- English

Changing the language updates all interface elements, messages, and log templates immediately without requiring an application restart. The language selection persists for the current session only.

---

## Build Process

To compile the application into a standalone executable:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name ForceApp --add-data "icon.ico;." --paths . --collect-all backend __init__.py
```

Flags explained:
- `--onefile` -- produces a single `.exe` file.
- `--windowed` -- suppresses the console window (GUI only).
- `--icon=icon.ico` -- sets the executable icon.
- `--add-data "icon.ico;."` -- bundles the icon file into the executable for runtime access.
- `--paths .` -- includes the current directory in the module search path.
- `--collect-all backend` -- ensures the entire `backend` package is included.

At runtime, the application uses `sys._MEIPASS` (PyInstaller's temporary extraction directory) to locate bundled resources when running as a compiled executable, falling back to the script directory when running from source.

---

## Project Structure

```
ForceApp/
  ForceApp.exe            -- Compiled executable
  icon.ico                -- Application window icon
  __init__.py             -- Entry point (QApplication setup, window launch)
  ui.py                   -- Graphical user interface (MainWindow, DeviceItemWidget)
  backend/
    __init__.py           -- Package marker
    library.py            -- Centralized imports and DeviceInfo type
    main.py               -- Backend controller, InstallWorker, UninstallWorker
    adb.py                -- ADBManager (device monitoring, command execution)
    translations.py       -- Internationalization (Spanish/English)
    icons.py              -- SVG-based icon generation
```

---

## Credits

Developed by zdxniel and @DevBujito.
