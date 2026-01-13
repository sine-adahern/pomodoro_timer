"""
timer_logic.py - Pomodoro timer state machine and time accounting
"""
import time
from enum import Enum
from typing import Optional


class Mode(Enum):
    """Timer modes."""
    STUDY = "study"
    BREAK = "break"


class PomodoroTimer:
    """
    Pomodoro timer logic with accurate time tracking.
    
    Uses monotonic time to avoid drift and accurately tracks study time.
    """
    
    def __init__(self, study_minutes: int = 30, break_minutes: int = 5, 
                 total_study_seconds: float = 0):
        """
        Initialize the timer.
        
        Args:
            study_minutes: Duration of study sessions in minutes
            break_minutes: Duration of break sessions in minutes
            total_study_seconds: Previously accumulated study time
        """
        self.study_minutes = study_minutes
        self.break_minutes = break_minutes
        self.total_study_seconds = total_study_seconds
        
        # Current state
        self.mode = Mode.STUDY
        self.running = False
        self.paused = False
        
        # Time tracking
        self.duration_seconds = study_minutes * 60
        self.remaining_seconds = self.duration_seconds
        self.end_time: Optional[float] = None  # monotonic time when timer should end
        self.last_tick_time: Optional[float] = None  # For tracking study time
        
    def start(self) -> None:
        """Start or resume the timer."""
        if not self.running or self.paused:
            now = time.monotonic()
            self.running = True
            self.paused = False
            # Set end time based on remaining seconds
            self.end_time = now + self.remaining_seconds
            self.last_tick_time = now
    
    def pause_toggle(self) -> None:
        """Toggle between paused and running states."""
        if not self.running:
            self.start()
            return
        
        now = time.monotonic()
        
        if self.paused:
            # Resume: adjust end_time based on remaining
            self.paused = False
            self.end_time = now + self.remaining_seconds
            self.last_tick_time = now
        else:
            # Pause: update remaining and track study time
            if self.end_time:
                self.remaining_seconds = max(0, self.end_time - now)
            self._track_study_time(now)
            self.paused = True
    
    def reset(self) -> None:
        """Reset the current session to full duration."""
        self.running = False
        self.paused = False
        self.duration_seconds = (self.study_minutes * 60 if self.mode == Mode.STUDY 
                                else self.break_minutes * 60)
        self.remaining_seconds = self.duration_seconds
        self.end_time = None
        self.last_tick_time = None
    
    def set_config(self, study_minutes: int, break_minutes: int) -> None:
        """
        Update timer configuration and reset current session.
        
        Args:
            study_minutes: New study duration
            break_minutes: New break duration
        """
        self.study_minutes = study_minutes
        self.break_minutes = break_minutes
        self.reset()
    
    def tick(self, now_monotonic: float) -> bool:
        """
        Update timer state based on current time.
        
        Args:
            now_monotonic: Current monotonic time (time.monotonic())
        
        Returns:
            True if mode switched, False otherwise
        """
        if not self.running or self.paused:
            return False
        
        # Track study time since last tick
        self._track_study_time(now_monotonic)
        
        # Update remaining time
        if self.end_time:
            self.remaining_seconds = max(0, self.end_time - now_monotonic)
        
        # Check if session completed
        if self.remaining_seconds <= 0:
            self._switch_mode()
            # Auto-start next session
            self.start()
            return True
        
        return False
    
    def _track_study_time(self, now: float) -> None:
        """Track elapsed study time if in study mode and running."""
        if (self.mode == Mode.STUDY and self.running and not self.paused 
            and self.last_tick_time is not None):
            elapsed = now - self.last_tick_time
            self.total_study_seconds += elapsed
        
        self.last_tick_time = now
    
    def _switch_mode(self) -> None:
        """Switch between study and break modes."""
        if self.mode == Mode.STUDY:
            self.mode = Mode.BREAK
            self.duration_seconds = self.break_minutes * 60
        else:
            self.mode = Mode.STUDY
            self.duration_seconds = self.study_minutes * 60
        
        self.remaining_seconds = self.duration_seconds
        self.running = False
        self.paused = False
        self.end_time = None
    
    def get_progress(self) -> float:
        """
        Get current session progress.
        
        Returns:
            Progress as a float between 0.0 and 1.0
        """
        if self.duration_seconds == 0:
            return 0.0
        elapsed = self.duration_seconds - self.remaining_seconds
        return min(1.0, max(0.0, elapsed / self.duration_seconds))
    
    def format_remaining(self) -> str:
        """
        Format remaining time as MM:SS.
        
        Returns:
            Formatted time string
        """
        total_secs = int(self.remaining_seconds)
        minutes = total_secs // 60
        seconds = total_secs % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def format_total_study_time(self) -> tuple[str, str]:
        """
        Format total study time in two formats.
        
        Returns:
            Tuple of (short_format, long_format)
            - short_format: "X.XX h"
            - long_format: "HH:MM:SS"
        """
        total_secs = int(self.total_study_seconds)
        hours = total_secs // 3600
        minutes = (total_secs % 3600) // 60
        seconds = total_secs % 60
        
        hours_decimal = self.total_study_seconds / 3600
        short = f"{hours_decimal:.2f} h"
        long = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return short, long
    
    def reset_total_study_time(self) -> None:
        """Reset total accumulated study time to zero."""
        self.total_study_seconds = 0
