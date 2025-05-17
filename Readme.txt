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

