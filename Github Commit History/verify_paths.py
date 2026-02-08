import os
from datetime import datetime
import config

def verify_path():
    today = datetime.now()
    
    # Logic from obsidian_client.py
    year = today.strftime("%Y")
    month_name = today.strftime("%B")
    day = today.day
    
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    day_str = f"{day}{suffix}"
    weekday = today.strftime("%A")
    filename = f"{day_str} {month_name}, {year} - {weekday}.md"
    
    note_path_rel = os.path.join(config.DAILY_NOTE_BASE_PATH, year, month_name, filename)
    note_path = os.path.join(config.OBSIDIAN_VAULT_PATH, note_path_rel)
    
    print(f"Calculated relative path: {note_path_rel}")
    print(f"Full path: {note_path}")
    print(f"Exists: {os.path.exists(note_path)}")

if __name__ == "__main__":
    verify_path()
