git clone https://your-repo-url.git
cd playwright_automation

# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt

#install Brwosers
playwright install
pip install pytest


#to run all the test
pytest

#to run a specfic test
pytest tests/test_example.py

#to run a test in in visible mode
pytest tests/test_example.py --headed

#to run a test in different Brwosers
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit






# to remove cache files before commit

chmod +x cleanup_playwright_repo.py

Before committing code:
 python cleanup_playwright_repo.py
To see what would be deleted without actually deleting:
 python cleanup_playwright_repo.py --dry-run
To clean everything except logs:
 python cleanup_playwright_repo.py --keep-logs