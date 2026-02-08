import time
import schedule
from datetime import datetime
import config
import github_client
import obsidian_client

def job():
    print(f"Starting job at {datetime.now()}")
    try:
        # 1. Fetch commits for today
        today = datetime.now().date()
        commits = github_client.get_commits_for_date(today)
        print(f"Found {len(commits)} commits.")
        
        # 2. Update Obsidian Note
        if commits:
            obsidian_client.update_daily_note(commits)
        else:
            print("No commits found, skipping update.")
            
    except Exception as e:
        print(f"Job failed: {e}")

def main():
    print("GitHub Commit History Automation Started")
    
    # Run once immediately
    job()
    
    # Schedule every 30 minutes
    schedule.every(30).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
