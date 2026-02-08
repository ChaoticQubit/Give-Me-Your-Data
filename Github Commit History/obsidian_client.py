import os
import re
from datetime import datetime
import config

def update_daily_note(commit_items):
    """
    Update the daily note with the list of commits.
    """
    # Path format: Daily Notes/2026/February/5th February, 2026 - Thursday
    # We need to construct this dynamically.
    
    today = datetime.now()
    
    year = today.strftime("%Y")
    month_name = today.strftime("%B")
    day = today.day
    
    # Suffix logic for day (1st, 2nd, 3rd, 4th...)
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    
    day_str = f"{day}{suffix}"
    weekday = today.strftime("%A")
    
    # Construct filename: "5th February, 2026 - Thursday"
    filename = f"{day_str} {month_name}, {year} - {weekday}.md"
    
    # Construct full path
    # Using config.DAILY_NOTE_BASE_PATH which defaults to "Daily Notes"
    # Structure: Base / Year / Month / Filename
    # Note: User example showed "Daily Notes/2026/February/..."
    
    note_path_rel = os.path.join(config.DAILY_NOTE_BASE_PATH, year, month_name, filename)
    note_path = os.path.join(config.OBSIDIAN_VAULT_PATH, note_path_rel)
    
    if not os.path.exists(note_path):
        print(f"Daily note not found at {note_path}. Skipping update.")
        return

    try:
        with open(note_path, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading daily note: {e}")
        return

    # Process commits into a simple list or count
    # Let's store a list of messages or just a count?
    # User asked to "update the github commit property".
    # Assuming it's a list or a string. Let's make it a list of strings: "Repo: Message"
    
    frontmatter_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        print("No frontmatter found in daily note in the expected format.")
        # Optionally create it? For now, skip.
        return

    frontmatter_content = frontmatter_match.group(1)
    
    # Check if property exists
    prop_regex = re.compile(f"^{config.PROPERTY_NAME}:.*$", re.MULTILINE)

    # Process commits into a simple count
    commit_count = len(commit_items)
    
    new_prop_str = f"{config.PROPERTY_NAME}: {commit_count}"
    
    if prop_regex.search(frontmatter_content):
        # Replace existing property
        # We need to match the property and its values (indented lines)
        # This is tricky with regex. 
        # Easier: Read frontmatter into lines, find the line with property, remove following indented lines, insert new lines.
        
        lines = frontmatter_content.split("\n")
        new_lines = []
        skip = False
        inserted = False
        
        for line in lines:
            if line.strip().startswith(f"{config.PROPERTY_NAME}:"):
                new_lines.append(new_prop_str)
                inserted = True
                skip = True # skip old values
            elif skip and (line.startswith("  ") or line.startswith("- ")): # assuming indented list items
                continue
            else:
                skip = False
                new_lines.append(line)
        
        new_frontmatter = "\n".join(new_lines)
        
    else:
        # Append property
        new_frontmatter = frontmatter_content + "\n" + new_prop_str

    new_content = f"---\n{new_frontmatter}\n---" + content[frontmatter_match.end():]
    
    with open(note_path, "w") as f:
        f.write(new_content)
    
    print(f"Updated daily note: {note_path}")
