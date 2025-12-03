# Reminder CLI

A simple, lightweight CLI utility for Linux that sends native desktop notifications after a set period of time. Perfect for Window Manager users (i3, Sway, Hyprland, etc.) or any desktop environment.

## 🚀 Features

- Simple, natural syntax (e.g., `10m`, `1h`, `15:30`).
- Native integration with system notifications (`notify-send`).
- Lightweight: Written in Python with zero heavy dependencies.
- Detached execution: Runs in the background, freeing up your terminal immediately.

## 📋 Prerequisites

- **Python 3**
- **libnotify** (`notify-send` command)
  - Arch: `sudo pacman -S libnotify`
  - Debian/Ubuntu: `sudo apt install libnotify-bin`

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/reminder-cli.git
   cd reminder-cli
   ```

2. Make it executable and install it to your PATH (e.g., `~/.local/bin`):
   ```bash
   chmod +x reminder.py
   cp reminder.py ~/.local/bin/reminder
   ```

3. Ensure `~/.local/bin` is in your system's PATH.

## 📖 Usage

```bash
reminder "Message" <time>
```

### Examples

```bash
# In 10 minutes
reminder "Take out the trash" 10m

# In 1 hour
reminder "Team Meeting" 1h

# At a specific time (today)
reminder "Lunch" 12:00

# Just seconds
reminder "Quick test" 30s
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
