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

def get_db_connection():
    conn = sqlite3.connect('/tmp/horizon.db')
    conn.row_factory = sqlite3.Row
    return conn

# Helper function to initialize DB in /tmp for Vercel
def init_db_if_not_exists():
    if not os.path.exists('/tmp/horizon.db'):
        import shutil
        # If a pre-seeded DB exists in the project root, copy it
        if os.path.exists('horizon.db'):
            shutil.copyfile('horizon.db', '/tmp/horizon.db')
        else:
            # Fallback: create a new one from database.py logic (simplified here)
            # In production, relying on the copied file is safer.
             from database import init_db
             # Temporarily patch init_db to write to /tmp
             # ... or just ensure 'horizon.db' is committed to git.
             pass

init_db_if_not_exists()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/jobs")
async def get_jobs():
    conn = get_db_connection()
    jobs = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return [dict(job) for job in jobs]

@app.get("/api/prep")
async def get_prep():
    conn = get_db_connection()
    prep = conn.execute('SELECT * FROM prep_materials').fetchall()
    conn.close()
    return [dict(p) for p in prep]

@app.get("/api/companies")
async def get_companies():
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return [dict(c) for c in companies]

@app.get("/companies", response_class=HTMLResponse)
async def companies_page(request: Request):
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return templates.TemplateResponse("companies.html", {"request": request, "companies": [dict(c) for c in companies]})

@app.get("/practice", response_class=HTMLResponse)
async def practice_page(request: Request):
    conn = get_db_connection()
    problems = conn.execute('SELECT * FROM practice_problems').fetchall()
    conn.close()
    
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
    conn = get_db_connection()
    prep = conn.execute('SELECT * FROM prep_materials WHERE id = ?', (prep_id,)).fetchone()
    conn.close()
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
