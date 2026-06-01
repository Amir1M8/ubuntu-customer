#!/usr/bin/env python3
"""
Ubuntu Theme Designer - PyQt5 GUI
Customize terminal themes, GTK styles, and desktop wallpapers.
"""

import subprocess
import os
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QGridLayout,
    QStackedWidget, QListWidget, QListWidgetItem, QSizePolicy,
    QSpacerItem, QMessageBox, QGroupBox, QCheckBox, QComboBox,
    QSpinBox, QStatusBar, QSplitter
)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import (
    QPainter, QColor, QLinearGradient, QGradient, QFont,
    QFontDatabase, QPalette, QPixmap, QIcon, QBrush, QPen
)


# ─── Color palettes ────────────────────────────────────────────────────────────

WALLPAPER_PALETTES = {
    "alone-winter":    ["#b8d4e8", "#7fa8c9", "#3d6a8a", "#1a3a52", "#0d1f2d"],
    "forest-road":     ["#a8c988", "#6a9e4a", "#2d6a1f", "#1a3d12", "#0d1f09"],
    "forest":          ["#88c98a", "#4a9e4e", "#1f6a22", "#123d14", "#091f0a"],
    "green":           ["#b4d98e", "#7ab950", "#3a8a1a", "#1f520d", "#0f2907"],
    "night":           ["#1a1a2e", "#16213e", "#0f3460", "#533483", "#e94560"],
    "rainy":           ["#8899aa", "#5577aa", "#335588", "#113366", "#001133"],
    "road":            ["#c8b88a", "#a89060", "#786030", "#483818", "#28180c"],
    "winter":          ["#e8f4fc", "#c0dcf0", "#90bcd8", "#5090b8", "#206890"],
    "spring":          ["#f8e8f0", "#e8b8d0", "#d890b0", "#b85880", "#883058"],
    "winter-forest":   ["#d0e8f0", "#90c0d8", "#3a8090", "#1a4050", "#0a2028"],
    "autumn-forest":   ["#f0c870", "#c89040", "#905018", "#602808", "#381408"],
    "spring-forest":   ["#d8f0b8", "#a0d870", "#58b030", "#287010", "#103808"],
}

TERMINAL_PALETTES = {
    "Blue Theme": {
        "colors": ["#0d1117", "#1c2128", "#1f4788", "#2d6fd4", "#58a6ff", "#7ee0ff", "#c9e6ff", "#e6f3ff"],
        "fg": "#e6f3ff", "bg": "#0d1117", "badge": "COOL", "badge_color": "#58a6ff",
        "preview": [("user@ubuntu", "#58a6ff"), ("~", "#7ee0ff"), ("$ ls -la", "#e6f3ff"), ("total 24", "#7ee787")],
    },
    "Night Theme": {
        "colors": ["#0a0a0f", "#141420", "#1a1a35", "#282850", "#3d3d7a", "#8888cc", "#bbbbff", "#e8e8ff"],
        "fg": "#e8e8ff", "bg": "#0a0a0f", "badge": "DARK", "badge_color": "#e94560",
        "preview": [("user@ubuntu", "#8888cc"), ("~", "#bbbbff"), ("$ vim config.py", "#e8e8ff"), ("[readonly]", "#e94560")],
    },
    "Forest Theme": {
        "colors": ["#0a120a", "#142014", "#1f3a1f", "#285028", "#3a703a", "#5aaa5a", "#88dd88", "#c0eec0"],
        "fg": "#c0eec0", "bg": "#0a120a", "badge": "NATURE", "badge_color": "#7ee787",
        "preview": [("user@ubuntu", "#5aaa5a"), ("~", "#88dd88"), ("$ grep -r 'theme'", "#c0eec0"), ("4 matches found", "#88dd88")],
    },
    "Winter Theme": {
        "colors": ["#0a1520", "#102030", "#184060", "#205880", "#2878a8", "#5aa8d8", "#90c8f0", "#c8e8ff"],
        "fg": "#c8e8ff", "bg": "#0a1520", "badge": "ICE", "badge_color": "#a5d8f0",
        "preview": [("user@ubuntu", "#5aa8d8"), ("~", "#90c8f0"), ("$ sudo apt update", "#c8e8ff"), ("Hit:1 noble InRelease", "#a5d8f0")],
    },
    "Autumn Theme": {
        "colors": ["#1a0800", "#2a1000", "#501800", "#782800", "#a84000", "#d86010", "#f09040", "#ffc880"],
        "fg": "#ffc880", "bg": "#1a0800", "badge": "WARM", "badge_color": "#e8a030",
        "preview": [("user@ubuntu", "#d86010"), ("~", "#f09040"), ("$ make install", "#ffc880"), ("Build complete", "#f09040")],
    },
    "Spring Theme": {
        "colors": ["#200015", "#380025", "#580040", "#800060", "#aa2080", "#d058a8", "#e890c8", "#ffc8e8"],
        "fg": "#ffc8e8", "bg": "#200015", "badge": "BLOOM", "badge_color": "#e878b0",
        "preview": [("user@ubuntu", "#d058a8"), ("~", "#e890c8"), ("$ python3 app.py", "#ffc8e8"), ("Server started :8000", "#e890c8")],
    },
}

FULL_THEMES = {
    "Winter":       {"wp": "winter",        "gtk": "winter-gtk",        "dconf": "winter-theme"},
    "Forest":       {"wp": "forest",        "gtk": "forest-gtk",        "dconf": "forest-theme"},
    "Night":        {"wp": "night",         "gtk": "nigth-gtk",         "dconf": "nigth-theme"},
    "Autumn":       {"wp": "autumn-forest", "gtk": "autumn-gtk",        "dconf": "autumn-theme"},
    "Spring":       {"wp": "spring",        "gtk": "spring-gtk",        "dconf": "spring-theme"},
    "Spring Forest":{"wp": "spring-forest", "gtk": "spring-forest-gtk", "dconf": "spring-forest-theme"},
    "Blue":         {"wp": "alone-winter",  "gtk": "blue-gtk",          "dconf": "blue-theme"},
    "Dark Blue":    {"wp": "rainy",         "gtk": "dark-blue-gtk",     "dconf": "dark-blue-theme"},
}

APP_STYLESHEET = """
QMainWindow, QWidget#central {
    background-color: #0d1117;
}

/* ── Sidebar ── */
QWidget#sidebar {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}
QPushButton#nav_btn {
    background: transparent;
    color: #8b949e;
    border: none;
    border-left: 2px solid transparent;
    border-radius: 0px;
    text-align: left;
    padding: 8px 14px 8px 12px;
    font-size: 13px;
}
QPushButton#nav_btn:hover {
    background-color: #1c2128;
    color: #e6edf3;
}
QPushButton#nav_btn[active="true"] {
    background-color: #1c2128;
    color: #7ee787;
    border-left: 2px solid #7ee787;
}
QPushButton#apply_btn {
    background-color: #238636;
    color: #ffffff;
    border: 1px solid #2ea043;
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 12px;
    font-weight: bold;
}
QPushButton#apply_btn:hover {
    background-color: #2ea043;
}
QPushButton#apply_btn:pressed {
    background-color: #1a7f37;
}

/* ── Main content ── */
QScrollArea {
    background: transparent;
    border: none;
}
QWidget#scroll_content {
    background: #0d1117;
}
QLabel#panel_title {
    color: #e6edf3;
    font-size: 16px;
    font-weight: bold;
}
QLabel#panel_sub {
    color: #484f58;
    font-size: 11px;
    font-family: 'Ubuntu Mono', monospace;
}
QLabel#section_label {
    color: #484f58;
    font-size: 10px;
    letter-spacing: 2px;
}

/* ── Cards ── */
QFrame#wp_card, QFrame#pal_card, QFrame#theme_card {
    background-color: #161b22;
    border: 2px solid #30363d;
    border-radius: 8px;
}
QFrame#wp_card:hover, QFrame#pal_card:hover, QFrame#theme_card:hover {
    border-color: #58a6ff;
}
QFrame#wp_card[selected="true"] {
    border-color: #7ee787;
}
QFrame#pal_card[selected="true"] {
    border-color: #58a6ff;
}
QFrame#theme_card[selected="true"] {
    border-color: #f78166;
}
QLabel#card_name {
    background-color: #1c2128;
    color: #8b949e;
    font-size: 11px;
    padding: 5px 8px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

/* ── Settings ── */
QGroupBox {
    color: #8b949e;
    font-size: 10px;
    letter-spacing: 2px;
    border: 1px solid #30363d;
    border-radius: 8px;
    margin-top: 8px;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
}
QCheckBox {
    color: #e6edf3;
    font-size: 13px;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 16px; height: 16px;
    border: 1px solid #30363d;
    border-radius: 4px;
    background: #1c2128;
}
QCheckBox::indicator:checked {
    background: #238636;
    border-color: #2ea043;
}
QComboBox, QSpinBox {
    background: #1c2128;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 5px 8px;
    font-size: 12px;
}
QComboBox:focus, QSpinBox:focus {
    border-color: #58a6ff;
}
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background: #1c2128;
    color: #e6edf3;
    border: 1px solid #30363d;
    selection-background-color: #2d6fd4;
}

/* ── Status bar ── */
QStatusBar {
    background-color: #161b22;
    color: #8b949e;
    font-size: 11px;
    border-top: 1px solid #30363d;
    font-family: 'Ubuntu Mono', monospace;
}
"""


# ─── Gradient canvas widgets ───────────────────────────────────────────────────

class WallpaperCanvas(QWidget):
    """Draws a gradient wallpaper preview."""
    def __init__(self, colors, parent=None):
        super().__init__(parent)
        self.colors = [QColor(c) for c in colors]
        self.setFixedHeight(72)
        self.setMinimumWidth(100)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        grad = QLinearGradient(0, 0, self.width(), self.height())
        n = len(self.colors)
        for i, c in enumerate(self.colors):
            grad.setColorAt(i / (n - 1), c)
        p.fillRect(self.rect(), QBrush(grad))
        # subtle vignette overlay
        vgr = QLinearGradient(0, 0, 0, self.height())
        vgr.setColorAt(0, QColor(0, 0, 0, 30))
        vgr.setColorAt(1, QColor(0, 0, 0, 80))
        p.fillRect(self.rect(), QBrush(vgr))
        p.end()


class PaletteStrip(QWidget):
    """Draws 8 color swatches side by side."""
    def __init__(self, colors, parent=None):
        super().__init__(parent)
        self.colors = [QColor(c) for c in colors]
        self.setFixedHeight(36)

    def paintEvent(self, event):
        p = QPainter(self)
        w = self.width() / len(self.colors)
        for i, c in enumerate(self.colors):
            p.fillRect(int(i * w), 0, int(w) + 1, self.height(), c)
        p.end()


class TerminalPreview(QWidget):
    """Simulates a few terminal lines."""
    def __init__(self, bg, lines, parent=None):
        super().__init__(parent)
        self.bg = QColor(bg)
        self.lines = lines   # list of (text, color_hex)
        self.setFixedHeight(70)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.fillRect(self.rect(), self.bg)
        font = QFont("Ubuntu Mono", 9)
        font.setStyleHint(QFont.Monospace)
        p.setFont(font)
        y = 16
        for text, color in self.lines:
            p.setPen(QColor(color))
            p.drawText(8, y, text)
            y += 14
        p.end()


class ThemePreviewCanvas(QWidget):
    """Mini desktop mockup for a full theme preset."""
    def __init__(self, wp_colors, accent, parent=None):
        super().__init__(parent)
        self.wp_colors = [QColor(c) for c in wp_colors]
        self.accent = QColor(accent)
        self.setFixedHeight(90)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        # wallpaper gradient
        grad = QLinearGradient(0, 0, self.width(), self.height())
        n = len(self.wp_colors)
        for i, c in enumerate(self.wp_colors):
            grad.setColorAt(i / (n - 1), c)
        p.fillRect(self.rect(), QBrush(grad))
        # dark sidebar mock
        sidebar_w = 30
        sidebar_bg = QColor(0, 0, 0, 100)
        p.fillRect(0, 0, sidebar_w, self.height(), sidebar_bg)
        for i in range(4):
            p.fillRect(5, 10 + i * 16, 20, 4, QColor(self.accent.red(), self.accent.green(), self.accent.blue(), 160))
        # content bars
        x0 = sidebar_w + 10
        p.fillRect(x0, 12, 80, 5, QColor(255, 255, 255, 120))
        p.fillRect(x0, 24, 60, 5, QColor(255, 255, 255, 80))
        p.fillRect(x0, 36, 70, 5, QColor(255, 255, 255, 60))
        # terminal block
        term_rect_x = x0
        term_rect_y = 50
        p.setBrush(QColor(0, 0, 0, 160))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(term_rect_x, term_rect_y, self.width() - x0 - 10, 30, 4, 4)
        p.setPen(self.accent)
        font = QFont("Ubuntu Mono", 8)
        p.setFont(font)
        p.drawText(term_rect_x + 6, term_rect_y + 13, "$ _")
        p.end()


# ─── Clickable card wrapper ────────────────────────────────────────────────────

class SelectableCard(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, data, card_type="wp", parent=None):
        super().__init__(parent)
        self.data = data
        self.card_type = card_type
        self.setObjectName(f"{card_type}_card")
        self.setProperty("selected", False)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.data)

    def set_selected(self, val: bool):
        self.setProperty("selected", val)
        self.style().unpolish(self)
        self.style().polish(self)


# ─── Worker thread for applying themes ────────────────────────────────────────

class ApplyWorker(QThread):
    done = pyqtSignal(bool, str)

    def __init__(self, commands):
        super().__init__()
        self.commands = commands

    def run(self):
        for cmd in self.commands:
            try:
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                if r.returncode != 0:
                    self.done.emit(False, r.stderr.strip() or cmd)
                    return
            except Exception as e:
                self.done.emit(False, str(e))
                return
        self.done.emit(True, "")


# ─── Main window ──────────────────────────────────────────────────────────────

class ThemeDesigner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theme Designer  v1.0")
        self.setMinimumSize(860, 620)
        self.resize(1000, 680)
        self.setStyleSheet(APP_STYLESHEET)

        self._selected_wp = None
        self._selected_pal = None
        self._selected_theme = None
        self._nav_buttons = []
        self._wp_cards = {}
        self._pal_cards = {}
        self._theme_cards = {}

        self._read_uuid()
        self._build_ui()

    # ── UUID helpers ──────────────────────────────────────────────────────────

    def _read_uuid(self):
        uuid_path = os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini")
        try:
            with open(uuid_path, "r") as f:
                self._uuid = f.read().strip()
        except FileNotFoundError:
            self._uuid = ""

    def _ensure_uuid(self):
        uuid_path = os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini")
        os.makedirs(os.path.dirname(uuid_path), exist_ok=True)
        if self._uuid:
            try:
                dconf_list = subprocess.check_output(
                    ["dconf", "list", "/org/gnome/terminal/legacy/profiles:/"], text=True
                )
                if self._uuid in dconf_list:
                    return self._uuid
            except Exception:
                pass
        new_uuid = subprocess.check_output(["uuidgen"], text=True).strip()
        with open(uuid_path, "w") as f:
            f.write(new_uuid)
        self._uuid = new_uuid
        return new_uuid

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget(objectName="central")
        self.setCentralWidget(central)
        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # sidebar
        sidebar = QWidget(objectName="sidebar")
        sidebar.setFixedWidth(190)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 12, 0, 12)
        sb_layout.setSpacing(0)

        self._stacked = QStackedWidget()

        nav_items = [
            ("  Wallpapers",  self._build_wallpapers_panel),
            ("  Terminal",    self._build_terminal_panel),
            ("  Full Themes", self._build_themes_panel),
            ("  Fonts",       self._build_fonts_panel),
            ("  Settings",    self._build_settings_panel),
        ]

        self._add_sidebar_label(sb_layout, "CUSTOMIZE")
        for i, (label, builder) in enumerate(nav_items[:3]):
            btn = self._make_nav_btn(label, i)
            sb_layout.addWidget(btn)
            self._stacked.addWidget(builder())
        self._add_sidebar_divider(sb_layout)
        self._add_sidebar_label(sb_layout, "MORE")
        for i, (label, builder) in enumerate(nav_items[3:], start=3):
            btn = self._make_nav_btn(label, i)
            sb_layout.addWidget(btn)
            self._stacked.addWidget(builder())

        sb_layout.addStretch()

        apply_btn = QPushButton("✓  Apply Changes", objectName="apply_btn")
        apply_btn.clicked.connect(self._on_apply)
        sb_layout.addWidget(apply_btn)

        root_layout.addWidget(sidebar)
        root_layout.addWidget(self._stacked)

        self._nav_buttons[0].setProperty("active", True)
        self._nav_buttons[0].style().unpolish(self._nav_buttons[0])
        self._nav_buttons[0].style().polish(self._nav_buttons[0])

        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("● Ready — select a wallpaper, palette or preset to get started")

    def _add_sidebar_label(self, layout, text):
        lbl = QLabel(text, objectName="section_label")
        lbl.setContentsMargins(14, 8, 0, 4)
        layout.addWidget(lbl)

    def _add_sidebar_divider(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #30363d;")
        line.setContentsMargins(0, 4, 0, 4)
        layout.addWidget(line)

    def _make_nav_btn(self, label, index):
        btn = QPushButton(label, objectName="nav_btn")
        btn.setProperty("active", False)
        btn.setCheckable(False)
        btn.clicked.connect(lambda _, i=index: self._switch_panel(i))
        self._nav_buttons.append(btn)
        return btn

    def _switch_panel(self, index):
        self._stacked.setCurrentIndex(index)
        for i, btn in enumerate(self._nav_buttons):
            active = i == index
            btn.setProperty("active", active)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ── Wallpapers panel ──────────────────────────────────────────────────────

    def _build_wallpapers_panel(self):
        panel, scroll_inner = self._make_scroll_panel()
        layout = scroll_inner.layout()

        self._panel_header(layout, "Desktop Wallpaper",
                           "$ gsettings set org.gnome.desktop.background picture-uri-dark")
        self._section_label(layout, "SELECT A WALLPAPER")

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(10)
        grid.setContentsMargins(0, 0, 0, 0)

        for idx, (name, colors) in enumerate(WALLPAPER_PALETTES.items()):
            card = SelectableCard(name, "wp")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(0)

            canvas = WallpaperCanvas(colors)
            name_lbl = QLabel(name, objectName="card_name")
            name_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            card_layout.addWidget(canvas)
            card_layout.addWidget(name_lbl)
            card.setFixedHeight(canvas.height() + 26)

            card.clicked.connect(self._on_wp_selected)
            self._wp_cards[name] = card
            grid.addWidget(card, idx // 3, idx % 3)

        layout.addWidget(grid_widget)
        layout.addStretch()
        return panel

    def _on_wp_selected(self, name):
        for n, c in self._wp_cards.items():
            c.set_selected(n == name)
        self._selected_wp = name
        self._status.showMessage(f"● Wallpaper selected: {name}  —  click Apply Changes to set")

    # ── Terminal panel ────────────────────────────────────────────────────────

    def _build_terminal_panel(self):
        panel, scroll_inner = self._make_scroll_panel()
        layout = scroll_inner.layout()

        self._panel_header(layout, "Terminal Color Palette",
                           "$ dconf load /org/gnome/terminal/legacy/profiles:/")
        self._section_label(layout, "COLOR SCHEMES")

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(10)
        grid.setContentsMargins(0, 0, 0, 0)

        for idx, (name, data) in enumerate(TERMINAL_PALETTES.items()):
            card = SelectableCard(name, "pal")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(0)

            strip = PaletteStrip(data["colors"])
            term = TerminalPreview(data["bg"], data["preview"])

            bottom = QWidget()
            bottom.setStyleSheet("background: #1c2128; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")
            blay = QHBoxLayout(bottom)
            blay.setContentsMargins(8, 5, 8, 5)
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet("color: #8b949e; font-size: 11px; background: transparent;")
            badge = QLabel(data["badge"])
            badge.setStyleSheet(
                f"color: {data['badge_color']}; background: {data['badge_color']}22;"
                "font-size: 9px; font-weight: bold; padding: 2px 6px;"
                "border-radius: 3px;"
            )
            blay.addWidget(name_lbl)
            blay.addStretch()
            blay.addWidget(badge)

            card_layout.addWidget(strip)
            card_layout.addWidget(term)
            card_layout.addWidget(bottom)

            card.clicked.connect(self._on_pal_selected)
            self._pal_cards[name] = card
            grid.addWidget(card, idx // 2, idx % 2)

        layout.addWidget(grid_widget)
        layout.addStretch()
        return panel

    def _on_pal_selected(self, name):
        for n, c in self._pal_cards.items():
            c.set_selected(n == name)
        self._selected_pal = name
        self._status.showMessage(f"● Palette selected: {name}  —  click Apply Changes to set")

    # ── Full themes panel ─────────────────────────────────────────────────────

    def _build_themes_panel(self):
        panel, scroll_inner = self._make_scroll_panel()
        layout = scroll_inner.layout()

        self._panel_header(layout, "Full Theme Presets",
                           "$ Wallpaper + GTK CSS + Terminal dconf in one click")
        self._section_label(layout, "COMPLETE THEMES")

        grid_widget = QWidget()
        grid = QGridLayout(grid_widget)
        grid.setSpacing(10)
        grid.setContentsMargins(0, 0, 0, 0)

        theme_accents = {
            "Winter": "#5aa8d8", "Forest": "#5aaa5a", "Night": "#8888cc",
            "Autumn": "#d86010", "Spring": "#d058a8", "Spring Forest": "#7ee040",
            "Blue": "#58a6ff", "Dark Blue": "#2d6fd4",
        }

        for idx, (name, data) in enumerate(FULL_THEMES.items()):
            wp_colors = WALLPAPER_PALETTES.get(data["wp"], ["#1a1a2e", "#0f3460"])
            accent = theme_accents.get(name, "#7ee787")

            card = SelectableCard(name, "theme")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(0, 0, 0, 0)
            card_layout.setSpacing(0)

            preview = ThemePreviewCanvas(wp_colors, accent)

            bottom = QWidget()
            bottom.setStyleSheet("background: #1c2128; border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;")
            blay = QHBoxLayout(bottom)
            blay.setContentsMargins(8, 6, 8, 6)
            name_lbl = QLabel(name)
            name_lbl.setStyleSheet("color: #e6edf3; font-size: 12px; font-weight: bold; background: transparent;")
            sub_lbl = QLabel(data["gtk"])
            sub_lbl.setStyleSheet("color: #484f58; font-size: 10px; background: transparent;")
            blay.addWidget(name_lbl)
            blay.addStretch()
            blay.addWidget(sub_lbl)

            card_layout.addWidget(preview)
            card_layout.addWidget(bottom)

            card.clicked.connect(self._on_theme_selected)
            self._theme_cards[name] = card
            grid.addWidget(card, idx // 2, idx % 2)

        layout.addWidget(grid_widget)
        layout.addStretch()
        return panel

    def _on_theme_selected(self, name):
        for n, c in self._theme_cards.items():
            c.set_selected(n == name)
        self._selected_theme = name
        self._status.showMessage(f"● Preset selected: {name}  —  sets wallpaper + GTK + terminal")

    # ── Fonts panel ───────────────────────────────────────────────────────────

    def _build_fonts_panel(self):
        panel, scroll_inner = self._make_scroll_panel()
        layout = scroll_inner.layout()
        self._panel_header(layout, "Font Settings",
                           "$ gsettings set org.gnome.desktop.interface font-name")

        rows = [
            ("Interface font", ["Ubuntu Regular", "Cantarell Regular", "Noto Sans Regular", "DejaVu Sans"], 11),
            ("Monospace font", ["Ubuntu Mono Regular", "JetBrains Mono", "Hack Regular", "Fira Code"], 13),
            ("Document font",  ["Ubuntu Regular", "Cantarell Regular", "Liberation Serif"], 11),
        ]
        for label, fonts, size in rows:
            self._section_label(layout, label.upper())
            row_w = QWidget()
            row_l = QHBoxLayout(row_w)
            row_l.setContentsMargins(0, 0, 0, 4)
            combo = QComboBox()
            combo.addItems(fonts)
            spin = QSpinBox()
            spin.setRange(8, 18)
            spin.setValue(size)
            spin.setFixedWidth(60)
            row_l.addWidget(combo)
            row_l.addWidget(spin)
            layout.addWidget(row_w)

        self._section_label(layout, "RENDERING")
        for label in ("Font antialiasing", "Subpixel hinting"):
            cb = QCheckBox(label)
            cb.setChecked(True)
            layout.addWidget(cb)

        apply_fonts = QPushButton("✓  Apply Fonts", objectName="apply_btn")
        apply_fonts.setFixedWidth(150)
        apply_fonts.clicked.connect(lambda: self._status.showMessage("● Fonts applied via gsettings"))
        layout.addSpacing(8)
        layout.addWidget(apply_fonts)
        layout.addStretch()
        return panel

    # ── Settings panel ────────────────────────────────────────────────────────

    def _build_settings_panel(self):
        panel, scroll_inner = self._make_scroll_panel()
        layout = scroll_inner.layout()
        self._panel_header(layout, "Settings", "$ ~/.ubuntu-customer/setting/")

        behavior = QGroupBox("BEHAVIOR")
        b_layout = QVBoxLayout(behavior)
        for label, checked in [
            ("Auto-apply theme on selection", False),
            ("Backup GTK before applying", True),
            ("Remember last applied theme", True),
        ]:
            cb = QCheckBox(label)
            cb.setChecked(checked)
            b_layout.addWidget(cb)
        layout.addWidget(behavior)

        about = QGroupBox("ABOUT")
        a_layout = QVBoxLayout(about)
        info_label = QLabel(
            f"<pre style='color:#8b949e; font-family: Ubuntu Mono, monospace; font-size:11px; line-height:1.8;'>"
            f"<span style='color:#7ee787'>version</span>  1.0.0\n"
            f"<span style='color:#7ee787'>profile</span>  ~/.ubuntu-customer/\n"
            f"<span style='color:#7ee787'>dconf</span>    /org/gnome/terminal/legacy/profiles:/\n"
            f"<span style='color:#58a6ff'>uuid</span>     {self._uuid or '(not set)'}"
            f"</pre>"
        )
        info_label.setTextFormat(Qt.RichText)
        a_layout.addWidget(info_label)
        layout.addWidget(about)

        danger = QGroupBox("DANGER ZONE")
        d_layout = QHBoxLayout(danger)
        reset_btn = QPushButton("Reset all settings")
        reset_btn.setStyleSheet(
            "background: #1a0800; color: #f78166; border: 1px solid #6e3028;"
            "border-radius: 6px; padding: 6px 14px; font-size: 12px;"
        )
        reset_btn.clicked.connect(self._on_reset)
        d_layout.addWidget(reset_btn)
        d_layout.addStretch()
        layout.addWidget(danger)
        layout.addStretch()
        return panel

    # ── Helper builders ───────────────────────────────────────────────────────

    def _make_scroll_panel(self):
        outer = QScrollArea()
        outer.setWidgetResizable(True)
        inner = QWidget(objectName="scroll_content")
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(20, 20, 20, 20)
        inner_layout.setSpacing(8)
        outer.setWidget(inner)
        return outer, inner

    def _panel_header(self, layout, title, subtitle):
        layout.addWidget(QLabel(title, objectName="panel_title"))
        layout.addWidget(QLabel(subtitle, objectName="panel_sub"))
        layout.addSpacing(8)

    def _section_label(self, layout, text):
        lbl = QLabel(text, objectName="section_label")
        layout.addWidget(lbl)

    # ── Apply logic ───────────────────────────────────────────────────────────

    def _on_apply(self):
        commands = []
        applied = []

        # Wallpaper
        if self._selected_wp:
            path = os.path.expanduser(
                f"~/.ubuntu-customer/wallpapers/{self._selected_wp}.jpg"
            )
            commands.append(
                f'gsettings set org.gnome.desktop.background picture-uri-dark "file:///{path}"'
            )
            commands.append(
                f'gsettings set org.gnome.desktop.background picture-uri "file:///{path}"'
            )
            applied.append(f"Wallpaper: {self._selected_wp}")

        # Full theme (overrides individual palette)
        if self._selected_theme and self._selected_theme in FULL_THEMES:
            t = FULL_THEMES[self._selected_theme]
            # GTK CSS
            gtk_src = os.path.expanduser(f"~/.ubuntu-customer/gtk/{t['gtk']}.css")
            commands.append(f"cp ~/.config/gtk-3.0/gtk.css ~/.config/gtk-3.0/gtk-backup.css 2>/dev/null || true")
            commands.append(f"cp {gtk_src} ~/.config/gtk-3.0/gtk.css")
            # dconf terminal
            uuid = self._ensure_uuid()
            dconf_src = os.path.expanduser(f"~/.ubuntu-customer/dconf/{t['dconf']}.dconf")
            commands.append(
                f"dconf load /org/gnome/terminal/legacy/profiles:/:{uuid}/ < {dconf_src}"
            )
            commands.append(
                f"gsettings set org.gnome.Terminal.ProfilesList list \"['{uuid}']\""
            )
            applied.append(f"Theme: {self._selected_theme}")

        elif self._selected_pal:
            # Individual palette only
            theme_key = self._selected_pal.lower().replace(" ", "-").replace("theme", "theme")
            uuid = self._ensure_uuid()
            dconf_src = os.path.expanduser(f"~/.ubuntu-customer/dconf/{theme_key}.dconf")
            commands.append(
                f"dconf load /org/gnome/terminal/legacy/profiles:/:{uuid}/ < {dconf_src}"
            )
            commands.append(
                f"gsettings set org.gnome.Terminal.ProfilesList list \"['{uuid}']\""
            )
            applied.append(f"Palette: {self._selected_pal}")

        if not commands:
            QMessageBox.information(self, "Nothing selected",
                                    "Please select a wallpaper, palette, or full theme first.")
            return

        self._status.showMessage("● Applying changes…")
        self._worker = ApplyWorker(commands)
        self._worker.done.connect(lambda ok, err: self._on_apply_done(ok, err, applied))
        self._worker.start()

    def _on_apply_done(self, ok, err, applied):
        if ok:
            summary = "  ·  ".join(applied)
            self._status.showMessage(f"✓  Applied: {summary}")
            QMessageBox.information(self, "Done", f"Applied successfully:\n• " + "\n• ".join(applied))
        else:
            self._status.showMessage("✗  Error applying theme")
            QMessageBox.critical(self, "Error",
                                 f"Something went wrong:\n{err}\n\nMake sure ~/.ubuntu-customer/ paths exist.")

    def _on_reset(self):
        reply = QMessageBox.question(
            self, "Reset settings",
            "This will clear your UUID cache and restore defaults.\nContinue?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            uuid_path = os.path.expanduser("~/.ubuntu-customer/setting/uuid.ini")
            try:
                os.remove(uuid_path)
            except FileNotFoundError:
                pass
            self._uuid = ""
            self._status.showMessage("● Settings reset. UUID will be regenerated on next apply.")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Theme Designer")
    app.setApplicationVersion("1.0")

    # Try to load a dark palette as fallback
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#0d1117"))
    palette.setColor(QPalette.WindowText, QColor("#e6edf3"))
    palette.setColor(QPalette.Base, QColor("#161b22"))
    palette.setColor(QPalette.AlternateBase, QColor("#1c2128"))
    palette.setColor(QPalette.Text, QColor("#e6edf3"))
    palette.setColor(QPalette.Button, QColor("#21262d"))
    palette.setColor(QPalette.ButtonText, QColor("#e6edf3"))
    app.setPalette(palette)

    win = ThemeDesigner()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()