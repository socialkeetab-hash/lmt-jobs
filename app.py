from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import os
import json

app = FastAPI()

# Mount static files (ensure directories exist)
os.makedirs("static/css", exist_ok=True)
os.makedirs("static/js", exist_ok=True)
os.makedirs("static/images", exist_ok=True)
os.makedirs("templates", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global In-Memory Database Connection
db_connection = sqlite3.connect(":memory:", check_same_thread=False)
db_connection.row_factory = sqlite3.Row

# Initialize DB with Seed Data
from database import init_db
init_db(db_connection)

def get_db_connection():
    # Return the shared in-memory connection
    return db_connection

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/jobs")
async def get_jobs():
    jobs = db_connection.execute('SELECT * FROM jobs').fetchall()
    # No close() necessary for shared memory connection
    return [dict(job) for job in jobs]

@app.get("/api/prep")
async def get_prep():
    prep = db_connection.execute('SELECT * FROM prep_materials').fetchall()
    # No close()
    return [dict(p) for p in prep]

@app.get("/api/companies")
async def get_companies():
    companies = db_connection.execute('SELECT * FROM companies').fetchall()
    # No close()
    return [dict(c) for c in companies]

@app.get("/companies", response_class=HTMLResponse)
async def companies_page(request: Request):
    companies = db_connection.execute('SELECT * FROM companies').fetchall()
    # No close()
    return templates.TemplateResponse("companies.html", {"request": request, "companies": [dict(c) for c in companies]})

@app.get("/practice", response_class=HTMLResponse)
async def practice_page(request: Request):
    problems = db_connection.execute('SELECT * FROM practice_problems').fetchall()
    # No close()
    
    # Group problems by topic
    grouped = {}
    for p in problems:
        p_dict = dict(p)
        topic = p_dict['topic']
        if topic not in grouped:
            grouped[topic] = []
        grouped[topic].append(p_dict)
        
    return templates.TemplateResponse("practice.html", {"request": request, "grouped_problems": grouped})

@app.get("/prep/{prep_id}", response_class=HTMLResponse)
async def prep_detail(request: Request, prep_id: int):
    prep = db_connection.execute('SELECT * FROM prep_materials WHERE id = ?', (prep_id,)).fetchone()
    # No close()
    if prep:
        p_dict = dict(prep)
        # Parse JSON fields
        p_dict['roadmap'] = json.loads(p_dict['roadmap'])
        p_dict['questions'] = json.loads(p_dict['questions'])
        return templates.TemplateResponse("prep_detail.html", {"request": request, "prep": p_dict})
    return HTMLResponse(content="Preparation material not found", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
