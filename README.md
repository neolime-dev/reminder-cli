# Reminder CLI

A simple, lightweight CLI utility for Linux that sends native desktop notifications after a set period of time. Perfect for Window Manager users (i3, Sway, Hyprland, etc.) or any desktop environment.

## 🚀 Features

- **Simple Syntax**: Natural time formats (e.g., `10m`, `1h`, `15:30`).
- **Native Integration**: Uses system notifications (`notify-send`).
- **Persistent Reminders**: All reminders are stored in a JSON file (`~/.reminder_cli.json`), allowing you to view history, scheduled reminders, and missed notifications.
- **Permanent Reminders**: Option to create sticky notifications that do not disappear until manually closed.
- **Lightweight**: Written in Python with zero heavy dependencies.
- **Detached Execution**: Runs in the background, freeing up your terminal immediately.
- **Sound Alerts**: Plays an audible alert by default when a reminder triggers.
- **Repeat Reminders**: Schedule a reminder to repeat multiple times.

## 📋 Prerequisites

- **Python 3**
- **libnotify** (`notify-send` command)
  - Arch: `sudo pacman -S libnotify`
  - Debian/Ubuntu: `sudo apt install libnotify-bin`
- **paplay** (part of PulseAudio/PipeWire, usually pre-installed on modern Linux desktops for sound alerts)

## 🛠️ Installation

You can install `reminder` using the provided `Makefile`.

1.  Clone the repository:
    ```bash
    git clone https://github.com/neolime-dev/reminder-cli.git
    cd reminder-cli
    ```

2.  Install using `make`:
    ```bash
    sudo make install
    ```
    (This will copy the `reminder.py` script to `/usr/local/bin/reminder` and make it executable.)

### Manual Installation (No Make)

If you don't have `make` or prefer to install manually:

1.  Copy the script to your bin directory:
    ```bash
    sudo cp reminder.py /usr/local/bin/reminder
    ```
2.  Make it executable:
    ```bash
    sudo chmod +x /usr/local/bin/reminder
    ```

## 📖 Usage

Create a new reminder:
```bash
reminder "Message" <time> [options]
```

List all reminders (pending, done, missed):
```bash
reminder --list
```

### Options

*   `-m`, `--mute`: Disable sound alert for the reminder.
*   `-r N`, `--repeat N`: Number of times to repeat the reminder (e.g., `-r 5`). Default is 1.
*   `-p`, `--permanent`: Make the notification sticky (permanent), meaning it won't disappear until manually dismissed.
*   `-l`, `--list`: Display a table of all scheduled, pending, and past reminders.

### Examples

```bash
# In 10 minutes (with sound, once)
reminder "Take out the trash" 10m

# In 1 hour, without sound
reminder "Team Meeting" 1h --mute

# At a specific time (today), with sound, once
reminder "Lunch" 12:00

# Every 30 seconds, 3 times
reminder "Quick break" 30s -r 3

# A permanent reminder (sticky) for something important
reminder "Finish Report X" 30m --permanent

# List all reminders (pending, completed, missed)
reminder --list
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
