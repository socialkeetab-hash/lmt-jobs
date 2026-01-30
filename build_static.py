import os
import json
import shutil
import sqlite3
from jinja2 import Environment, FileSystemLoader

# Setup directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
if os.path.exists(DOCS_DIR):
    shutil.rmtree(DOCS_DIR)
os.makedirs(DOCS_DIR)

# Copy static assets
shutil.copytree(os.path.join(BASE_DIR, 'static'), os.path.join(DOCS_DIR, 'static'))

# Initialize DB connection (In-Memory for seed data)
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
from database import init_db
init_db(conn)

# Setup Jinja2
env = Environment(loader=FileSystemLoader('templates'))

# 1. Render Index (Home)
# Note: Index mostly uses JS to fetch data, but we need to ensure main.js works.
# main.js fetches /api/jobs. We will generate that JSON file.
template = env.get_template('index.html')
with open(os.path.join(DOCS_DIR, 'index.html'), 'w') as f:
    f.write(template.render())

# 2. Render Companies
companies = conn.execute('SELECT * FROM companies').fetchall()
data_companies = [dict(c) for c in companies]
template = env.get_template('companies.html')
rendered = template.render(companies=data_companies)
# Fix links
rendered = rendered.replace('href="/"', 'href="index.html"')
with open(os.path.join(DOCS_DIR, 'companies.html'), 'w') as f:
    f.write(rendered)

# 3. Render Practice
problems = conn.execute('SELECT * FROM practice_problems').fetchall()
grouped = {}
for p in problems:
    p_dict = dict(p)
    topic = p_dict['topic']
    if topic not in grouped:
        grouped[topic] = []
    grouped[topic].append(p_dict)

template = env.get_template('practice.html')
rendered = template.render(grouped_problems=grouped)
rendered = rendered.replace('href="/"', 'href="index.html"')
with open(os.path.join(DOCS_DIR, 'practice.html'), 'w') as f:
    f.write(rendered)

# 4. Render Prep Details
preps = conn.execute('SELECT * FROM prep_materials').fetchall()
data_prep = [dict(p) for p in preps]

# We also need to fix main.js to fetch from 'data/...' instead of '/api/...'
# Let's create JSON data files
os.makedirs(os.path.join(DOCS_DIR, 'api'), exist_ok=True)
conn_jobs = conn.execute('SELECT * FROM jobs').fetchall()
data_jobs = [dict(j) for j in conn_jobs]

with open(os.path.join(DOCS_DIR, 'api', 'jobs.json'), 'w') as f:
    json.dump(data_jobs, f)

with open(os.path.join(DOCS_DIR, 'api', 'prep.json'), 'w') as f:
    json.dump(data_prep, f)

# Render Prep Detail Pages
for p in data_prep:
    p['roadmap'] = json.loads(p['roadmap'])
    p['questions'] = json.loads(p['questions'])
    template = env.get_template('prep_detail.html')
    rendered = template.render(prep=p)
    rendered = rendered.replace('href="/"', 'href="index.html"')
    with open(os.path.join(DOCS_DIR, f"prep_{p['id']}.html"), 'w') as f:
        f.write(rendered)

# 5. Fix Javascript (main.js)
# We need a version of main.js that fetches from local JSON files and links to .html
js_path = os.path.join(DOCS_DIR, 'static/js/main.js')
with open(js_path, 'r') as f:
    js_content = f.read()

# Replace API endpoints with JSON files
js_content = js_content.replace('/api/jobs', 'api/jobs.json')
js_content = js_content.replace('/api/prep', 'api/prep.json')

# Replace dynamic links with static links
# Regex would be safer but simple replace works for this known codebase
js_content = js_content.replace('`/prep/${item.id}`', '`prep_${item.id}.html`')
js_content = js_content.replace("window.location.href = `/prep/${item.id}`", "window.location.href = `prep_${item.id}.html`")
js_content = js_content.replace('href="/companies"', 'href="companies.html"')
js_content = js_content.replace('href="/practice"', 'href="practice.html"')

with open(js_path, 'w') as f:
    f.write(js_content)

# 6. Fix Navbar links in index.html (already written, need to overwrite or process before write)
# Let's simple re-read all HTMLs and fix common nav links
for filename in os.listdir(DOCS_DIR):
    if filename.endswith('.html'):
        path = os.path.join(DOCS_DIR, filename)
        with open(path, 'r') as f:
            content = f.read()
        
        content = content.replace('href="/companies"', 'href="companies.html"')
        content = content.replace('href="/practice"', 'href="practice.html"')
        content = content.replace('href="/"', 'href="index.html"')
        
        # fix CSS/JS paths to be relative (remove leading slash)
        content = content.replace('href="/static/css/style.css"', 'href="static/css/style.css"')
        content = content.replace('src="/static/js/main.js"', 'src="static/js/main.js"')

        with open(path, 'w') as f:
            f.write(content)

print(f"Static site built in {DOCS_DIR}")
