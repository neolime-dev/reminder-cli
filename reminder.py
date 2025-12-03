#!/usr/bin/env python3
import sys
import re
import time
import subprocess
import datetime
import argparse
import os

def parse_time(time_str):
    """Parses time strings like '10m', '1h', '30s' or '15:30' into seconds."""
    match_rel = re.match(r'^(\d+)([hms])$', time_str)
    if match_rel:
        val = int(match_rel.group(1))
        unit = match_rel.group(2)
        if unit == 's': return val
        if unit == 'm': return val * 60
        if unit == 'h': return val * 3600
    
    match_abs = re.match(r'^(\d{1,2}):(\d{2})$', time_str)
    if match_abs:
        now = datetime.datetime.now()
        h = int(match_abs.group(1))
        m = int(match_abs.group(2))
        target = now.replace(hour=h, minute=m, second=0, microsecond=0)
        if target < now: return -1
        delta = target - now
        return int(delta.total_seconds())

    return None

def play_sound():
    """Plays a system alert sound if available."""
    sound_path = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    if os.path.exists(sound_path):
        try:
            subprocess.run(["paplay", sound_path], stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass

def notify(title, message):
    """Sends a desktop notification."""
    subprocess.run([
        "notify-send",
        "-a", "Reminder",
        "-u", "critical",
        title,
        message
    ])

def main():
    parser = argparse.ArgumentParser(description="A simple CLI reminder tool.")
    parser.add_argument("message", help="The reminder message")
    parser.add_argument("time", help="Time delay (e.g. '10m', '1h') or absolute time ('15:30')")
    parser.add_argument("-m", "--mute", action="store_true", help="Disable sound alert")
    parser.add_argument("-r", "--repeat", type=int, default=1, help="Number of times to repeat")
    
    # Hidden flag for internal use (daemon mode)
    parser.add_argument("--_daemon", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args()

    raw_seconds = parse_time(args.time)
    
    if raw_seconds is None:
        print(f"Error: Invalid time format '{args.time}'.")
        sys.exit(1)
    if raw_seconds < 0:
        print(f"Error: Time {args.time} has already passed today.")
        sys.exit(1)

    # ==========================================
    # DAEMON LOGIC (The magic happens here)
    # ==========================================
    if not args._daemon:
        # PARENT PROCESS (Foreground)
        # 1. Print feedback to user
        finish_time = (datetime.datetime.now() + datetime.timedelta(seconds=raw_seconds)).strftime('%H:%M:%S')
        print(f"✅ Reminder set!")
        print(f"Msg: {args.message}")
        print(f"At:  {finish_time}")
        if args.repeat > 1:
            print(f"Repeat: {args.repeat} times")
        print("(Running in background. You can close this terminal.)")

        # 2. Prepare arguments for the child
        # We reconstruct the command line but add the hidden --_daemon flag
        new_args = [sys.executable, os.path.abspath(__file__), args.message, args.time]
        if args.mute: new_args.append("--mute")
        if args.repeat > 1:
            new_args.append("--repeat")
            new_args.append(str(args.repeat))
        
        new_args.append("--_daemon")

        # 3. Spawn the detached process
        subprocess.Popen(
            new_args,
            start_new_session=True, # DETACH from terminal
            stdout=subprocess.DEVNULL, # Silence output
            stderr=subprocess.DEVNULL  # Silence errors
        )
        
        # 4. Exit immediately
        sys.exit(0)

    # ==========================================
    # WORKER PROCESS (Background)
    # ==========================================
    
    # The loop logic runs here, invisible to the user
    for i in range(args.repeat):
        # Recalculate time for each loop (important for relative times)
        # but we use the initial raw_seconds for the first wait logic or simple reuse
        current_wait = raw_seconds
        
        time.sleep(current_wait)
        
        notify("Reminder", args.message)
        
        if not args.mute:
            play_sound()

if __name__ == "__main__":
    main()
