# Pomodoro Timer

A beautiful desktop Pomodoro timer built with Python and PySide6 (Qt for Python).

## Features

- **Clean, Modern UI**: Soft pink pastel theme with customizable colors
- **Pomodoro Method**: Alternates between study and break sessions
- **Accurate Time Tracking**: Uses monotonic time to avoid drift
- **Total Study Time**: Tracks and displays cumulative study time
- **Customizable Themes**: Choose from Pink, Blue, Green presets or create custom colors
- **Persistent Settings**: All configurations and total time are saved locally
- **Progress Bar**: Visual progress indicator for current session
- **Auto-switching**: Automatically switches between study and break modes

## Requirements

- Python 3.10 or higher
- PySide6

## Installation

1. Clone or download this project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Usage

### First Run
- The timer will show "Set time" on the card
- Click the timer card to configure study and break durations
- Default: 30 minutes study, 5 minutes break

### Controls
- **Timer Card**: Click to open settings and change durations
- **Pause Button**: Pause/resume the current session
- **Reset Button**: Reset current session to full duration
- **Theme**: Click to change color theme
- **Total Time**: Displays accumulated study time (hover for detailed format)

### Behavior
- Timer automatically starts the next session when current one completes
- A beep sound plays when switching between study and break
- Only study time (when timer is running and not paused) counts toward total
- Progress bar shows completion of current session
- All settings and total time persist between app restarts

### Settings Location
Settings are stored in: `~/.pomo_timer/settings.json`

## Project Structure

```
pomodoro_timer/
├── main.py           # Application entry point
├── ui.py             # UI components and main window
├── timer_logic.py    # Timer state machine and time tracking
├── storage.py        # Settings persistence (JSON)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Customization

### Themes
Click "Theme" in the header to choose:
- **Pink** (default): Soft pink pastel
- **Blue**: Calm blue tones
- **Green**: Fresh green colors
- **Custom**: Pick your own colors for background, card, accent, and progress

### Time Configuration
Click the timer card to adjust:
- Study duration: 1-180 minutes
- Break duration: 1-60 minutes

## Technical Details

- **Framework**: PySide6 (Qt for Python 6)
- **Timer Accuracy**: Uses `time.monotonic()` for drift-free timing
- **Update Rate**: UI refreshes every 200ms for smooth progress
- **Auto-save**: Total study time saved every 30 seconds and on exit
- **Cross-platform**: Works on Windows, macOS, and Linux

## License

Free to use and modify for personal or commercial projects.
