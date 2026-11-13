import subprocess
import api
import app
import time

#basic start of all fucntions together

try:
    print("Staring Fast API.")
    runApi = subprocess.Popen(["uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8000","--reload"])
    print(runApi.returncode)

    time.sleep(2)

    print("Staring Fast APP.")
    runApp = subprocess.Popen(["streamlit", "run", "app.py"])
    print(runApp.returncode)

    runApi.wait()
    runApp.wait()

except KeyboardInterrupt:
    print("\nShutting down servers...")
    runApi.terminate()
    runApp.terminate()
    print("Both servers stopped successfully.")