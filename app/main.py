from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

# Serve static files (CSS, JS, images) from the static folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the CV upload router
from app.routes.cv_upload import router as cv_upload_router

app.include_router(cv_upload_router)


@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Read and return the HTML file
    with open("index.html", "r") as file:
        return HTMLResponse(content=file.read())
