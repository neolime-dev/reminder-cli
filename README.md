# Reminder CLI

A simple, lightweight CLI utility for Linux that sends native desktop notifications after a set period of time. Perfect for Window Manager users (i3, Sway, Hyprland, etc.) or any desktop environment.

## ✨ New Features (Desde a última atualização)

- **Persistent Reminders**: Todos os avisos são agora armazenados num arquivo JSON (`~/.reminder_cli.json`), permitindo que você veja o histórico, avisos agendados e avisos 'perdidos' (missed).
- **Avisos Permanentes**: Notificações que não desaparecem automaticamente até serem fechadas manualmente.

## 🚀 Features

- Simple, natural syntax (e.g., `10m`, `1h`, `15:30`).
- Native integration with system notifications (`notify-send`).
- Lightweight: Written in Python with zero heavy dependencies.
- Detached execution: Runs in the background, freeing up your terminal immediately.
- **Sound Alerts**: Plays an audible alert by default when a reminder triggers.
- **Repeat Reminders**: Schedule a reminder to repeat multiple times.
- **Command-line Parsing**: Uses `argparse` for robust command-line argument handling and a helpful `--help` page.

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
    git clone https://github.com/YOUR_USERNAME/reminder-cli.git
    cd reminder-cli
    ```

2.  Install using `make`:
    ```bash
    sudo make install
    ```
    (This will copy the `reminder.py` script to `/usr/local/bin/reminder` and make it executable.)

## 📖 Usage

```bash
reminder "Message" <time> [options]
```
Ou para listar avisos:
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

# At a specific time (hoje), with sound, once
reminder "Lunch" 12:00

# Every 30 seconds, 3 times
reminder "Quick break" 30s -r 3

# Um aviso permanente para não esquecer de algo importante
reminder "Concluir relatório X" 30m --permanent

# Listar todos os avisos (pendentes, concluídos, perdidos)
reminder --list
```

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.