Step 1: If you are trying to run this in a Windows we recommend you do so using WSL for windows that run Linux(Ubuntu) commands for ease of access. Install WSL for windows.

Step 2: Install python3.

Step 3: Run command
sudo apt update && sudo apt upgrade 

Step 4: Set up a virtual environment (optional but recommended)
python3 -m venv .venv
source venv/bin/activate

Step 5: Install dependencies
pip install -r requirements.txt

Step 6: Initialize the database
python app.py
CTRL C

Step 7: Populate with sample data
python data_populate.py

Step 8:  Repeat step 6 and now use Postman to check the routes.
