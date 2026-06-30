from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import QByteArray, QSize, Qt


def _icon(svg, size=20, color='#555555'):
    svg = svg.replace('{SIZE}', str(size)).replace('{COLOR}', color)
    data = QByteArray(svg.encode('utf-8'))
    pm = QPixmap()
    if pm.loadFromData(data):
        return QIcon(pm)
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    return QIcon(pm)


def _draw_dot(color, size=12):
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(color))
    p.drawEllipse(1, 1, size - 2, size - 2)
    p.end()
    return QIcon(pm)


_REFRESH = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="23 4 23 10 17 10"/>
  <polyline points="1 20 1 14 7 14"/>
  <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
</svg>'''

_FOLDER = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
</svg>'''

_DOWNLOAD = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="7 10 12 15 17 10"/>
  <line x1="12" y1="15" x2="12" y2="3"/>
</svg>'''

_TRASH = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="3 6 5 6 21 6"/>
  <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
</svg>'''

_SEARCH = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="11" cy="11" r="8"/>
  <line x1="21" y1="21" x2="16.65" y2="16.65"/>
</svg>'''

_PHONE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="5" y="2" width="14" height="20" rx="2" ry="2"/>
  <line x1="12" y1="18" x2="12.01" y2="18"/>
</svg>'''

_GEAR = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="3"/>
  <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>
</svg>'''

_LIGHTBULB = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M9 18h6"/>
  <path d="M10 21h4"/>
  <path d="M12 2a7 7 0 0 0-4 12.6V16a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1v-1.4A7 7 0 0 0 12 2z"/>
</svg>'''

_CHECK = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
  <polyline points="22 4 12 14.01 9 11.01"/>
</svg>'''

_CROSS = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"/>
  <line x1="15" y1="9" x2="9" y2="15"/>
  <line x1="9" y1="9" x2="15" y2="15"/>
</svg>'''

_PLAY = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="{COLOR}" stroke="none">
  <polygon points="5 3 19 12 5 21 5 3"/>
</svg>'''

_STOP = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <rect x="6" y="6" width="12" height="12" rx="2"/>
</svg>'''

_WARNING = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
  <line x1="12" y1="9" x2="12" y2="13"/>
  <line x1="12" y1="17" x2="12.01" y2="17"/>
</svg>'''

_CLOSE = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <line x1="18" y1="6" x2="6" y2="18"/>
  <line x1="6" y1="6" x2="18" y2="18"/>
</svg>'''

_DROPDOWN = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="{SIZE}" height="{SIZE}" fill="none" stroke="{COLOR}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="6 9 12 15 18 9"/>
</svg>'''




def refresh(size=20, color='#555555'):
    return _icon(_REFRESH, size, color)


def folder(size=20, color='#555555'):
    return _icon(_FOLDER, size, color)


def download(size=20, color='#555555'):
    return _icon(_DOWNLOAD, size, color)


def trash(size=20, color='#555555'):
    return _icon(_TRASH, size, color)


def search(size=20, color='#555555'):
    return _icon(_SEARCH, size, color)


def phone(size=20, color='#555555'):
    return _icon(_PHONE, size, color)


def gear(size=20, color='#555555'):
    return _icon(_GEAR, size, color)


def lightbulb(size=20, color='#555555'):
    return _icon(_LIGHTBULB, size, color)


def check(size=20, color='#555555'):
    return _icon(_CHECK, size, color)


def cross(size=20, color='#555555'):
    return _icon(_CROSS, size, color)


def play(size=20, color='#555555'):
    return _icon(_PLAY, size, color)


def stop(size=20, color='#555555'):
    return _icon(_STOP, size, color)


def warning(size=20, color='#555555'):
    return _icon(_WARNING, size, color)


def close(size=20, color='#555555'):
    return _icon(_CLOSE, size, color)


def dropdown(size=20, color='#555555'):
    return _icon(_DROPDOWN, size, color)


def dot_online(size=12):
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(Qt.NoPen)
    p.setBrush(QColor('#2E7D32'))
    p.drawEllipse(1, 1, size - 2, size - 2)
    p.end()
    return QIcon(pm)


def dot_offline(size=12):
    pm = QPixmap(size, size)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QColor('#F57F17'))
    p.setBrush(Qt.NoBrush)
    p.drawEllipse(1, 1, size - 2, size - 2)
    p.end()
    return QIcon(pm)
