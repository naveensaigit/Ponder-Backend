# Ponder-Backend
This is the code for Ponder App's Backend.
The backend is written in python and we have used Flask for providing the API endpoints.

Steps to start backend (for Ubuntu):

1. Create a virtual environment.
      `python -m venv env`
2. Activate virtual environment.
      `source env/bin/activate`
3. Install requirements.
      `pip install -r requirements.txt`
4. Run app.py.
      `python app.py`

To use this locally hosted runtime in the Ponder App, we used `ngrok` and changed the corresponding URL in `Ponder-Frontend` to include this URL.
