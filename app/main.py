from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from .langchain_chain import run_extraction

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/extract", response_class=HTMLResponse)
async def extract(request: Request, job_description: str = Form(...)):
    try:
        result = run_extraction(job_description)
    except Exception as e:
        result = {"error": str(e)}
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "input_jd": job_description})

