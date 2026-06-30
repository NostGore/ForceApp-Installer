import os
import sys
import re
import time
import json
import queue
import subprocess
import threading
import traceback
from pathlib import Path
from collections import namedtuple
from datetime import datetime
from typing import Optional, List, Tuple, Callable

import PySide6
from PySide6.QtCore import (
    Qt, QThread, QObject, Signal, Slot, QTimer, QSize,
    QCoreApplication, QMetaObject, Q_ARG
)
from PySide6.QtGui import (
    QFont, QIcon, QPixmap, QColor, QPalette, QAction, QTextCursor,
    QFontDatabase, QCloseEvent, QBrush, QStandardItem, QStandardItemModel
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QTextEdit,
    QPlainTextEdit, QGroupBox, QCheckBox, QLineEdit, QFileDialog,
    QMessageBox, QStatusBar, QFrame, QSplitter, QComboBox,
    QProgressBar, QMenuBar, QMenu, QToolBar, QSizePolicy,
    QSpacerItem, QGridLayout, QFormLayout, QDialog, QDialogButtonBox,
    QStyle, QToolButton, QButtonGroup, QTabWidget, QTabBar
)

DeviceInfo = namedtuple('DeviceInfo', ['serial', 'status', 'model', 'product', 'device_name'])
