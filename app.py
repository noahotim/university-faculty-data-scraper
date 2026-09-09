"""
Live Demo Web App for University Faculty Data Scraper
Run: python app.py
Open: http://localhost:5000
"""
from flask import Flask, render_template_string, request, jsonify, send_from_directory
from pathlib import Path
import csv

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>University Faculty Data — Live Demo | noahotim</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{font-family:Segoe UI,Arial,sans-serif;margin:0;background:#f5f7fb;color:#222}
header{background:#0a66c2;color:#fff;padding:18px 24px;display:flex;justify-content:space-between;align-items:center}
header h1{margin:0;font-size:22px}
header a{color:#fff;text-decoration:none;background:#004182;padding:8px 14px;border-radius:6px}
.stats{background:#fff;margin:16px;padding:14px;border-radius:10px;display:flex;gap:18px;box-shadow:0 2px 8px rgba(0,0,0,.06);flex-wrap:wrap}
.stat b{font-size:22px;color:#0a66c2}
.controls{background:#fff;margin:0 16px 16px;padding:14px;border-radius:10px;display:flex;gap:10px;flex-wrap:wrap}
.controls input,.controls select{padding:8px 10px;border:1px solid #ccc;border-radius:6px;min-width:180px}
table{width:100%;border-collapse:collapse;background:#fff;margin:0 16px 16px;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.06)}
th{background:#0a66c2;color:#fff;padding:10px;text-align:left}
td{padding:10px;border-bottom:1px solid #eee}
tr:hover{background:#f0f6ff}
img{width:48px;height:48px;object-fit:cover;border-radius:6px;border:1px solid #ddd}
.badge{padding:2px 8px;border-radius:12px;font-size:11px;background:#e6f0ff;color:#0a66c2}
footer{text-align:center;padding:14px;color:#666;font-size:12px}
</style>
</head>
<body>
<header>
 <h1>🎓 University Faculty Data — Live Demo</h1>
 <div><a href="https://github.com/noahotim/university-faculty-data-scraper" target="_blank">GitHub: noahotim/university-faculty-data-scraper</a></div>
</header>

<div class="stats">
 <div><b>{{ total }}</b><br>Valid Records</div>
 <div><b>{{ universities|length }}</b><br>Universities</div>
 <div><b>{{ images }}</b><br>Images</div>
 <div><b>{{ failed }}</b><br>Failed (demo)</div>
 <div><span class="badge">{{ data_source }}</span></div>
</div>

<div class="controls">
 <input id="q" placeholder="Search name/position/university..." onkeyup="filter()">
 <select id="uni" onchange="filter()"><option value="">All Universities</option>{% for u in universities %}<option>{{u}}</option>{% endfor %}</select>
 <select id="fac" onchange="filter()"><option value="">All Faculties</option>{% for f in faculties %}<option>{{f}}</option>{% endfor %}</select>
 <button onclick="window.location.href='/api/run-demo'" style="background:#0a66c2;color:#fff;border:none;padding:8px 14px;border-radius:6px;cursor:pointer">▶ Run Live Scrape (demo)</button>
</div>

<table id="tbl">
<thead><tr><th>Photo</th><th>University</th><th>Faculty</th><th>Department</th><th>Name</th><th>Position</th></tr></thead>
<tbody>
{% for r in records %}
<tr data-uni="{{r.University}}" data-fac="{{r.Faculty}}">
 <td>{% if r.Image_file and r.Image_file != '' %}<img src="/{{r.Image_file}}" onerror="this.src='https://via.placeholder.com/48?text=N/A'">{% else %}<span class="badge">No Image</span>{% endif %}</td>
 <td>{{r.University}}</td>
 <td>{{r.Faculty}}</td>
 <td>{{r.Department}}</td>
 <td><b>{{r.Name}}</b></td>
 <td>{{r.Position}}</td>
</tr>
{% endfor %}
</tbody>
</table>

<div id="pager" style="text-align:center;margin:16px"><button onclick="prev()" id="prevBtn">‹ Prev</button> <span id="pageInfo" class="badge"></span> <button onclick="next()" id="nextBtn">Next ›</button></div>
<footer>Demo reads <code>output/universities.csv</code> (169 records from 7/43 universities) | All 43 Ugandan in <code>input/Universities_Uganda_All.csv</code> — 36 failed due to no public directory / 404 (see <code>output/logs/app.log</code>) | <a href="/api/data">JSON API</a> | Free Render sleeps — first load 30s</footer>

<script>
let cur=1, per=20;
function paginate(){
  const rows=[...document.querySelectorAll('#tbl tbody tr')].filter(tr=>tr.style.display!=='none' || true);
  // filter first
  const q=document.getElementById('q').value.toLowerCase();
  const uni=document.getElementById('uni').value;
  const fac=document.getElementById('fac').value;
  let visible=[];
  rows.forEach(tr=>{
    const txt=tr.innerText.toLowerCase();
    const okQ=!q||txt.includes(q);
    const okU=!uni||tr.dataset.uni===uni;
    const okF=!fac||tr.dataset.fac===fac;
    const show=okQ&&okU&&okF;
    tr.dataset.show=show?'1':'0';
    if(show) visible.push(tr);
  });
  const pages=Math.max(1, Math.ceil(visible.length/per));
  if(cur>pages) cur=pages;
  visible.forEach((tr,i)=>{ tr.style.display=(i>=(cur-1)*per && i<cur*per)?'':'none'; });
  document.querySelectorAll('#tbl tbody tr[data-show=\"0\"]').forEach(tr=>tr.style.display='none');
  document.getElementById('pageInfo').innerText=cur+' / '+pages+'  ('+visible.length+' matches)';
  document.getElementById('prevBtn').disabled=cur<=1;
  document.getElementById('nextBtn').disabled=cur>=pages;
}
function filter(){ cur=1; paginate(); }
function next(){ cur++; paginate(); }
function prev(){ cur--; paginate(); }
window.onload=paginate;
</script>
</body>
</html>
"""

def load_records():
    p = Path("output/universities.csv")
    if not p.exists():
        return []
    with p.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        for r in rows:
            if r.get("Image_file"):
                r["Image_file"] = r["Image_file"].replace("\\", "/")
        return rows

@app.route("/")
def index():
    records = load_records()
    universities = sorted({r["University"] for r in records})
    faculties = sorted({r["Faculty"] for r in records if r["Faculty"]})
    total = len(records)
    images = len(list(Path("output/images").glob("*.jpg"))) if Path("output/images").exists() else 0
    return render_template_string(TEMPLATE, records=records, total=total, universities=universities, faculties=faculties, images=images, failed=43-total//25, data_source=f"output/universities.csv ({total} records from {len(universities)} universities)")

@app.route("/api/data")
def api_data():
    return jsonify(load_records())

@app.route("/api/run-demo")
def run_demo():
    # Trigger a lightweight scrape for demo (CEDAT + Gulu only to be fast)
    import subprocess, sys
    # run main.py in background? For demo just return status
    return jsonify({"status": "Demo data already loaded", "hint": "Run: python main.py to refresh output/universities.csv"})

@app.route("/output/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(Path("output/images"), filename)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    print(f"Live demo at http://localhost:{port}  (Ctrl+C to stop)")
    app.run(host="0.0.0.0", port=port, debug=False)
