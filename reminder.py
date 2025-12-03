#!/usr/bin/env python3
import sys
import re
import time
import subprocess
import datetime
import argparse
import os
import json
import uuid
from pathlib import Path

# File to store reminders
DATA_FILE = Path.home() / ".reminder_cli.json"

def load_reminders():
    if not DATA_FILE.exists():
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_reminders(reminders):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(reminders, f, indent=2)
    except IOError as e:
        print(f"Error saving reminders: {e}")

def update_reminder_status(reminder_id, status, executed_at=None):
    reminders = load_reminders()
    for r in reminders:
        if r["id"] == reminder_id:
            r["status"] = status
            if executed_at:
                r["executed_at"] = executed_at
            break
    save_reminders(reminders)

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
        if target < now:
            # If time passed today, assume tomorrow? Or error? 
            # Original logic returned -1. Let's keep it simple or improve.
            # User might want to set reminder for tomorrow 8am.
            # For now, preserving original logic: strict future check for today.
            return -1
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

def notify(title, message, permanent=False):
    """Sends a desktop notification."""
    cmd = [
        "notify-send",
        "-a", "Reminder",
        "-u", "critical",
        title,
        message
    ]
    if permanent:
        # 0 means never expire (requires notification server support)
        cmd.extend(["-t", "0"])
        
    subprocess.run(cmd)

def list_reminders():
    reminders = load_reminders()
    if not reminders:
        print("No reminders found.")
        return

    print(f"{'ID':<36} | {'Status':<10} | {'Time':<20} | {'Permanent':<9} | {'Message'}")
    print("-" * 100)
    
    # Sort by status (pending first) then time
    reminders.sort(key=lambda x: (x["status"] != "pending", x["target_time"]))

    for r in reminders:
        status = r["status"]
        # specific check for missed pending reminders could go here
        target_dt = datetime.datetime.fromisoformat(r["target_time"])
        if status == "pending" and target_dt < datetime.datetime.now():
            status = "missed"
            
        print(f"{r['id']:<36} | {status:<10} | {r['target_time']:<20} | {str(r.get('permanent', False)):<9} | {r['message']}")

def main():
    parser = argparse.ArgumentParser(description="A simple CLI reminder tool.")
    # Make message and time optional to support --list
    parser.add_argument("message", nargs="?", help="The reminder message")
    parser.add_argument("time", nargs="?", help="Time delay (e.g. '10m', '1h') or absolute time ('15:30')")
    parser.add_argument("-m", "--mute", action="store_true", help="Disable sound alert")
    parser.add_argument("-r", "--repeat", type=int, default=1, help="Number of times to repeat")
    parser.add_argument("-p", "--permanent", action="store_true", help="Make the notification sticky (permanent)")
    parser.add_argument("-l", "--list", action="store_true", help="List all reminders")
    
    # Hidden flag for internal use (daemon mode)
    parser.add_argument("--_daemon", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--_id", help=argparse.SUPPRESS) # Internal ID to track execution

    args = parser.parse_args()

    # ==========================================
    # LIST MODE
    # ==========================================
    if args.list:
        list_reminders()
        sys.exit(0)

    # ==========================================
    # VALIDATION (If not listing)
    # ==========================================
    if not args._daemon and (not args.message or not args.time):
        parser.print_help()
        sys.exit(1)

    raw_seconds = parse_time(args.time)
    
    if raw_seconds is None:
        print(f"Error: Invalid time format '{args.time}'.")
        sys.exit(1)
    if raw_seconds < 0:
        print(f"Error: Time {args.time} has already passed today.")
        sys.exit(1)

    # ==========================================
    # PARENT PROCESS (Foreground)
    # ==========================================
    if not args._daemon:
        now = datetime.datetime.now()
        target_time = now + datetime.timedelta(seconds=raw_seconds)
        finish_time_str = target_time.strftime('%H:%M:%S')
        
        # 1. Create Record
        reminder_id = str(uuid.uuid4())
        new_reminder = {
            "id": reminder_id,
            "message": args.message,
            "created_at": now.isoformat(),
            "target_time": target_time.isoformat(),
            "status": "pending",
            "permanent": args.permanent,
            "mute": args.mute,
            "repeat": args.repeat
        }
        
        reminders = load_reminders()
        reminders.append(new_reminder)
        save_reminders(reminders)

        # 2. Print feedback
        print(f"✅ Reminder set!")
        print(f"ID:  {reminder_id}")
        print(f"Msg: {args.message}")
        print(f"At:  {finish_time_str}")
        if args.permanent:
            print("Type: Permanent (Sticky notification)")
        if args.repeat > 1:
            print(f"Repeat: {args.repeat} times")
        print("(Running in background. You can close this terminal.)")

        # 3. Spawn the detached process
        new_args = [sys.executable, os.path.abspath(__file__), args.message, args.time]
        if args.mute: new_args.append("--mute")
        if args.permanent: new_args.append("--permanent")
        if args.repeat > 1:
            new_args.append("--repeat")
            new_args.append(str(args.repeat))
        
        new_args.append("--_daemon")
        new_args.append("--_id")
        new_args.append(reminder_id)

        subprocess.Popen(
            new_args,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        sys.exit(0)

    # ==========================================
    # WORKER PROCESS (Background)
    # ==========================================
    
    # We need the ID to update status
    reminder_id = args._id

    for i in range(args.repeat):
        current_wait = raw_seconds
        time.sleep(current_wait)
        
        notify("Reminder", args.message, permanent=args.permanent)
        
        if not args.mute:
            play_sound()
        
        # Update DB after notification
        # Note: In a repeat loop, we might only want to mark 'done' after the last one,
        # or track repetition. For simplicity, we mark 'done' after the first success 
        # if repeat=1. If repeat > 1, we might want a 'repeating' status? 
        # Let's just update executed_at every time, and status to 'done' at the end.
        
        if reminder_id:
            status = "done" if (i == args.repeat - 1) else "pending"
            update_reminder_status(reminder_id, status, datetime.datetime.now().isoformat())

if __name__ == "__main__":
    main()
