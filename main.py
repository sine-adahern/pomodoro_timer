"""
main.py - Application entry point
"""
import sys
import time
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from PySide6.QtGui import QIcon

from timer_logic import PomodoroTimer, Mode
from storage import Storage
from ui import MainWindow


class PomodoroApp:
    """Main application controller."""
    
    def __init__(self):
        # Initialize storage
        self.storage = Storage()
        settings = self.storage.load_settings()
        
        # Initialize timer logic
        self.timer = PomodoroTimer(
            study_minutes=settings["study_minutes"],
            break_minutes=settings["break_minutes"],
            total_study_seconds=settings["total_study_seconds"]
        )
        
        # Initialize UI
        self.window = MainWindow()
        self.current_theme = settings["theme"]
        self.window.apply_theme(self.current_theme)
        
        # Connect signals
        self._connect_signals()
        
        # Set up refresh timer (tick every 200ms for smooth updates)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._on_tick)
        self.refresh_timer.start(200)  # 200ms interval
        
        # Auto-save timer (save total study time every 30 seconds)
        self.save_timer = QTimer()
        self.save_timer.timeout.connect(self._save_total_time)
        self.save_timer.start(30000)  # 30 seconds
        
        # Initial UI update
        self._update_ui()
        
        # Show window
        self.window.show()
    
    def _connect_signals(self) -> None:
        """Connect UI signals to handlers."""
        self.window.set_time_requested.connect(self._on_set_time)
        self.window.pause_clicked.connect(self._on_pause)
        self.window.reset_clicked.connect(self._on_reset)
        self.window.theme_requested.connect(self._on_theme)
    
    def _on_tick(self) -> None:
        """Handle timer tick - update timer state and UI."""
        now = time.monotonic()
        mode_switched = self.timer.tick(now)
        
        if mode_switched:
            # Play a beep when mode switches
            QApplication.beep()
        
        self._update_ui()
    
    def _update_ui(self) -> None:
        """Update all UI elements based on current timer state."""
        # Timer display
        time_str = self.timer.format_remaining()
        self.window.update_timer_display(time_str)
        
        # Mode display
        mode_text = self.timer.mode.value
        self.window.update_mode_display(mode_text)
        
        # Pause button
        self.window.update_pause_button(self.timer.running, self.timer.paused)
        
        # Progress bar
        progress = self.timer.get_progress()
        self.window.update_progress(progress)
        
        # Total time studied
        short, long = self.timer.format_total_study_time()
        self.window.update_total_time(short, long)
    
    def _on_set_time(self) -> None:
        """Handle set time dialog."""
        result = self.window.show_set_time_dialog(
            self.timer.study_minutes,
            self.timer.break_minutes
        )
        
        if result:
            study_min, break_min = result
            self.timer.set_config(study_min, break_min)
            
            # Save settings
            settings = self.storage.load_settings()
            settings["study_minutes"] = study_min
            settings["break_minutes"] = break_min
            self.storage.save_settings(settings)
            
            self._update_ui()
    
    def _on_pause(self) -> None:
        """Handle pause/resume button click."""
        self.timer.pause_toggle()
        self._update_ui()
    
    def _on_reset(self) -> None:
        """Handle reset button click."""
        self.timer.reset()
        self._update_ui()
    
    def _on_theme(self) -> None:
        """Handle theme selection."""
        theme = self.window.show_theme_dialog(self.current_theme)
        
        if theme:
            self.current_theme = theme
            self.window.apply_theme(theme)
            
            # Save theme
            settings = self.storage.load_settings()
            settings["theme"] = theme
            self.storage.save_settings(settings)
    
    def _save_total_time(self) -> None:
        """Periodically save total study time."""
        self.storage.update_total_study_seconds(self.timer.total_study_seconds)
    
    def cleanup(self) -> None:
        """Save data before exit."""
        self._save_total_time()


def main():
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Pomodoro Timer")
    
    # Create and run app
    pomo_app = PomodoroApp()
    
    # Save on exit
    app.aboutToQuit.connect(pomo_app.cleanup)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
