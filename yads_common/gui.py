#!/usr/bin/env python3
import sys
import re
import html as _html
import traceback
import subprocess
from pathlib import Path
from datetime import datetime
from PySide6.QtCore import Qt, Signal, QObject, QThread, QTimer, QSize, Slot
from PySide6.QtGui import QIcon, QFont, QColor
from qfluentwidgets import isDarkTheme

_ANSI_RE = re.compile(r'\x1b\[[0-9;]*[mGKHF]|\r')

def detect_system_dark_mode() -> bool:
    """Detect if system is using dark mode"""
    try:
        import darkdetect
        if darkdetect.isDark(): return True
    except:
        pass

    # Fallback: check GTK settings on Linux
    try:
        # Check color-scheme (modern standard)
        res1 = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'], capture_output=True, text=True, timeout=1)
        out1 = res1.stdout.lower()
        if 'dark' in out1 or 'prefer-dark' in out1: return True
        
        # Check gtk-theme (fallback for Mint/Cinnamon/Old GNOME)
        res2 = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'], capture_output=True, text=True, timeout=1)
        if 'dark' in res2.stdout.lower(): return True
        
        # Check KDE (Plasma)
        # Some newer KDE versions use different keys, but ColorScheme is still a good fallback
        res3 = subprocess.run(['kreadconfig5', '--group', 'General', '--key', 'ColorScheme'], capture_output=True, text=True, timeout=1)
        if 'dark' in res3.stdout.lower(): return True
    except:
        pass

    return False

def get_log_stylesheet(dark: bool = None) -> str:
    """Get stylesheet for log view based on theme"""
    if dark is None:
        dark = isDarkTheme()

    if dark:
        return """
            TextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border-radius: 8px;
                padding: 12px;
            }
        """
    else:
        return """
            TextEdit {
                background-color: #f5f5f5;
                color: #1e1e1e;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 12px;
                border-radius: 8px;
                padding: 12px;
                border: 1px solid #e0e0e0;
            }
        """

def _insert_log_line(log_view, message: str, level: str = "info"):
    """Thread-safe HTML log insert with escaping and document size limit."""
    dark = isDarkTheme()
    if dark:
        colors = {"info": "#d4d4d4", "success": "#4ec9b0", "warning": "#dcdcaa", "error": "#f14c4c", "cmd": "#808080"}
        ts_color = "#6a9955"
    else:
        colors = {"info": "#1e1e1e", "success": "#107c10", "warning": "#ca5010", "error": "#d13438", "cmd": "#808080"}
        ts_color = "#107c10"
    color = colors.get(level, colors["info"])
    timestamp = datetime.now().strftime("%H:%M:%S")
    safe_msg = _html.escape(str(message))
    line = f'<span style="color:{ts_color};">[{timestamp}]</span> <span style="color:{color};">{safe_msg}</span><br>'
    
    doc = log_view.document()
    if doc.blockCount() > 2000:
        cur = log_view.textCursor()
        cur.movePosition(cur.MoveOperation.Start)
        cur.movePosition(cur.MoveOperation.Down, cur.MoveMode.KeepAnchor, 200)
        cur.removeSelectedText()
    cur = log_view.textCursor()
    cur.movePosition(cur.MoveOperation.End)
    log_view.setTextCursor(cur)
    log_view.insertHtml(line)
    log_view.ensureCursorVisible()

class LogSignals(QObject):
    """Signals for thread-safe log updates"""
    log_message = Signal(str, str)  # message, level
    operation_finished = Signal(bool, str)  # success, message
    progress_update = Signal(int, int, str)  # current, total, description

class StdoutCapture:
    """Captures stdout and emits to signal"""
    def __init__(self, signal):
        self.signal = signal
        self.buffer = ""

    def write(self, text):
        if text:
            self.buffer += text
            while '\n' in self.buffer:
                line, self.buffer = self.buffer.split('\n', 1)
                if line.strip():
                    self.signal.emit(line, "info")

    def flush(self):
        if self.buffer.strip():
            self.signal.emit(self.buffer, "info")
            self.buffer = ""
