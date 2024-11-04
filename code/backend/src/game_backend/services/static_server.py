from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .api_server import app as ws_app

app = FastAPI()

# Mount the WebSocket app at /ws
app.mount("/ws", ws_app)

# Serve static files from the frontend build directory
app.mount("/", StaticFiles(directory="/app/frontend/build", html=True), name="frontend")

# Serve index.html for the root path
@app.get("/")
async def serve_index():
    return FileResponse("/app/frontend/build/index.html")