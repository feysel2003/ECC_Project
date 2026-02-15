import os
import random
import subprocess
from datetime import datetime, timedelta

# ================= CONFIGURATION =================
# 1. Start exactly when you joined
START_DATE = datetime(2024, 12, 8) 

# 2. End at the end of last year (2025)
END_DATE = datetime(2025, 12, 31)

# 3. Work Habits
MIN_COMMITS_PER_DAY = 1
MAX_COMMITS_PER_DAY = 5
CHANCE_TO_SKIP_WORKDAY = 15  # 15% chance to skip a random Tuesday, etc.
# =================================================

# Realistic Project Structure
PROJECT_FILES = [
    {"path": "index.html", "type": "html", "content": "<!-- Updated section -->\n"},
    {"path": "README.md", "type": "md", "content": "- Updated documentation\n"},
    {"path": "src/main.py", "type": "py", "content": "# Refactored logic\n"},
    {"path": "src/utils.py", "type": "py", "content": "def helper(): pass\n"},
    {"path": "assets/style.css", "type": "css", "content": ".container { display: block; }\n"},
    {"path": "assets/logo.png", "type": "binary", "content": "BIN"}, # Binary simulation
    {"path": "js/app.js", "type": "js", "content": "console.log('debug');\n"},
    {"path": "js/api.js", "type": "js", "content": "fetch('/api/data');\n"},
    {"path": "config/settings.json", "type": "json", "content": "{ \"version\": 1 }\n"},
]

COMMIT_MESSAGES = [
    "feat: initial setup", "style: improve layout", "fix: resolve bug in api",
    "refactor: clean up code", "docs: update readme", "chore: dependency update",
    "perf: optimize image loading", "test: add unit tests", "fix: css alignment issue"
]

def create_structure():
    """Creates the folders so the script doesn't crash."""
    dirs = ["src", "assets", "js", "config"]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    
    # Create initial empty files
    for f in PROJECT_FILES:
        if not os.path.exists(f["path"]):
            with open(f["path"], "w") as file:
                file.write("")

def git_commit(date_obj):
    # Select a random file to modify
    target_file = random.choice(PROJECT_FILES)
    file_path = target_file["path"]
    
    # Modify the file (Append dummy data so Git sees a change)
    # We use valid syntax comments so it looks real if opened
    with open(file_path, "a") as f:
        if target_file["type"] == "py":
            f.write(f"\n# Log update: {random.randint(1000,9999)}")
        elif target_file["type"] == "js":
            f.write(f"\n// Timestamp: {random.randint(1000,9999)}")
        elif target_file["type"] == "css":
            f.write(f"\n/* Style tweak {random.randint(100,900)} */")
        elif target_file["type"] == "html":
            f.write(f"\n<!-- Page update {random.randint(100,900)} -->")
        else:
            f.write(f"\nUpdate: {random.randint(100,900)}")

    # Git Add
    subprocess.run(["git", "add", file_path], check=True)
    
    # Generate Random Time (Ethiopia Working Hours: 09:00 - 18:00)
    hour = random.randint(9, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    
    # Format Date
    date_str = date_obj.replace(hour=hour, minute=minute, second=second).strftime('%Y-%m-%d %H:%M:%S')
    
    # Git Commit (Backdated)
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    msg = random.choice(COMMIT_MESSAGES)
    subprocess.run(["git", "commit", "-m", msg], env=env, check=True)

def main():
    create_structure()
    current_date = START_DATE
    total_commits = 0

    print(f"--- Generating Full Stack History from {START_DATE.date()} ---")

    while current_date <= END_DATE:
        # Skip Sundays (Looks human)
        if current_date.weekday() == 6: 
            current_date += timedelta(days=1)
            continue
            
        # Randomly skip workdays (Sick/Busy)
        if random.randint(1, 100) <= CHANCE_TO_SKIP_WORKDAY:
            current_date += timedelta(days=1)
            continue

        # Determine workload
        # Dec 2024: Light work (starting out)
        # 2025: Heavy work
        if current_date.year == 2024:
            daily_commits = random.randint(1, 3)
        else:
            daily_commits = random.randint(MIN_COMMITS_PER_DAY, MAX_COMMITS_PER_DAY)
        
        for _ in range(daily_commits):
            git_commit(current_date)
            total_commits += 1
            
        current_date += timedelta(days=1)

    print(f"--- SUCCESS: Generated {total_commits} commits across .js, .py, .css files ---")
    print("Now create a Private Repo on GitHub and push this.")

if __name__ == "__main__":
    main()