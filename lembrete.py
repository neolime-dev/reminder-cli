#!/usr/bin/env python3
import sys
import re
import time
import subprocess
import datetime

def print_usage():
    print("""Usage: lembrete "Message" <time>

Examples:
  lembrete "Take out the trash" 10m
  lembrete "Team Meeting" 1h
  lembrete "Daily" 15:30""")

def parse_time(time_str):
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

def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    msg = sys.argv[1]
    time_str = sys.argv[2]
    
    seconds = parse_time(time_str)
    
    if seconds is None:
        print(f"Error: Invalid time format '{time_str}'.")
        print_usage()
        sys.exit(1)
        
    if seconds < 0:
        print(f"Error: Time {time_str} has already passed today.")
        sys.exit(1)
    
    # Escape single quotes for shell safety
    safe_msg = msg.replace("'", "'\\\'"")
    
    # Command to run in background detached
    # sleep X && notify-send ...
    cmd = f"sleep {seconds} && notify-send -a 'Reminder' 'Reminder' '{safe_msg}' -u critical"
    
    # Execute detached
    subprocess.Popen(['sh', '-c', cmd], start_new_session=True)
    
    # Calculate finish time for visual feedback
    finish_time = (datetime.datetime.now() + datetime.timedelta(seconds=seconds)).strftime('%H:%M:%S')
    
    print(f"✅ Reminder set!")
    print(f"Msg: {msg}")
    print(f"At:  {finish_time}")

if __name__ == "__main__":
    main()