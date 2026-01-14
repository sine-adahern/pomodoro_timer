"""
ui.py - Main window UI with header, timer card, buttons, and progress bar
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QDialog, QSpinBox, QDialogButtonBox, QMessageBox,
    QColorDialog, QFrame
)
from PySide6.QtCore import Qt, Signal, QRect
from PySide6.QtGui import QPainter, QColor, QFont, QPalette, QMouseEvent


class ProgressBar(QWidget):
    """Custom progress bar widget for bottom strip."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = 0.0
        self.bg_color = QColor("#FFD6E0")  # Lighter pink
        self.fill_color = QColor("#FF9BB5")  # Accent pink
        self.setFixedHeight(28)
    
    def set_progress(self, progress: float) -> None:
        """Set progress value (0.0 to 1.0)."""
        self.progress = max(0.0, min(1.0, progress))
        self.update()
    
    def set_colors(self, bg_color: str, fill_color: str) -> None:
        """Update colors for theming."""
        self.bg_color = QColor(bg_color)
        self.fill_color = QColor(fill_color)
        self.update()
    
    def paintEvent(self, event):
        """Draw the progress bar."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Draw fill
        if self.progress > 0:
            fill_width = int(self.width() * self.progress)
            fill_rect = QRect(0, 0, fill_width, self.height())
            painter.fillRect(fill_rect, self.fill_color)


class TimerCard(QWidget):
    """Custom clickable timer card widget."""
    
    clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 300)
        self.bg_color = QColor("#FFD6E0")
        self.border_color = QColor("#FF9BB5")
        self.text_color = QColor("#FFFFFF")
        
        # Create label for timer text
        self.timer_label = QLabel("Set time", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(72)
        font.setBold(True)
        self.timer_label.setFont(font)
        self.timer_label.setStyleSheet("background: transparent; color: white;")
        
        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.timer_label)
        layout.setContentsMargins(20, 20, 20, 20)
    
    def set_time_text(self, text: str) -> None:
        """Update the timer display text."""
        self.timer_label.setText(text)
    
    def set_colors(self, bg_color: str, border_color: str, text_color: str) -> None:
        """Update colors for theming."""
        self.bg_color = QColor(bg_color)
        self.border_color = QColor(border_color)
        self.text_color = QColor(text_color)
        self.timer_label.setStyleSheet(f"background: transparent; color: {text_color};")
        self.update()
    
    def paintEvent(self, event):
        """Draw the card with border."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self.bg_color)
        
        # Draw border
        painter.setPen(self.border_color)
        painter.drawRect(self.rect().adjusted(0, 0, -1, -1))
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Emit clicked signal when card is clicked."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()


class SetTimeDialog(QDialog):
    """Dialog for configuring study and break durations."""
    
    def __init__(self, study_minutes: int, break_minutes: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Set time and breaks")
        self.setModal(True)
        self.setFixedSize(350, 200)
        
        layout = QVBoxLayout(self)
        
        # Study minutes
        study_layout = QHBoxLayout()
        study_label = QLabel("Study (minutes):")
        self.study_spin = QSpinBox()
        self.study_spin.setRange(1, 180)
        self.study_spin.setValue(study_minutes)
        study_layout.addWidget(study_label)
        study_layout.addWidget(self.study_spin)
        layout.addLayout(study_layout)
        
        # Break minutes
        break_layout = QHBoxLayout()
        break_label = QLabel("Break (minutes):")
        self.break_spin = QSpinBox()
        self.break_spin.setRange(1, 60)
        self.break_spin.setValue(break_minutes)
        break_layout.addWidget(break_label)
        break_layout.addWidget(self.break_spin)
        layout.addLayout(break_layout)
        
        layout.addStretch()
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def get_values(self) -> tuple[int, int]:
        """Return (study_minutes, break_minutes)."""
        return self.study_spin.value(), self.break_spin.value()


class ThemeDialog(QDialog):
    """Dialog for selecting color theme."""
    
    def __init__(self, current_theme: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Theme")
        self.setModal(True)
        self.setFixedSize(300, 250)
        
        self.current_theme = current_theme
        self.selected_theme = None
        
        layout = QVBoxLayout(self)
        
        # Preset buttons
        presets = [
            ("Pink (Default)", {
                "background_color": "#FFE5EC",
                "card_color": "#FFD6E0",
                "accent_color": "#FF9BB5",
                "progress_color": "#FF9BB5",
                "text_color": "#FFFFFF"
            }),
            ("Blue", {
                "background_color": "#E3F2FD",
                "card_color": "#BBDEFB",
                "accent_color": "#42A5F5",
                "progress_color": "#42A5F5",
                "text_color": "#FFFFFF"
            }),
            ("Green", {
                "background_color": "#E8F5E9",
                "card_color": "#C8E6C9",
                "accent_color": "#66BB6A",
                "progress_color": "#66BB6A",
                "text_color": "#FFFFFF"
            })
        ]
        
        for name, theme in presets:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, t=theme: self.select_preset(t))
            layout.addWidget(btn)
        
        layout.addStretch()
        
        # Custom button
        custom_btn = QPushButton("Custom...")
        custom_btn.clicked.connect(self.select_custom)
        layout.addWidget(custom_btn)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
    
    def select_preset(self, theme: dict) -> None:
        """Select a preset theme."""
        self.selected_theme = theme
        self.accept()
    
    def select_custom(self) -> None:
        """Open color picker for custom theme."""
        bg_color = QColorDialog.getColor(
            QColor(self.current_theme["background_color"]),
            self,
            "Choose Background Color"
        )
        if not bg_color.isValid():
            return
        
        card_color = QColorDialog.getColor(
            QColor(self.current_theme["card_color"]),
            self,
            "Choose Card Color"
        )
        if not card_color.isValid():
            return
        
        accent_color = QColorDialog.getColor(
            QColor(self.current_theme["accent_color"]),
            self,
            "Choose Accent/Text Color"
        )
        if not accent_color.isValid():
            return
        
        progress_color = QColorDialog.getColor(
            QColor(self.current_theme["progress_color"]),
            self,
            "Choose Progress Fill Color"
        )
        if not progress_color.isValid():
            return
        
        self.selected_theme = {
            "background_color": bg_color.name(),
            "card_color": card_color.name(),
            "accent_color": accent_color.name(),
            "progress_color": progress_color.name(),
            "text_color": "#FFFFFF"
        }
        self.accept()
    
    def get_theme(self) -> dict:
        """Return selected theme."""
        return self.selected_theme


class MainWindow(QMainWindow):
    """Main application window."""
    
    # Signals
    set_time_requested = Signal()
    pause_clicked = Signal()
    reset_clicked = Signal()
    theme_requested = Signal()
    reset_total_requested = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setMinimumSize(1200, 700)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        self.header = self._create_header()
        main_layout.addWidget(self.header)
        
        # Main content area (centered timer)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setAlignment(Qt.AlignCenter)
        
        # Mode label
        self.mode_label = QLabel("study")
        self.mode_label.setAlignment(Qt.AlignCenter)
        mode_font = QFont()
        mode_font.setPointSize(16)
        self.mode_label.setFont(mode_font)
        content_layout.addWidget(self.mode_label)
        
        # Timer card
        self.timer_card = TimerCard()
        self.timer_card.clicked.connect(self.set_time_requested.emit)
        content_layout.addWidget(self.timer_card, alignment=Qt.AlignCenter)
        
        content_layout.addSpacing(20)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        self.pause_button = QPushButton("pause")
        self.pause_button.setFixedSize(100, 40)
        self.pause_button.clicked.connect(self.pause_clicked.emit)
        buttons_layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("reset")
        self.reset_button.setFixedSize(100, 40)
        self.reset_button.clicked.connect(self.reset_clicked.emit)
        buttons_layout.addWidget(self.reset_button)
        
        content_layout.addLayout(buttons_layout)
        
        main_layout.addWidget(content, stretch=1)
        
        # Bottom progress bar
        self.progress_bar = ProgressBar()
        main_layout.addWidget(self.progress_bar)
        
        # Apply default theme
        self.apply_theme({
            "background_color": "#FFE5EC",
            "card_color": "#FFD6E0",
            "accent_color": "#FF9BB5",
            "progress_color": "#FF9BB5",
            "text_color": "#FFFFFF"
        })
    
    def _create_header(self) -> QWidget:
        """Create the top header bar."""
        header = QFrame()
        header.setFixedHeight(70)
        header.setStyleSheet("""
            QFrame {
                background-color: white;
                border-bottom: 2px solid #FF9BB5;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Left spacer
        layout.addStretch()
        
        # Right side - Theme button and total time
        self.theme_button = QPushButton("Theme")
        self.theme_button.setFlat(True)
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.clicked.connect(self.theme_requested.emit)
        layout.addWidget(self.theme_button)
        
        layout.addSpacing(30)
        
        # Total time studied label
        total_label = QLabel("total time studied")
        total_font = QFont()
        total_font.setPointSize(11)
        total_label.setFont(total_font)
        layout.addWidget(total_label)
        
        layout.addSpacing(10)
        
        # Total time value
        self.total_time_label = QLabel("0.00 h")
        self.total_time_label.setFont(total_font)
        self.total_time_label.setStyleSheet("font-weight: bold;")
        self.total_time_label.setCursor(Qt.WhatsThisCursor)
        layout.addWidget(self.total_time_label)
        
        return header
    
    def update_timer_display(self, time_str: str) -> None:
        """Update the timer card display."""
        self.timer_card.set_time_text(time_str)
    
    def update_mode_display(self, mode: str) -> None:
        """Update the mode label."""
        self.mode_label.setText(mode)
    
    def update_pause_button(self, is_running: bool, is_paused: bool) -> None:
        """Update pause button text."""
        if is_running and not is_paused:
            self.pause_button.setText("pause")
        else:
            self.pause_button.setText("start")
    
    def update_progress(self, progress: float) -> None:
        """Update the progress bar."""
        self.progress_bar.set_progress(progress)
    
    def update_total_time(self, short_format: str, long_format: str) -> None:
        """Update total time studied display."""
        self.total_time_label.setText(short_format)
        self.total_time_label.setToolTip(long_format)
    
    def apply_theme(self, theme: dict) -> None:
        """Apply color theme to the UI."""
        bg_color = theme["background_color"]
        card_color = theme["card_color"]
        accent_color = theme["accent_color"]
        progress_color = theme["progress_color"]
        text_color = theme["text_color"]
        
        # Main background
        self.centralWidget().setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
            }}
        """)
        
        # Header styling
        self.header.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-bottom: 2px solid {accent_color};
            }}
        """)
        
        # Theme button and labels
        self.theme_button.setStyleSheet(f"""
            QPushButton {{
                color: {accent_color};
                font-weight: bold;
                font-size: 13px;
                background: transparent;
                border: none;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        
        self.mode_label.setStyleSheet(f"color: {accent_color};")
        
        header_labels = self.header.findChildren(QLabel)
        for label in header_labels:
            label.setStyleSheet(f"color: {accent_color}; background: transparent;")
        
        # Timer card
        self.timer_card.set_colors(card_color, accent_color, text_color)
        
        # Buttons
        button_style = f"""
            QPushButton {{
                background-color: white;
                color: {accent_color};
                border: 2px solid {accent_color};
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {accent_color};
                color: white;
            }}
        """
        self.pause_button.setStyleSheet(button_style)
        self.reset_button.setStyleSheet(button_style)
        
        # Progress bar
        lighter_bg = self._lighten_color(bg_color)
        self.progress_bar.set_colors(lighter_bg, progress_color)
    
    def _lighten_color(self, hex_color: str) -> str:
        """Lighten a hex color for progress background."""
        color = QColor(hex_color)
        h, s, v, a = color.getHsv()
        # Increase value (brightness) by 10%
        v = min(255, int(v * 1.1))
        color.setHsv(h, s, v, a)
        return color.name()
    
    def show_set_time_dialog(self, study_min: int, break_min: int) -> tuple[int, int] | None:
        """Show the set time dialog and return values if accepted."""
        dialog = SetTimeDialog(study_min, break_min, self)
        if dialog.exec() == QDialog.Accepted:
            return dialog.get_values()
        return None
    
    def show_theme_dialog(self, current_theme: dict) -> dict | None:
        """Show theme selection dialog."""
        dialog = ThemeDialog(current_theme, self)
        if dialog.exec() == QDialog.Accepted:
            return dialog.get_theme()
        return None
    
    def show_reset_total_confirmation(self) -> bool:
        """Show confirmation dialog for resetting total study time."""
        reply = QMessageBox.question(
            self,
            "Reset Total Study Time",
            "Are you sure you want to reset your total study time to zero?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes
