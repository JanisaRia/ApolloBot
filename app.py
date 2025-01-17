from flask import Flask, redirect
from flask_cors import CORS
from constants import STREAMLIT_URL
import os
import subprocess
import time
import requests

app = Flask(__name__)
CORS(app)

STREAMLIT_PROCESS = None

def start_streamlit_app():
    """Starts the Streamlit app in a subprocess."""
    global STREAMLIT_PROCESS
    if STREAMLIT_PROCESS is None or STREAMLIT_PROCESS.poll() is not None:  # Check if already running
        print("Starting Streamlit app...")
        try:
            STREAMLIT_PROCESS = subprocess.Popen(['streamlit', 'run', 'interface.py'])
            
            timeout = 30  # Max wait time in seconds
            start_time = time.time()

            while True:
                try:
                    requests.get(STREAMLIT_URL)
                    print(f"Streamlit started at {STREAMLIT_URL}")
                    break  # Streamlit is up
                except requests.ConnectionError:
                    if time.time() - start_time > timeout:
                        print("Timed out waiting for Streamlit to start.")
                        return False
                    time.sleep(0.2)  # Check every 0.2 seconds
        except Exception as e:
            print(f"Error starting Streamlit app: {e}")
            return False
    else:
        print("Streamlit is already running.")
    return True


@app.route('/')
def home():
    print("Home route accessed.")
    if start_streamlit_app():
         return redirect(STREAMLIT_URL, code=302) 
    else:
        return "Failed to start Streamlit application. Check logs."


if __name__ == "__main__":
    app.run(debug=True)  
