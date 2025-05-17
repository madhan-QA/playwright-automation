git clone https://your-repo-url.git
cd playwright_automation

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
playwright install

pip install pytest



# to remove cache files before commit

chmod +x cleanup_playwright_repo.py

Before committing code:
 python cleanup_playwright_repo.py
To see what would be deleted without actually deleting:
 python cleanup_playwright_repo.py --dry-run
To clean everything except logs:
 python cleanup_playwright_repo.py --keep-logs