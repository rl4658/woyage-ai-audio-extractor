from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Woyage AI Audio Extractor")

# mount static files (CSS/JS/images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# set up Jinja2 templates folder
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def homepage(request: Request):
    """
    Renders the main page.
    Later, form submissions will post to /video/extract-audio.
    """
    return templates.TemplateResponse("index.html", {"request": request})
