# Secure Password Generator

A professional desktop password generator with advanced customization, strength indicators, and generation history.

## Features

### Core Functionality
- **Cryptographically Secure Generation**: Uses Python's `secrets` module for true randomness
- **Customizable Character Types**: Toggle lowercase, uppercase, digits, and special characters independently
- **Ambiguous Character Exclusion**: Option to exclude confusing characters (0, O, 1, l, I)
- **Flexible Length**: Generate passwords from 4 to 1024 characters (default: 16, recommended minimum)
- **Extended Special Characters**: Support for 14 special characters: `!@#$%^&*()_+-=[]{}|;:,.<>?`

### User Experience
- **Real-time Strength Indicator**: Visual progress bar with strength levels (Weak, Fair, Strong, Very Strong)
- **Session History**: View and reuse the last 10 generated passwords
- **Non-intrusive Feedback**: Subtle status messages instead of popup dialogs
- **Keyboard Shortcuts**: Press Enter to generate passwords
- **Read-only Display**: Password field is protected from accidental edits

### Security
- Passwords are never stored persistently (session history only)
- Optional Supabase integration for tracking generation metadata only
- Row-level security on all cloud data
- No actual passwords transmitted or stored in the cloud

## Installation

### Requirements
- Python 3.8 or higher
- Tkinter (usually included with Python)

### Setup
1. Clone this repository
2. Navigate to the project directory
3. No external dependencies required for the desktop app (only built-in Python libraries)

## Usage

### Basic Usage
```bash
python3 main.py
```

### Generating Passwords
1. Adjust the desired password length (default: 16)
2. Select which character types to include
3. Optionally exclude ambiguous characters
4. Click "Generate Password" or press Enter
5. Click "Copy" to copy to clipboard or select from history

### Understanding Strength Levels
- **Weak**: Short passwords or limited character variety
- **Fair**: Medium length with some character variety
- **Strong**: Good length (12+) with multiple character types
- **Very Strong**: Long passwords (20+) with all character types

## Architecture

### File Structure
- `main.py`: GUI application and user interface
- `password_generator.py`: Core password generation logic with strength calculation
- `requirements.txt`: Python version requirements

### Design Principles
- **Separation of Concerns**: Password generation logic is independent of UI
- **Type Hints**: Full type annotations for better code maintainability
- **Constants-Based Configuration**: Easy customization of UI colors and settings
- **Error Handling**: Comprehensive validation and user-friendly error messages

## Optional Cloud Features

The project includes a Supabase database schema for optional password generation tracking:

### Enable Cloud History (Advanced)
To track password generation metadata in the cloud:
1. Create a Supabase account at https://supabase.com
2. Connect your Supabase credentials to the app
3. Metadata like password length, character types used, and strength will be saved

**Important**: Actual passwords are NEVER stored. Only generation parameters and timestamps are tracked.

## Privacy & Security

- Local desktop app with no mandatory cloud connectivity
- Passwords remain on your machine during the session
- No sensitive data is logged or transmitted
- Ambient session history (cleared on app close)
- Optional, opt-in cloud features with full encryption

## License

Educational project - feel free to modify and improve.

## Future Enhancements

Potential improvements for future versions:
- Multi-language support
- Batch password generation with export
- Dark/light theme toggle
- Password validation against common weak passwords
- Integration with password managers
- Cross-platform packaging (executable builds)
