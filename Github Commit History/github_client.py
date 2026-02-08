import requests
from datetime import datetime, timezone
import config

def fetch_commits(since_datetime=None):
    """
    Fetch commits from GitHub API for the authenticated user.
    If since_datetime is provided, only fetch commits after that time.
    Returns a list of commit objects or relevant data.
    """
    url = "https://api.github.com/search/commits"
    
    # Construct query: author:USERNAME and committed:>TIMESTAMP
    # First, we need the username. We can fetch it or ask the user to provide it.
    # Ideally, we fetch the authenticated user's login first.
    
    headers = {
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.cloak-preview" # Search commits API preview
    }
    
    # Get current user login
    user_resp = requests.get("https://api.github.com/user", headers=headers)
    if user_resp.status_code != 200:
        print(f"Error fetching user: {user_resp.status_code} {user_resp.text}")
        return []
        
    username = user_resp.json()["login"]
    
    query = f"author:{username}"
    if since_datetime:
        # ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ
        timestamp = since_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
        query += f" committer-date:>{timestamp}"
    
    # Wait, fetching ALL commits might be too much.
    # The requirement is "fetch github commit history ... for that day".
    # So we probably interested in commits *today*.
    
    # Let's refine the logic. When the script runs, it should update the daily note with *today's* commits.
    # So we should fetch commits for the current day (in local time? or UTC? usually local for daily notes).
    # But GitHub API uses UTC.
    
    # For now, let's just use the query for "committer-date" covering the whole day.
    # We can calculate the start of the day in UTC.
    
    params = {
        "q": query,
        "sort": "committer-date",
        "order": "desc",
        "per_page": 100
    }
    
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code != 200:
        print(f"Error fetching commits: {resp.status_code} {resp.text}")
        return []
        
    return resp.json().get("items", [])

def get_commits_for_date(target_date):
    """
    Fetch commits for a specific date (datetime.date object).
    The API expects ISO timestamps. We'll search for the whole 24h period of that date.
    Note: Timezone handling is tricky. Daily notes are usually local time.
    GitHub commits are UTC.
    We might miss commits if we don't handle timezone correctly.
    For MVP, we can just ask for committer-date:YYYY-MM-DD which implies UTC?
    Actually GitHub search `committer-date:2024-01-01` matches that day.
    """
    date_str = target_date.strftime("%Y-%m-%d")
    
    headers = {
        "Authorization": f"token {config.GITHUB_TOKEN}",
        "Accept": "application/vnd.github.cloak-preview"
    }
    
    # Get current user login
    user_resp = requests.get("https://api.github.com/user", headers=headers)
    if user_resp.status_code != 200:
        print(f"Error fetching user: {user_resp.status_code} {user_resp.text}")
        return []
    
    username = user_resp.json()["login"]
    
    query = f"author:{username} committer-date:{date_str}"
    
    params = {
        "q": query,
        "sort": "committer-date",
        "order": "desc",
        "per_page": 100
    }
    
    resp = requests.get("https://api.github.com/search/commits", headers=headers, params=params)
    if resp.status_code != 200:
        print(f"Error fetching commits: {resp.status_code} {resp.text}")
        return []
        
    return resp.json().get("items", [])
