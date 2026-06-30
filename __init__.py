import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.library import QApplication, QFont, QIcon
from ui import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName('ForceApp')
    app.setOrganizationName('ForceApp')

    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base, 'icon.ico')
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)

    font = QFont('Segoe UI', 10)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
