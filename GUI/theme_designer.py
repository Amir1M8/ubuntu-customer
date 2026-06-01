#!/usr/bin/env python3
"""
Ubuntu Theme Designer  v2.0  —  PyQt5
• Wallpapers loaded from ~/.ubuntu-customer/wallpapers/ (real previews)
• Add-wallpaper dialog (copy any image into the wallpapers folder)
• Custom theme builder  (terminal colors + GTK accent + cursor)
• Full-theme presets, individual terminal palettes, font settings
"""

import os
import sys
import shutil
import subprocess
import configparser
import json

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QGridLayout,
    QStackedWidget, QSizePolicy, QSpacerItem, QMessageBox,
    QGroupBox, QCheckBox, QComboBox, QSpinBox, QStatusBar,
    QFileDialog, QDialog, QLineEdit, QColorDialog, QSlider,
    QTabWidget, QFormLayout, QToolButton, QInputDialog,
)
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import (
    QPainter, QColor, QLinearGradient, QFont, QPalette,
    QPixmap, QIcon, QBrush, QPen, QImage,
)

# ─── Paths ────────────────────────────────────────────────────────────────────
WP_DIR      = os.path.expanduser("~/.ubuntu-customer/wallpapers")
DCONF_DIR   = os.path.expanduser("~/.ubuntu-customer/dconf")
GTK_DIR     = os.path.expanduser("~/.ubuntu-customer/gtk")
SETTING_DIR = os.path.expanduser("~/.ubuntu-customer/setting")
CUSTOM_DIR  = os.path.expanduser("~/.ubuntu-customer/custom")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tiff", ".gif"}

# ─── Built-in terminal palettes ───────────────────────────────────────────────
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
    "Dark-Blue-Theme":    {"colors": ["#0d1117","#1c2128","#1f4788","#2d6fd4","#58a6ff","#7ee0ff","#c9e6ff","#e6f3ff"], "fg":"#e6f3ff","bg":"#0d1117","badge":"COOL","bc":"#58a6ff","preview":[("user@ubuntu","#58a6ff"),("~","#7ee0ff"),("$ ls -la","#e6f3ff"),("total 24","#7ee787")]},
    "Nigth-Theme":   {"colors": ["#0a0a0f","#141420","#1a1a35","#282850","#3d3d7a","#8888cc","#bbbbff","#e8e8ff"], "fg":"#e8e8ff","bg":"#0a0a0f","badge":"DARK","bc":"#e94560","preview":[("user@ubuntu","#8888cc"),("~","#bbbbff"),("$ vim cfg.py","#e8e8ff"),("[readonly]","#e94560")]},
    "Forest-Theme":  {"colors": ["#0a120a","#142014","#1f3a1f","#285028","#3a703a","#5aaa5a","#88dd88","#c0eec0"], "fg":"#c0eec0","bg":"#0a120a","badge":"NATURE","bc":"#7ee787","preview":[("user@ubuntu","#5aaa5a"),("~","#88dd88"),("$ grep -r .","#c0eec0"),("4 matches","#88dd88")]},
    "Winter-Theme":  {"colors": ["#0a1520","#102030","#184060","#205880","#2878a8","#5aa8d8","#90c8f0","#c8e8ff"], "fg":"#c8e8ff","bg":"#0a1520","badge":"ICE","bc":"#a5d8f0","preview":[("user@ubuntu","#5aa8d8"),("~","#90c8f0"),("$ apt update","#c8e8ff"),("Hit:1 noble","#a5d8f0")]},
    "Autumn-Theme":  {"colors": ["#1a0800","#2a1000","#501800","#782800","#a84000","#d86010","#f09040","#ffc880"], "fg":"#ffc880","bg":"#1a0800","badge":"WARM","bc":"#e8a030","preview":[("user@ubuntu","#d86010"),("~","#f09040"),("$ make","#ffc880"),("Build OK","#f09040")]},
    "Spring-Forest-Theme":  {"colors": ["#200015","#380025","#580040","#800060","#aa2080","#d058a8","#e890c8","#ffc8e8"], "fg":"#ffc8e8","bg":"#200015","badge":"BLOOM","bc":"#e878b0","preview":[("user@ubuntu","#d058a8"),("~","#e890c8"),("$ python3","#ffc8e8"),("Running...","#e890c8")]},
}

FULL_THEMES = {
    "Winter":       {"wp": "winter-theme",        "gtk": "winter-gtk",        "dconf": "winter-theme"},
    "Forest":       {"wp": "forest-theme",        "gtk": "forest-gtk",        "dconf": "forest-theme"},
    "Night":        {"wp": "nigth-theme",         "gtk": "nigth-gtk",         "dconf": "nigth-theme"},
    "Autumn":       {"wp": "autumn-forest", "gtk": "autumn-gtk",        "dconf": "autumn-theme"},
    "Spring":       {"wp": "spring",        "gtk": "spring-gtk",        "dconf": "spring-theme"},
    "Spring Forest":{"wp": "spring-forest", "gtk": "spring-forest-gtk", "dconf": "spring-forest-theme"},
    "Blue":         {"wp": "alone-winter",  "gtk": "blue-gtk",          "dconf": "blue-theme"},
    "Dark Blue":    {"wp": "rainy",         "gtk": "dark-blue-gtk",     "dconf": "dark-blue-theme"},
}

# ─── Stylesheet ───────────────────────────────────────────────────────────────
APP_STYLESHEET = """
QMainWindow, QWidget#central { background-color: #0d1117; }

QWidget#sidebar { background-color: #161b22; border-right: 1px solid #30363d; }

QPushButton#nav_btn {
    background: transparent; color: #8b949e;
    border: none; border-left: 2px solid transparent;
    border-radius: 0; text-align: left;
    padding: 8px 14px 8px 12px; font-size: 13px;
}
QPushButton#nav_btn:hover { background-color: #1c2128; color: #e6edf3; }
QPushButton#nav_btn[active="true"] {
    background-color: #1c2128; color: #7ee787;
    border-left: 2px solid #7ee787;
}

QPushButton#apply_btn {
    background-color: #238636; color: #fff;
    border: 1px solid #2ea043; border-radius: 6px;
    padding: 8px 12px; font-size: 12px; font-weight: bold;
}
QPushButton#apply_btn:hover { background-color: #2ea043; }
QPushButton#apply_btn:pressed { background-color: #1a7f37; }

QPushButton#secondary_btn {
    background-color: #21262d; color: #c9d1d9;
    border: 1px solid #30363d; border-radius: 6px;
    padding: 6px 12px; font-size: 12px;
}
QPushButton#secondary_btn:hover { background-color: #30363d; }

QScrollArea { background: transparent; border: none; }
QWidget#scroll_content { background: #0d1117; }

QLabel#panel_title { color: #e6edf3; font-size: 16px; font-weight: bold; }
QLabel#panel_sub   { color: #484f58; font-size: 11px; font-family: 'Ubuntu Mono', monospace; }
QLabel#section_label { color: #484f58; font-size: 10px; letter-spacing: 2px; }

QFrame#wp_card, QFrame#pal_card, QFrame#theme_card, QFrame#custom_card {
    background-color: #161b22; border: 2px solid #30363d; border-radius: 8px;
}
QFrame#wp_card:hover, QFrame#pal_card:hover,
QFrame#theme_card:hover, QFrame#custom_card:hover { border-color: #58a6ff; }
QFrame#wp_card[selected="true"]     { border-color: #7ee787; }
QFrame#pal_card[selected="true"]    { border-color: #58a6ff; }
QFrame#theme_card[selected="true"]  { border-color: #f78166; }
QFrame#custom_card[selected="true"] { border-color: #d29922; }

QLabel#card_name {
    background-color: #1c2128; color: #8b949e;
    font-size: 11px; padding: 5px 8px;
    border-bottom-left-radius: 6px; border-bottom-right-radius: 6px;
}

QGroupBox {
    color: #8b949e; font-size: 10px; letter-spacing: 2px;
    border: 1px solid #30363d; border-radius: 8px;
    margin-top: 8px; padding-top: 10px;
}
QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 4px; }

QCheckBox { color: #e6edf3; font-size: 13px; spacing: 8px; }
QCheckBox::indicator {
    width: 16px; height: 16px;
    border: 1px solid #30363d; border-radius: 4px; background: #1c2128;
}
QCheckBox::indicator:checked { background: #238636; border-color: #2ea043; }

QLineEdit, QComboBox, QSpinBox {
    background: #1c2128; color: #e6edf3;
    border: 1px solid #30363d; border-radius: 6px;
    padding: 5px 8px; font-size: 12px;
}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus { border-color: #58a6ff; }
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background: #1c2128; color: #e6edf3;
    border: 1px solid #30363d; selection-background-color: #2d6fd4;
}

QSlider::groove:horizontal {
    height: 4px; background: #30363d; border-radius: 2px;
}
QSlider::handle:horizontal {
    width: 14px; height: 14px; margin: -5px 0;
    background: #58a6ff; border-radius: 7px;
}
QSlider::sub-page:horizontal { background: #58a6ff; border-radius: 2px; }

QTabWidget::pane { border: 1px solid #30363d; border-radius: 6px; background: #161b22; }
QTabBar::tab {
    background: #1c2128; color: #8b949e;
    padding: 7px 16px; border-bottom: 2px solid transparent;
    font-size: 12px;
}
QTabBar::tab:selected { color: #7ee787; border-bottom-color: #7ee787; }
QTabBar::tab:hover { color: #e6edf3; }

QStatusBar {
    background-color: #161b22; color: #8b949e;
    font-size: 11px; border-top: 1px solid #30363d;
    font-family: 'Ubuntu Mono', monospace;
}

QToolButton#color_btn {
    border: 1px solid #30363d; border-radius: 4px;
    min-width: 28px; min-height: 22px;
}
QToolButton#color_btn:hover { border-color: #58a6ff; }
"""

# ─── Helpers ──────────────────────────────────────────────────────────────────

def ensure_dirs():
    for d in (WP_DIR, DCONF_DIR, GTK_DIR, SETTING_DIR, CUSTOM_DIR):
        os.makedirs(d, exist_ok=True)


def list_wallpapers():
    """Return sorted list of image filenames in WP_DIR."""
    try:
        files = [
            f for f in os.listdir(WP_DIR)
            if os.path.splitext(f.lower())[1] in IMAGE_EXTS
        ]
        return sorted(files)
    except FileNotFoundError:
        return []


def load_custom_themes():
    path = os.path.join(CUSTOM_DIR, "custom_themes.json")
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def save_custom_themes(data: dict):
    path = os.path.join(CUSTOM_DIR, "custom_themes.json")
    os.makedirs(CUSTOM_DIR, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ─── Worker thread ────────────────────────────────────────────────────────────

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
                    self.done.emit(False, (r.stderr or r.stdout or cmd).strip())
                    return
            except Exception as e:
                self.done.emit(False, str(e))
                return
        self.done.emit(True, "")


# ─── Small reusable widgets ───────────────────────────────────────────────────

class SelectableCard(QFrame):
    clicked = pyqtSignal(object)

    def __init__(self, data, card_type="wp", parent=None):
        super().__init__(parent)
        self.data = data
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


class PaletteStrip(QWidget):
    def __init__(self, colors, parent=None):
        super().__init__(parent)
        self._colors = [QColor(c) for c in colors]
        self.setFixedHeight(36)

    def paintEvent(self, event):
        p = QPainter(self)
        w = self.width() / len(self._colors)
        for i, c in enumerate(self._colors):
            p.fillRect(int(i * w), 0, int(w) + 1, self.height(), c)
        p.end()


class TerminalPreview(QWidget):
    def __init__(self, bg, lines, parent=None):
        super().__init__(parent)
        self._bg = QColor(bg)
        self._lines = lines
        self.setFixedHeight(70)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.TextAntialiasing)
        p.fillRect(self.rect(), self._bg)
        font = QFont("Ubuntu Mono", 9)
        font.setStyleHint(QFont.Monospace)
        p.setFont(font)
        y = 16
        for text, color in self._lines:
            p.setPen(QColor(color))
            p.drawText(8, y, text)
            y += 14
        p.end()


class ColorButton(QToolButton):
    """Square button that shows a color and opens a picker on click."""
    colorChanged = pyqtSignal(str)

    def __init__(self, color="#ffffff", parent=None):
        super().__init__(parent)
        self.setObjectName("color_btn")
        self.setFixedSize(28, 22)
        self._color = QColor(color)
        self._refresh()
        self.clicked.connect(self._pick)

    def _refresh(self):
        px = QPixmap(self.size())
        px.fill(self._color)
        self.setIcon(QIcon(px))
        self.setIconSize(self.size())

    def _pick(self):
        c = QColorDialog.getColor(self._color, self, "Pick color")
        if c.isValid():
            self._color = c
            self._refresh()
            self.colorChanged.emit(c.name())

    def color(self) -> str:
        return self._color.name()

    def set_color(self, hex_str: str):
        self._color = QColor(hex_str)
        self._refresh()


# ─── Add-wallpaper dialog ─────────────────────────────────────────────────────

class AddWallpaperDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Wallpaper")
        self.setMinimumWidth(460)
        self.setStyleSheet(APP_STYLESHEET)
        self._src = ""

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        layout.addWidget(QLabel("Source image file:", styleSheet="color:#8b949e;font-size:12px;"))

        row = QHBoxLayout()
        self._path_edit = QLineEdit()
        self._path_edit.setPlaceholderText("Click Browse or paste a path…")
        browse = QPushButton("Browse", objectName="secondary_btn")
        browse.clicked.connect(self._browse)
        row.addWidget(self._path_edit)
        row.addWidget(browse)
        layout.addLayout(row)

        # preview
        self._preview_lbl = QLabel(alignment=Qt.AlignCenter)
        self._preview_lbl.setFixedHeight(140)
        self._preview_lbl.setStyleSheet("background:#161b22;border:1px solid #30363d;border-radius:6px;color:#484f58;font-size:11px;")
        self._preview_lbl.setText("No image selected")
        layout.addWidget(self._preview_lbl)

        layout.addWidget(QLabel("Save as (name inside wallpapers folder):", styleSheet="color:#8b949e;font-size:12px;"))
        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("my-wallpaper  (extension kept automatically)")
        layout.addWidget(self._name_edit)

        btns = QHBoxLayout()
        ok = QPushButton("Add Wallpaper", objectName="apply_btn")
        ok.clicked.connect(self._accept)
        cancel = QPushButton("Cancel", objectName="secondary_btn")
        cancel.clicked.connect(self.reject)
        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(ok)
        layout.addLayout(btns)

    def _browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select image", os.path.expanduser("~"),
            "Images (*.jpg *.jpeg *.png *.bmp *.webp *.tiff *.gif)"
        )
        if path:
            self._path_edit.setText(path)
            self._src = path
            # auto-fill name
            base = os.path.splitext(os.path.basename(path))[0]
            self._name_edit.setText(base)
            # preview
            px = QPixmap(path)
            if not px.isNull():
                self._preview_lbl.setPixmap(
                    px.scaled(440, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )

    def _accept(self):
        src = self._path_edit.text().strip()
        name = self._name_edit.text().strip()
        if not src or not os.path.isfile(src):
            QMessageBox.warning(self, "Error", "Please select a valid image file.")
            return
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a name for the wallpaper.")
            return
        ext = os.path.splitext(src)[1].lower() or ".jpg"
        dest = os.path.join(WP_DIR, name + ext)
        try:
            os.makedirs(WP_DIR, exist_ok=True)
            shutil.copy2(src, dest)
        except Exception as e:
            QMessageBox.critical(self, "Copy failed", str(e))
            return
        self._dest = dest
        self.accept()

    def dest_path(self):
        return getattr(self, "_dest", "")


# ─── Custom theme builder dialog ──────────────────────────────────────────────

class CustomThemeDialog(QDialog):
    """Build or edit a custom terminal+desktop theme."""

    def __init__(self, name="", data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Custom Theme Builder")
        self.setMinimumSize(560, 580)
        self.setStyleSheet(APP_STYLESHEET)
        self._result_data = {}
        data = data or {}

        root = QVBoxLayout(self)
        root.setSpacing(10)

        # Name
        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("Theme name:", styleSheet="color:#8b949e;font-size:12px;"))
        self._name_edit = QLineEdit(name)
        self._name_edit.setPlaceholderText("my-custom-theme")
        name_row.addWidget(self._name_edit)
        root.addLayout(name_row)

        tabs = QTabWidget()
        root.addWidget(tabs)

        # ── Terminal tab ──────────────────────────────────────────────────────
        term_widget = QWidget()
        term_layout = QVBoxLayout(term_widget)
        term_layout.setSpacing(10)

        # BG / FG
        basic = QGroupBox("BACKGROUND & FOREGROUND")
        b_form = QFormLayout(basic)
        b_form.setSpacing(8)
        self._bg_btn  = ColorButton(data.get("bg",  "#0d1117"))
        self._fg_btn  = ColorButton(data.get("fg",  "#e6edf3"))
        self._cur_btn = ColorButton(data.get("cursor", "#7ee787"))
        b_form.addRow(QLabel("Background:", styleSheet="color:#8b949e;font-size:12px;"), self._bg_btn)
        b_form.addRow(QLabel("Foreground:", styleSheet="color:#8b949e;font-size:12px;"), self._fg_btn)
        b_form.addRow(QLabel("Cursor:", styleSheet="color:#8b949e;font-size:12px;"), self._cur_btn)
        term_layout.addWidget(basic)

        # 16-color ANSI palette
        ansi_group = QGroupBox("16-COLOR ANSI PALETTE")
        ansi_outer = QVBoxLayout(ansi_group)
        ansi_grid = QGridLayout()
        ansi_grid.setSpacing(6)
        default_ansi = [
            "#000000","#cc0000","#4e9a06","#c4a000",
            "#3465a4","#75507b","#06989a","#d3d7cf",
            "#555753","#ef2929","#8ae234","#fce94f",
            "#729fcf","#ad7fa8","#34e2e2","#eeeeec",
        ]
        saved_ansi = data.get("ansi", default_ansi)
        self._ansi_btns = []
        ansi_labels = [
            "Black","Red","Green","Yellow","Blue","Magenta","Cyan","White",
            "Br.Black","Br.Red","Br.Green","Br.Yellow","Br.Blue","Br.Magenta","Br.Cyan","Br.White",
        ]
        for i in range(16):
            col = i % 8
            row = i // 8
            vbox = QVBoxLayout()
            vbox.setSpacing(2)
            btn = ColorButton(saved_ansi[i] if i < len(saved_ansi) else default_ansi[i])
            lbl = QLabel(ansi_labels[i], alignment=Qt.AlignCenter)
            lbl.setStyleSheet("color:#484f58;font-size:9px;")
            vbox.addWidget(btn, alignment=Qt.AlignCenter)
            vbox.addWidget(lbl)
            wrapper = QWidget()
            wrapper.setLayout(vbox)
            ansi_grid.addWidget(wrapper, row, col)
            self._ansi_btns.append(btn)
        ansi_outer.addLayout(ansi_grid)

        # Live terminal preview
        self._term_preview = TerminalPreview(
            data.get("bg", "#0d1117"),
            [("user@ubuntu", data.get("fg", "#7ee787")),
             ("~", data.get("fg", "#8b949e")),
             ("$ echo hello", "#e6edf3"),
             ("hello", data.get("fg", "#7ee787"))],
        )
        ansi_outer.addWidget(QLabel("Preview:", styleSheet="color:#484f58;font-size:10px;letter-spacing:2px;"))
        ansi_outer.addWidget(self._term_preview)
        term_layout.addWidget(ansi_group)

        self._bg_btn.colorChanged.connect(self._update_preview)
        self._fg_btn.colorChanged.connect(self._update_preview)

        tabs.addTab(term_widget, "Terminal")

        # ── Desktop / GTK tab ─────────────────────────────────────────────────
        gtk_widget = QWidget()
        gtk_layout = QVBoxLayout(gtk_widget)
        gtk_layout.setSpacing(10)

        gtk_group = QGroupBox("GTK ACCENT COLORS")
        gtk_form = QFormLayout(gtk_group)
        gtk_form.setSpacing(8)

        self._accent_btn  = ColorButton(data.get("gtk_accent", "#58a6ff"))
        self._sel_btn     = ColorButton(data.get("gtk_sel",    "#2d6fd4"))
        self._hover_btn   = ColorButton(data.get("gtk_hover",  "#1c2128"))
        gtk_form.addRow(QLabel("Accent color:", styleSheet="color:#8b949e;font-size:12px;"), self._accent_btn)
        gtk_form.addRow(QLabel("Selection bg:", styleSheet="color:#8b949e;font-size:12px;"), self._sel_btn)
        gtk_form.addRow(QLabel("Hover bg:",     styleSheet="color:#8b949e;font-size:12px;"), self._hover_btn)

        font_row_combo = QComboBox()
        font_row_combo.addItems(["Ubuntu Regular","Cantarell Regular","Noto Sans","DejaVu Sans"])
        gtk_form.addRow(QLabel("UI font:", styleSheet="color:#8b949e;font-size:12px;"), font_row_combo)
        self._font_combo = font_row_combo

        opacity_row = QHBoxLayout()
        self._opacity_slider = QSlider(Qt.Horizontal)
        self._opacity_slider.setRange(70, 100)
        self._opacity_slider.setValue(data.get("terminal_opacity", 95))
        self._opacity_lbl = QLabel(f"{self._opacity_slider.value()}%", styleSheet="color:#8b949e;font-size:12px;min-width:32px;")
        self._opacity_slider.valueChanged.connect(lambda v: self._opacity_lbl.setText(f"{v}%"))
        opacity_row.addWidget(self._opacity_slider)
        opacity_row.addWidget(self._opacity_lbl)
        gtk_form.addRow(QLabel("Terminal opacity:", styleSheet="color:#8b949e;font-size:12px;"), opacity_row)
        gtk_layout.addWidget(gtk_group)

        # GTK CSS preview textarea (read-only)
        css_group = QGroupBox("GENERATED GTK CSS PREVIEW")
        css_v = QVBoxLayout(css_group)
        self._css_preview = QLabel()
        self._css_preview.setWordWrap(True)
        self._css_preview.setStyleSheet(
            "font-family:'Ubuntu Mono',monospace;font-size:10px;color:#8b949e;"
            "background:#0d1117;padding:8px;border-radius:4px;"
        )
        self._accent_btn.colorChanged.connect(self._refresh_css_preview)
        self._sel_btn.colorChanged.connect(self._refresh_css_preview)
        self._refresh_css_preview()
        css_v.addWidget(self._css_preview)
        gtk_layout.addWidget(css_group)
        gtk_layout.addStretch()

        tabs.addTab(gtk_widget, "Desktop / GTK")

        # ── Buttons ───────────────────────────────────────────────────────────
        btns = QHBoxLayout()
        save_btn = QPushButton("Save Theme", objectName="apply_btn")
        save_btn.clicked.connect(self._save)
        cancel = QPushButton("Cancel", objectName="secondary_btn")
        cancel.clicked.connect(self.reject)
        btns.addStretch()
        btns.addWidget(cancel)
        btns.addWidget(save_btn)
        root.addLayout(btns)

    def _update_preview(self):
        self._term_preview._bg = QColor(self._bg_btn.color())
        self._term_preview._lines = [
            ("user@ubuntu", self._fg_btn.color()),
            ("~",           "#8b949e"),
            ("$ echo hello","#e6edf3"),
            ("hello",       self._fg_btn.color()),
        ]
        self._term_preview.update()

    def _refresh_css_preview(self):
        acc = self._accent_btn.color()
        sel = self._sel_btn.color()
        css = (
            f"/* Auto-generated by Theme Designer */\n"
            f"@define-color accent_color {acc};\n"
            f"@define-color theme_selected_bg_color {sel};\n"
            f"button:hover {{ background-color: {self._hover_btn.color()}; }}\n"
            f"selection {{ background-color: {sel}; }}"
        )
        self._css_preview.setText(css)

    def _save(self):
        name = self._name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Name required", "Please enter a theme name.")
            return
        self._result_data = {
            "name": name,
            "bg":   self._bg_btn.color(),
            "fg":   self._fg_btn.color(),
            "cursor": self._cur_btn.color(),
            "ansi": [b.color() for b in self._ansi_btns],
            "gtk_accent":  self._accent_btn.color(),
            "gtk_sel":     self._sel_btn.color(),
            "gtk_hover":   self._hover_btn.color(),
            "ui_font":     self._font_combo.currentText(),
            "terminal_opacity": self._opacity_slider.value(),
        }
        self.accept()

    def result_data(self):
        return self._result_data


# ─── Main window ──────────────────────────────────────────────────────────────

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


class ThemeDesigner(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theme Designer  v2.0")
        self.setMinimumSize(900, 640)
        self.resize(1060, 700)
        self.setStyleSheet(APP_STYLESHEET)

        ensure_dirs()
        self._selected_wp      = None   # full path
        self._selected_pal     = None   # name key
        self._selected_theme   = None   # name key (full preset)
        self._selected_custom  = None   # name key (custom theme)
        self._nav_buttons      = []
        self._wp_cards         = {}     # filename → SelectableCard
        self._pal_cards        = {}
        self._theme_cards      = {}
        self._custom_cards     = {}
        self._custom_themes    = load_custom_themes()

        self._read_uuid()
        self._build_ui()

    # ── UUID ──────────────────────────────────────────────────────────────────

    def _read_uuid(self):
        try:
            with open(os.path.join(SETTING_DIR, "uuid.ini")) as f:
                self._uuid = f.read().strip()
        except FileNotFoundError:
            self._uuid = ""

    def _ensure_uuid(self):
        path = os.path.join(SETTING_DIR, "uuid.ini")
        os.makedirs(SETTING_DIR, exist_ok=True)
        if self._uuid:
            try:
                out = subprocess.check_output(
                    ["dconf", "list", "/org/gnome/terminal/legacy/profiles:/"], text=True
                )
                if self._uuid in out:
                    return self._uuid
            except Exception:
                pass
        new = subprocess.check_output(["uuidgen"], text=True).strip()
        with open(path, "w") as f:
            f.write(new)
        self._uuid = new
        return new

    # ── UI skeleton ───────────────────────────────────────────────────────────

    def _build_ui(self):
        central = QWidget(objectName="central")
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QWidget(objectName="sidebar")
        sidebar.setFixedWidth(195)
        sb = QVBoxLayout(sidebar)
        sb.setContentsMargins(0, 12, 0, 12)
        sb.setSpacing(0)

        self._stacked = QStackedWidget()

        nav = [
            ("  Wallpapers",   self._build_wallpapers_panel),
            ("  Terminal",     self._build_terminal_panel),
            ("  Full Themes",  self._build_themes_panel),
            ("  Custom Theme", self._build_custom_panel),
            ("  Fonts",        self._build_fonts_panel),
            ("  Settings",     self._build_settings_panel),
        ]
        self._add_sb_label(sb, "CUSTOMIZE")
        for i, (label, builder) in enumerate(nav[:4]):
            sb.addWidget(self._make_nav(label, i))
            self._stacked.addWidget(builder())
        self._add_sb_divider(sb)
        self._add_sb_label(sb, "MORE")
        for i, (label, builder) in enumerate(nav[4:], start=4):
            sb.addWidget(self._make_nav(label, i))
            self._stacked.addWidget(builder())

        sb.addStretch()
        apply_btn = QPushButton("✓  Apply Changes", objectName="apply_btn")
        apply_btn.clicked.connect(self._on_apply)
        sb.addWidget(apply_btn)

        root.addWidget(sidebar)
        root.addWidget(self._stacked)

        self._nav_buttons[0].setProperty("active", True)
        self._nav_buttons[0].style().unpolish(self._nav_buttons[0])
        self._nav_buttons[0].style().polish(self._nav_buttons[0])

        self._status = QStatusBar()
        self.setStatusBar(self._status)
        self._status.showMessage("● Ready  —  load wallpapers from ~/.ubuntu-customer/wallpapers/")

    def _add_sb_label(self, layout, text):
        lbl = QLabel(text, objectName="section_label")
        lbl.setContentsMargins(14, 8, 0, 4)
        layout.addWidget(lbl)

    def _add_sb_divider(self, layout):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color:#30363d;")
        line.setContentsMargins(0, 4, 0, 4)
        layout.addWidget(line)

    def _make_nav(self, label, index):
        btn = QPushButton(label, objectName="nav_btn")
        btn.setProperty("active", False)
        btn.clicked.connect(lambda _, i=index: self._switch(i))
        self._nav_buttons.append(btn)
        return btn

    def _switch(self, index):
        self._stacked.setCurrentIndex(index)
        for i, btn in enumerate(self._nav_buttons):
            btn.setProperty("active", i == index)
            btn.style().unpolish(btn)
            btn.style().polish(btn)

    # ── Wallpapers panel ──────────────────────────────────────────────────────

    def _build_wallpapers_panel(self):
        panel, inner = self._scroll_panel()
        layout = inner.layout()
        self._panel_header(layout, "Desktop Wallpaper",
                           "$ gsettings set org.gnome.desktop.background picture-uri-dark")

        # toolbar
        toolbar = QHBoxLayout()
        self._section_label_widget(toolbar, "WALLPAPERS FROM ~/.ubuntu-customer/wallpapers/")
        toolbar.addStretch()
        add_btn = QPushButton("+ Add Wallpaper", objectName="secondary_btn")
        add_btn.clicked.connect(self._add_wallpaper)
        refresh_btn = QPushButton("⟳ Refresh", objectName="secondary_btn")
        refresh_btn.clicked.connect(self._reload_wallpapers)
        toolbar.addWidget(refresh_btn)
        toolbar.addWidget(add_btn)
        layout.addLayout(toolbar)

        # grid container (rebuilt on reload)
        self._wp_grid_widget = QWidget()
        self._wp_grid_layout = QGridLayout(self._wp_grid_widget)
        self._wp_grid_layout.setSpacing(10)
        self._wp_grid_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._wp_grid_widget)

        self._wp_empty_lbl = QLabel(
            "No wallpapers found.\nAdd images to  ~/.ubuntu-customer/wallpapers/",
            alignment=Qt.AlignCenter,
        )
        self._wp_empty_lbl.setStyleSheet("color:#484f58;font-size:13px;padding:40px;")
        layout.addWidget(self._wp_empty_lbl)

        layout.addStretch()
        self._populate_wallpapers()
        return panel

    def _populate_wallpapers(self):
        # clear old cards
        for i in reversed(range(self._wp_grid_layout.count())):
            w = self._wp_grid_layout.itemAt(i).widget()
            if w:
                w.deleteLater()
        self._wp_cards.clear()

        files = list_wallpapers()
        self._wp_empty_lbl.setVisible(len(files) == 0)
        self._wp_grid_widget.setVisible(len(files) > 0)

        for idx, fname in enumerate(files):
            full_path = os.path.join(WP_DIR, fname)
            card = SelectableCard(full_path, "wp")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(0, 0, 0, 0)
            cl.setSpacing(0)

            # real image thumbnail
            thumb_lbl = QLabel(alignment=Qt.AlignCenter)
            thumb_lbl.setFixedHeight(90)
            thumb_lbl.setMinimumWidth(120)
            thumb_lbl.setStyleSheet("background:#0d1117;")
            px = QPixmap(full_path)
            if not px.isNull():
                thumb_lbl.setPixmap(
                    px.scaled(240, 90, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
                )
            else:
                thumb_lbl.setText("?")
                thumb_lbl.setStyleSheet("color:#484f58;background:#161b22;font-size:20px;")

            name_lbl = QLabel(fname, objectName="card_name")
            name_lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

            cl.addWidget(thumb_lbl)
            cl.addWidget(name_lbl)
            card.setFixedHeight(116)

            card.clicked.connect(self._on_wp_selected)
            self._wp_cards[full_path] = card
            self._wp_grid_layout.addWidget(card, idx // 3, idx % 3)

    def _on_wp_selected(self, path):
        for p, c in self._wp_cards.items():
            c.set_selected(p == path)
        self._selected_wp = path
        self._status.showMessage(f"● Wallpaper: {os.path.basename(path)}  — click Apply Changes")

    def _add_wallpaper(self):
        dlg = AddWallpaperDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            self._populate_wallpapers()
            self._status.showMessage(f"● Added: {os.path.basename(dlg.dest_path())}")

    def _reload_wallpapers(self):
        self._populate_wallpapers()
        self._status.showMessage("● Wallpaper list refreshed")

    # ── Terminal panel ────────────────────────────────────────────────────────

    def _build_terminal_panel(self):
        panel, inner = self._scroll_panel()
        layout = inner.layout()
        self._panel_header(layout, "Terminal Color Palette",
                           "$ dconf load /org/gnome/terminal/legacy/profiles:/")
        self._section_label_layout(layout, "BUILT-IN COLOR SCHEMES")

        grid_w = QWidget()
        grid = QGridLayout(grid_w)
        grid.setSpacing(10)
        grid.setContentsMargins(0, 0, 0, 0)

        for idx, (name, data) in enumerate(TERMINAL_PALETTES.items()):
            card = SelectableCard(name, "pal")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(0, 0, 0, 0)
            cl.setSpacing(0)

            strip = PaletteStrip(data["colors"])
            term = TerminalPreview(data["bg"], data["preview"])

            bot = QWidget()
            bot.setStyleSheet("background:#1c2128;border-bottom-left-radius:6px;border-bottom-right-radius:6px;")
            bl = QHBoxLayout(bot)
            bl.setContentsMargins(8, 5, 8, 5)
            nl = QLabel(name)
            nl.setStyleSheet("color:#8b949e;font-size:11px;background:transparent;")
            bdg = QLabel(data["badge"])
            bdg.setStyleSheet(
                f"color:{data['bc']};background:{data['bc']}22;"
                "font-size:9px;font-weight:bold;padding:2px 6px;border-radius:3px;"
            )
            bl.addWidget(nl); bl.addStretch(); bl.addWidget(bdg)

            cl.addWidget(strip)
            cl.addWidget(term)
            cl.addWidget(bot)

            card.clicked.connect(self._on_pal_selected)
            self._pal_cards[name] = card
            grid.addWidget(card, idx // 2, idx % 2)

        layout.addWidget(grid_w)
        layout.addStretch()
        return panel

    def _on_pal_selected(self, name):
        for n, c in self._pal_cards.items():
            c.set_selected(n == name)
        self._selected_pal = name
        self._status.showMessage(f"● Palette: {name}  — click Apply Changes")

    # ── Full themes panel ─────────────────────────────────────────────────────

    def _build_themes_panel(self):
        panel, inner = self._scroll_panel()
        layout = inner.layout()
        self._panel_header(layout, "Full Theme Presets",
                           "$ Wallpaper + GTK CSS + Terminal dconf in one click")
        self._section_label_layout(layout, "COMPLETE PRESETS")

        grid_w = QWidget()
        grid = QGridLayout(grid_w)
        grid.setSpacing(10)
        grid.setContentsMargins(0, 0, 0, 0)

        # accent colors per preset
        accents = {
            "Winter":"#5aa8d8","Forest":"#5aaa5a","Night":"#8888cc",
            "Autumn":"#d86010","Spring":"#d058a8","Spring Forest":"#7ee040",
            "Blue":"#58a6ff","Dark Blue":"#2d6fd4",
        }

        for idx, (name, data) in enumerate(FULL_THEMES.items()):
            wp_colors = WALLPAPER_PALETTES.get(data["wp"], ["#1a1a2e", "#0f3460"])
            accent = accents.get(name, "#7ee787")

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

        layout.addWidget(grid_w)
        layout.addStretch()
        return panel

    def _find_wallpaper_for_theme(self, theme_name):
        """Try to find a wallpaper file whose name contains the theme name (fuzzy)."""
        keyword = theme_name.lower().replace(" ", "-")
        for f in list_wallpapers():
            if keyword in f.lower():
                return os.path.join(WP_DIR, f)
        return None

    def _on_theme_selected(self, name):
        for n, c in self._theme_cards.items():
            c.set_selected(n == name)
        self._selected_theme = name
        self._status.showMessage(f"● Preset: {name}  — wallpaper + GTK + terminal")

    # ── Custom theme panel ────────────────────────────────────────────────────

    def _build_custom_panel(self):
        panel, inner = self._scroll_panel()
        layout = inner.layout()
        self._panel_header(layout, "Custom Theme Builder",
                           "$ Create your own terminal + desktop theme")

        toolbar = QHBoxLayout()
        self._section_label_widget(toolbar, "SAVED CUSTOM THEMES")
        toolbar.addStretch()
        new_btn = QPushButton("+ New Theme", objectName="apply_btn")
        new_btn.clicked.connect(self._new_custom_theme)
        toolbar.addWidget(new_btn)
        layout.addLayout(toolbar)

        self._custom_grid_widget = QWidget()
        self._custom_grid_layout = QGridLayout(self._custom_grid_widget)
        self._custom_grid_layout.setSpacing(10)
        self._custom_grid_layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._custom_grid_widget)

        self._custom_empty_lbl = QLabel(
            "No custom themes yet.\nClick  + New Theme  to create one.",
            alignment=Qt.AlignCenter,
        )
        self._custom_empty_lbl.setStyleSheet("color:#484f58;font-size:13px;padding:40px;")
        layout.addWidget(self._custom_empty_lbl)
        layout.addStretch()

        self._refresh_custom_grid()
        return panel

    def _refresh_custom_grid(self):
        for i in reversed(range(self._custom_grid_layout.count())):
            w = self._custom_grid_layout.itemAt(i).widget()
            if w:
                w.deleteLater()
        self._custom_cards.clear()

        themes = self._custom_themes
        self._custom_empty_lbl.setVisible(len(themes) == 0)
        self._custom_grid_widget.setVisible(len(themes) > 0)

        for idx, (name, data) in enumerate(themes.items()):
            card = SelectableCard(name, "custom")
            cl = QVBoxLayout(card)
            cl.setContentsMargins(0, 0, 0, 0)
            cl.setSpacing(0)

            # swatch
            ansi = data.get("ansi", ["#000"] * 16)
            strip = PaletteStrip(ansi[:8])
            term  = TerminalPreview(
                data.get("bg", "#0d1117"),
                [("user@ubuntu", data.get("fg", "#7ee787")),
                 ("~",           data.get("fg", "#8b949e")),
                 ("$ _",         "#e6edf3")],
            )
            bot = QWidget()
            bot.setStyleSheet("background:#1c2128;border-bottom-left-radius:6px;border-bottom-right-radius:6px;")
            bl = QHBoxLayout(bot)
            bl.setContentsMargins(8, 5, 8, 5)
            nl = QLabel(name)
            nl.setStyleSheet("color:#e6edf3;font-size:11px;font-weight:bold;background:transparent;")
            edit_btn = QPushButton("Edit", objectName="secondary_btn")
            edit_btn.setFixedHeight(22)
            edit_btn.clicked.connect(lambda _, n=name: self._edit_custom_theme(n))
            del_btn = QPushButton("✕", objectName="secondary_btn")
            del_btn.setFixedSize(22, 22)
            del_btn.setStyleSheet("color:#f78166;background:#1a0800;border:1px solid #6e3028;border-radius:4px;font-size:10px;")
            del_btn.clicked.connect(lambda _, n=name: self._delete_custom_theme(n))
            bl.addWidget(nl); bl.addStretch(); bl.addWidget(edit_btn); bl.addWidget(del_btn)

            cl.addWidget(strip)
            cl.addWidget(term)
            cl.addWidget(bot)

            card.clicked.connect(self._on_custom_selected)
            self._custom_cards[name] = card
            self._custom_grid_layout.addWidget(card, idx // 2, idx % 2)

    def _on_custom_selected(self, name):
        for n, c in self._custom_cards.items():
            c.set_selected(n == name)
        self._selected_custom = name
        self._status.showMessage(f"● Custom theme: {name}  — click Apply Changes")

    def _new_custom_theme(self):
        dlg = CustomThemeDialog(parent=self)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.result_data()
            self._custom_themes[d["name"]] = d
            save_custom_themes(self._custom_themes)
            self._refresh_custom_grid()
            self._status.showMessage(f"● Custom theme '{d['name']}' saved")

    def _edit_custom_theme(self, name):
        data = self._custom_themes.get(name, {})
        dlg = CustomThemeDialog(name=name, data=data, parent=self)
        if dlg.exec_() == QDialog.Accepted:
            d = dlg.result_data()
            # handle rename
            if d["name"] != name:
                del self._custom_themes[name]
            self._custom_themes[d["name"]] = d
            save_custom_themes(self._custom_themes)
            self._refresh_custom_grid()

    def _delete_custom_theme(self, name):
        reply = QMessageBox.question(self, "Delete theme",
                                     f"Delete '{name}'?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._custom_themes.pop(name, None)
            save_custom_themes(self._custom_themes)
            if self._selected_custom == name:
                self._selected_custom = None
            self._refresh_custom_grid()

    # ── Fonts panel ───────────────────────────────────────────────────────────

    def _build_fonts_panel(self):
        panel, inner = self._scroll_panel()
        layout = inner.layout()
        self._panel_header(layout, "Font Settings",
                           "$ gsettings set org.gnome.desktop.interface font-name")

        rows = [
            ("Interface font", ["Ubuntu Regular","Cantarell Regular","Noto Sans","DejaVu Sans"], 11),
            ("Monospace font", ["Ubuntu Mono","JetBrains Mono","Hack Regular","Fira Code"], 13),
            ("Document font",  ["Ubuntu Regular","Cantarell Regular","Liberation Serif"], 11),
        ]
        for label, fonts, size in rows:
            self._section_label_layout(layout, label.upper())
            rw = QWidget()
            rl = QHBoxLayout(rw)
            rl.setContentsMargins(0, 0, 0, 4)
            cb = QComboBox(); cb.addItems(fonts)
            sp = QSpinBox(); sp.setRange(8, 18); sp.setValue(size); sp.setFixedWidth(60)
            rl.addWidget(cb); rl.addWidget(sp)
            layout.addWidget(rw)

        self._section_label_layout(layout, "RENDERING")
        for lbl in ("Font antialiasing", "Subpixel hinting"):
            c = QCheckBox(lbl); c.setChecked(True); layout.addWidget(c)

        af = QPushButton("✓  Apply Fonts", objectName="apply_btn")
        af.setFixedWidth(150)
        af.clicked.connect(lambda: self._status.showMessage("● Fonts applied"))
        layout.addSpacing(8); layout.addWidget(af)
        layout.addStretch()
        return panel

    # ── Settings panel ────────────────────────────────────────────────────────

    def _build_settings_panel(self):
        panel, inner = self._scroll_panel()
        layout = inner.layout()
        self._panel_header(layout, "Settings", "$ ~/.ubuntu-customer/setting/")

        beh = QGroupBox("BEHAVIOR")
        bl = QVBoxLayout(beh)
        for lbl, chk in [("Auto-apply on selection", False),
                          ("Backup GTK before applying", True),
                          ("Remember last applied theme", True)]:
            cb = QCheckBox(lbl); cb.setChecked(chk); bl.addWidget(cb)
        layout.addWidget(beh)

        ab = QGroupBox("ABOUT")
        al = QVBoxLayout(ab)
        al.addWidget(QLabel(
            f"<pre style='color:#8b949e;font-family:Ubuntu Mono,monospace;"
            f"font-size:11px;line-height:1.8;'>"
            f"<span style='color:#7ee787'>version</span>  2.0.0\n"
            f"<span style='color:#7ee787'>wallpapers</span> ~/.ubuntu-customer/wallpapers/\n"
            f"<span style='color:#7ee787'>custom</span>   ~/.ubuntu-customer/custom/\n"
            f"<span style='color:#58a6ff'>uuid</span>     {self._uuid or '(not set)'}</pre>",
            textFormat=Qt.RichText,
        ))
        layout.addWidget(ab)

        dz = QGroupBox("DANGER ZONE")
        dl = QHBoxLayout(dz)
        rb = QPushButton("Reset all settings")
        rb.setStyleSheet("background:#1a0800;color:#f78166;border:1px solid #6e3028;border-radius:6px;padding:6px 14px;font-size:12px;")
        rb.clicked.connect(self._on_reset)
        dl.addWidget(rb); dl.addStretch()
        layout.addWidget(dz)
        layout.addStretch()
        return panel

    # ── Reusable helpers ──────────────────────────────────────────────────────

    def _scroll_panel(self):
        outer = QScrollArea()
        outer.setWidgetResizable(True)
        inner = QWidget(objectName="scroll_content")
        il = QVBoxLayout(inner)
        il.setContentsMargins(20, 20, 20, 20)
        il.setSpacing(8)
        outer.setWidget(inner)
        return outer, inner

    def _panel_header(self, layout, title, sub):
        layout.addWidget(QLabel(title, objectName="panel_title"))
        layout.addWidget(QLabel(sub,   objectName="panel_sub"))
        layout.addSpacing(8)

    def _section_label_layout(self, layout, text):
        lbl = QLabel(text, objectName="section_label")
        layout.addWidget(lbl)

    def _section_label_widget(self, hbox, text):
        lbl = QLabel(text, objectName="section_label")
        hbox.addWidget(lbl)

    # ── Apply logic ───────────────────────────────────────────────────────────

    def _on_apply(self):
        commands, applied = [], []

        # ── wallpaper ─────────────────────────────────────────────────────────
        if self._selected_wp and os.path.isfile(self._selected_wp):
            uri = f"file://{self._selected_wp}"
            commands += [
                f'gsettings set org.gnome.desktop.background picture-uri "{uri}"',
                f'gsettings set org.gnome.desktop.background picture-uri-dark "{uri}"',
            ]
            applied.append(f"Wallpaper: {os.path.basename(self._selected_wp)}")

        # ── custom theme ──────────────────────────────────────────────────────
        if self._selected_custom and self._selected_custom in self._custom_themes:
            data = self._custom_themes[self._selected_custom]
            commands += self._commands_for_custom(data)
            applied.append(f"Custom: {self._selected_custom}")

        # ── full preset ───────────────────────────────────────────────────────
        elif self._selected_theme and self._selected_theme in FULL_THEMES:
            t = FULL_THEMES[self._selected_theme]
            gtk_src   = os.path.join(GTK_DIR,   f"{t['gtk']}.css")
            dconf_src = os.path.join(DCONF_DIR,  f"{t['dconf']}.dconf")
            uuid = self._ensure_uuid()
            commands += [
                "cp ~/.config/gtk-3.0/gtk.css ~/.config/gtk-3.0/gtk-backup.css 2>/dev/null || true",
                f"cp '{gtk_src}' ~/.config/gtk-3.0/gtk.css",
                f"dconf load /org/gnome/terminal/legacy/profiles:/:{uuid}/ < '{dconf_src}'",
                f"gsettings set org.gnome.Terminal.ProfilesList list \"['{uuid}']\""
            ]
            applied.append(f"Theme: {self._selected_theme}")

        # ── individual palette ────────────────────────────────────────────────
        elif self._selected_pal:
            key = self._selected_pal.lower().replace(" ", "-")
            dconf_src = os.path.join(DCONF_DIR, f"{key}.dconf")
            uuid = self._ensure_uuid()
            commands += [
                f"dconf load /org/gnome/terminal/legacy/profiles:/:{uuid}/ < '{dconf_src}'",
                f"gsettings set org.gnome.Terminal.ProfilesList list \"['{uuid}']\""
            ]
            applied.append(f"Palette: {self._selected_pal}")

        if not commands:
            QMessageBox.information(self, "Nothing selected",
                                    "Select a wallpaper, palette, preset or custom theme first.")
            return

        self._status.showMessage("● Applying…")
        self._worker = ApplyWorker(commands)
        self._worker.done.connect(lambda ok, err: self._on_done(ok, err, applied))
        self._worker.start()

    def _commands_for_custom(self, data: dict) -> list:
        """Write a temp dconf file and GTK CSS from custom theme data, return commands."""
        uuid = self._ensure_uuid()
        # --- write dconf ini ---
        dconf_path = os.path.join(CUSTOM_DIR, "custom_term.dconf")
        bg  = data.get("bg",  "#0d1117")
        fg  = data.get("fg",  "#e6edf3")
        cur = data.get("cursor", "#7ee787")
        ansi = data.get("ansi", ["#000000"] * 16)
        palette_str = "['{}']".format("', '".join(ansi))
        dconf_content = (
            "[/]\n"
            f"background-color='{bg}'\n"
            f"foreground-color='{fg}'\n"
            f"cursor-colors-set=true\n"
            f"cursor-background-color='{cur}'\n"
            f"palette={palette_str}\n"
            f"use-theme-colors=false\n"
            f"use-transparent-background=true\n"
            f"background-transparency-percent={100 - data.get('terminal_opacity', 95)}\n"
        )
        os.makedirs(CUSTOM_DIR, exist_ok=True)
        with open(dconf_path, "w") as f:
            f.write(dconf_content)

        # --- write GTK CSS ---
        gtk_path = os.path.join(CUSTOM_DIR, "custom.css")
        accent  = data.get("gtk_accent", "#58a6ff")
        sel     = data.get("gtk_sel",    "#2d6fd4")
        hover   = data.get("gtk_hover",  "#1c2128")
        css = (
            f"/* Custom theme: {data.get('name','custom')} */\n"
            f"@define-color accent_color {accent};\n"
            f"@define-color theme_selected_bg_color {sel};\n"
            f"@define-color theme_selected_fg_color #ffffff;\n"
            f"button:hover {{ background-color: {hover}; }}\n"
            f"selection {{ background-color: {sel}; color: #ffffff; }}\n"
        )
        with open(gtk_path, "w") as f:
            f.write(css)

        return [
            "cp ~/.config/gtk-3.0/gtk.css ~/.config/gtk-3.0/gtk-backup.css 2>/dev/null || true",
            f"cp '{gtk_path}' ~/.config/gtk-3.0/gtk.css",
            f"dconf load /org/gnome/terminal/legacy/profiles:/:{uuid}/ < '{dconf_path}'",
            f"gsettings set org.gnome.Terminal.ProfilesList list \"['{uuid}']\""
        ]

    def _on_done(self, ok, err, applied):
        if ok:
            self._status.showMessage("✓  Applied: " + "  ·  ".join(applied))
            # QMessageBox.information(self, "Done",
                                    # "Applied:\n• " + "\n• ".join(applied))
        else:
            self._status.showMessage("✗  Error")
            QMessageBox.critical(self, "Error",
                                 f"Something went wrong:\n{err}\n\n"
                                 "Make sure ~/.ubuntu-customer/ paths exist and dconf is installed.")

    def _on_reset(self):
        if QMessageBox.question(self, "Reset", "Clear UUID cache and reset all settings?",
                                QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            try:
                os.remove(os.path.join(SETTING_DIR, "uuid.ini"))
            except FileNotFoundError:
                pass
            self._uuid = ""
            self._status.showMessage("● Settings reset")


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Theme Designer")
    app.setApplicationVersion("2.0")

    pal = QPalette()
    pal.setColor(QPalette.Window,          QColor("#0d1117"))
    pal.setColor(QPalette.WindowText,      QColor("#e6edf3"))
    pal.setColor(QPalette.Base,            QColor("#161b22"))
    pal.setColor(QPalette.AlternateBase,   QColor("#1c2128"))
    pal.setColor(QPalette.Text,            QColor("#e6edf3"))
    pal.setColor(QPalette.Button,          QColor("#21262d"))
    pal.setColor(QPalette.ButtonText,      QColor("#e6edf3"))
    pal.setColor(QPalette.Highlight,       QColor("#2d6fd4"))
    pal.setColor(QPalette.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)

    win = ThemeDesigner()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
