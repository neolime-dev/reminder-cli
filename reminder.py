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
    # Try relative (10m, 1h)
    match_rel = re.match(r'^(\d+)([hms])$', time_str)
    if match_rel:
        val = int(match_rel.group(1))
        unit = match_rel.group(2)
        if unit == 's': return val
        if unit == 'm': return val * 60
        if unit == 'h': return val * 3600
    
    # Try absolute (15:30)
    match_abs = re.match(r'^(\d{1,2}):(\d{2})$', time_str)
    if match_abs:
        now = datetime.datetime.now()
        h = int(match_abs.group(1))
        m = int(match_abs.group(2))
        target = now.replace(hour=h, minute=m, second=0, microsecond=0)
        
        if target < now:
            # If time has passed
            return -1
        
        delta = target - now
        return int(delta.total_seconds())

    return None

def play_sound():
    """Plays a system alert sound if available."""
    # Common path for the 'complete' sound on Freedesktop compliant systems
    sound_path = "/usr/share/sounds/freedesktop/stereo/complete.oga"
    
    if os.path.exists(sound_path):
        try:
            # paplay is the standard PulseAudio/PipeWire player
            subprocess.run(["paplay", sound_path], stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            pass # Silently fail if paplay is missing

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
    
    parser.add_argument("message", help="The reminder message (e.g. 'Drink water')")
    parser.add_argument("time", help="Time delay (e.g. '10m', '1h') or absolute time ('15:30')")
    
    parser.add_argument("-m", "--mute", action="store_true", 
                        help="Disable sound alert")
    
    parser.add_argument("-r", "--repeat", type=int, default=1,
                        help="Number of times to repeat the reminder (default: 1)")

    args = parser.parse_args()

    raw_seconds = parse_time(args.time)
    
    if raw_seconds is None:
        print(f"Error: Invalid time format '{args.time}'. Use '10m', '1h' or 'HH:MM'.")
        sys.exit(1)
        
    if raw_seconds < 0:
        print(f"Error: Time {args.time} has already passed today.")
        sys.exit(1)

    # Calculation for display only (first iteration)
    finish_time = (datetime.datetime.now() + datetime.timedelta(seconds=raw_seconds)).strftime('%H:%M:%S')
    print(f"✅ Reminder set!")
    print(f"Msg: {args.message}")
    print(f"At:  {finish_time}")
    if args.repeat > 1:
        print(f"Repeat: {args.repeat} times")

    # The Main Loop
    for i in range(args.repeat):
        # If this is a repeat loop (i > 0), we need to recalculate seconds 
        # IF the input was relative (e.g. 10m). 
        # If input was absolute (15:30), repeat doesn't make sense immediately, 
        # but for simplicity we treat 'repeat' as 'wait the same duration again'.
        
        current_wait = raw_seconds
        
        # Sleep
        time.sleep(current_wait)
        
        # Notify
        notify("Reminder", args.message)
        
        # Sound
        if not args.mute:
            play_sound()

        # Feedback for loops
        if i < args.repeat - 1:
            # Only print if attached to a terminal
            if sys.stdout.isatty():
                print(f"🔁 Repeating... ({i+1}/{args.repeat})")

if __name__ == "__main__":
    main()