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

# 1. Flatten Static Assets
# Copy style.css
src_css = os.path.join(BASE_DIR, 'static', 'css', 'style.css')
dst_css = os.path.join(DOCS_DIR, 'style.css')
if os.path.exists(src_css):
    shutil.copy(src_css, dst_css)

# Copy main.js (we will modify it later, but copy first as base)
src_js = os.path.join(BASE_DIR, 'static', 'js', 'main.js')
dst_js = os.path.join(DOCS_DIR, 'main.js')
if os.path.exists(src_js):
    with open(src_js, 'r') as f:
        js_content = f.read()

# Initialize DB connection (In-Memory for seed data)
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
from database import init_db
init_db(conn)

# Setup Jinja2
env = Environment(loader=FileSystemLoader('templates'))

# Helper to fix paths in HTML
def flatten_paths(html_content):
    # CSS
    html_content = html_content.replace('href="/static/css/style.css"', 'href="style.css"')
    html_content = html_content.replace('href="static/css/style.css"', 'href="style.css"')
    html_content = html_content.replace('/static/css/style.css', 'style.css')
    
    # JS
    html_content = html_content.replace('src="/static/js/main.js"', 'src="main.js"')
    html_content = html_content.replace('src="static/js/main.js"', 'src="main.js"')
    html_content = html_content.replace('/static/js/main.js', 'main.js')
    
    # Nav Links
    html_content = html_content.replace('href="/companies"', 'href="companies.html"')
    html_content = html_content.replace('href="/practice"', 'href="practice.html"')
    html_content = html_content.replace('href="/"', 'href="index.html"')
    
    return html_content

# 2. Render HTML Pages
# Index
template = env.get_template('index.html')
with open(os.path.join(DOCS_DIR, 'index.html'), 'w') as f:
    f.write(flatten_paths(template.render()))

# Companies
companies = conn.execute('SELECT * FROM companies').fetchall()
data_companies = [dict(c) for c in companies]
template = env.get_template('companies.html')
with open(os.path.join(DOCS_DIR, 'companies.html'), 'w') as f:
    f.write(flatten_paths(template.render(companies=data_companies)))

# Practice
problems = conn.execute('SELECT * FROM practice_problems').fetchall()
grouped = {}
for p in problems:
    p_dict = dict(p)
    topic = p_dict['topic']
    if topic not in grouped:
        grouped[topic] = []
    grouped[topic].append(p_dict)
template = env.get_template('practice.html')
with open(os.path.join(DOCS_DIR, 'practice.html'), 'w') as f:
    f.write(flatten_paths(template.render(grouped_problems=grouped)))

# Prep Details
preps = conn.execute('SELECT * FROM prep_materials').fetchall()
data_prep = [dict(p) for p in preps]
for p in data_prep:
    p['roadmap'] = json.loads(p['roadmap'])
    p['questions'] = json.loads(p['questions'])
    template = env.get_template('prep_detail.html')
    with open(os.path.join(DOCS_DIR, f"prep_{p['id']}.html"), 'w') as f:
        f.write(flatten_paths(template.render(prep=p)))

# 3. Create JSON Data Files (Flat)
conn_jobs = conn.execute('SELECT * FROM jobs').fetchall()
data_jobs = [dict(j) for j in conn_jobs]

with open(os.path.join(DOCS_DIR, 'jobs.json'), 'w') as f:
    json.dump(data_jobs, f)

with open(os.path.join(DOCS_DIR, 'prep.json'), 'w') as f:
    # We re-fetch prep to get raw JSON strings if needed, or use cleaned data_prep
    # data_prep has parsed JSON, we might want consistent JSON for JS
    # Let's just dump data_prep but ensure keys match what JS expects
    json.dump(data_prep, f) 

# 4. Fix main.js to use flat paths
# Replace API endpoints with flat JSON files
js_content = js_content.replace('/api/jobs', 'jobs.json')
js_content = js_content.replace('api/jobs.json', 'jobs.json') # in case repeated
js_content = js_content.replace('/api/prep', 'prep.json')
js_content = js_content.replace('api/prep.json', 'prep.json')

# Replace dynamic links with flat HTML links
js_content = js_content.replace('`/prep/${item.id}`', '`prep_${item.id}.html`')
js_content = js_content.replace("window.location.href = `/prep/${item.id}`", "window.location.href = `prep_${item.id}.html`")
js_content = js_content.replace('href="/companies"', 'href="companies.html"')
js_content = js_content.replace('href="/practice"', 'href="practice.html"')

# Start Learning button in JS often has /prep/id
js_content = js_content.replace('href="/prep/${item.id}"', 'href="prep_${item.id}.html"')

with open(dst_js, 'w') as f:
    f.write(js_content)

print(f"Flat static site built in {DOCS_DIR}")
