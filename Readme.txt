git clone git@github.com:madhan-QA/playwright-automation.git
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

#to run a test in Headed mode
pytest --headed

#to run a specfic test
pytest tests/test_example.py

#to run a test in in visible mode
pytest tests/test_example.py --headed

#to run a test in different Brwosers
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit


#To run with Allure report
pip install allure-pytest

#To run all the test with Allure output
pytest --headed --alluredir=allure-results

#To run specfic test with Allure output
pytest tests/test_example.py --headed --alluredir=allure-results

#Generate and open report
allure serve allure-results

#To browser Debug
page.pause() #Need to add the commend in specfic line where you want to Debug



#project structure 
playwright-python/
├── tests/ # Test files
├── pages/ # Page Object Model (POM) classes
├── data/ # Input JSON files (test data)
├── conftest.py # Pytest setup and fixtures
├── requirements.txt # Python dependencies
└── README.md # This file 



# to remove cache files before commit
chmod +x cleanup_playwright_repo.py

Before committing code:
 python cleanup_playwright_repo.py
To see what would be deleted without actually deleting:
 python cleanup_playwright_repo.py --dry-run
To clean everything except logs:
 python cleanup_playwright_repo.py --keep-logs





