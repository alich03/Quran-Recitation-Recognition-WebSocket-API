import sys
import os

# Ensure the current directory is in the system path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
from api.websocket_api import app

# Additional code to run the app
if __name__ == "__main__":
    import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app)
