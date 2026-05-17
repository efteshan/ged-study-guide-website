#!/usr/bin/env python3
"""Build script: Parses content_prd.md and generates index.html"""
import re, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def bold_to_strong(text):
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

CONTENT_PRD = os.path.join(SCRIPT_DIR, '..', '..', '.gemini', 'antigravity', 'brain',
    'f1f65c89-93d3-4722-b1a6-60b30db5fcae', 'content_prd.md')
if not os.path.exists(CONTENT_PRD):
    CONTENT_PRD = r'C:\Users\User\.gemini\antigravity\brain\f1f65c89-93d3-4722-b1a6-60b30db5fcae\content_prd.md'

PDF_TEXT = os.path.join(SCRIPT_DIR, 'pdf_text.txt')

CATEGORIES = {
    "Algebra & Equations": [1,2,3,4,9,10,30,38,39,40,41,42,43,47],
    "Geometry & Measurement": [13,14,15,16,17,18],
    "Graphs, Slope & Functions": [5,6,7,8,26,27,28,29,46],
    "Data, Stats & Probability": [25,32,33,34,35],
    "Numbers & Percents": [11,12,19,20,21,22,23,24,31,36,37,44,45,48,49,50],
}
CAT_IDS = {
    "Algebra & Equations": "algebra",
    "Geometry & Measurement": "geometry",
    "Graphs, Slope & Functions": "graphs",
    "Data, Stats & Probability": "data",
    "Numbers & Percents": "numbers",
}

def parse_questions(md_text):
    parts = re.split(r'^## Question ', md_text, flags=re.MULTILINE)
    questions = {}
    for part in parts[1:]:
        m = re.match(r'(\d+):\s*(.*?)$', part, re.MULTILINE)
        if m:
            qnum = int(m.group(1))
            qtitle = m.group(2).strip()
            body = part[m.end():]
            questions[qnum] = {"num": qnum, "title": qtitle, "body": body}
    return questions

def md_to_html_body(body):
    lines = body.strip().split('\n')
    html_parts = []
    i = 0
    practice_count = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('### 💡 Core Concept'):
            i += 1
            concept_lines = []
            while i < len(lines) and not lines[i].strip().startswith('### '):
                if lines[i].strip():
                    concept_lines.append(lines[i].strip())
                i += 1
            html_parts.append(bold_to_strong(f'<div class="callout tip"><div class="callout-title">💡 CORE CONCEPT</div><p>{" ".join(concept_lines)}</p></div>'))
            continue
        if line.startswith('### 📝 Step-by-Step Solution'):
            i += 1
            html_parts.append('<h3>📝 Step-by-Step Solution</h3>')
            while i < len(lines) and not lines[i].strip().startswith('### '):
                sline = lines[i].strip()
                if not sline:
                    i += 1
                    continue
                if sline.startswith('* **Step') or sline.startswith('* **Final Answer'):
                    html_parts.append(bold_to_strong(f'<p class="step-item">{sline[2:]}</p>'))
                elif sline.startswith('$$') and sline.endswith('$$'):
                    html_parts.append(f'<p class="math-display">{sline}</p>')
                else:
                    html_parts.append(bold_to_strong(f'<p>{sline}</p>'))
                i += 1
            continue
        if line.startswith('### 🧠 GED Practice Problems'):
            i += 1
            practice_count = 0
            continue
        if line.startswith('#### Practice'):
            practice_count += 1
            i += 1
            q_text = []
            options = []
            answer_text = ""
            while i < len(lines):
                pline = lines[i].strip()
                if not pline:
                    i += 1
                    continue
                if pline.startswith('#### Practice') or pline.startswith('### ') or pline.startswith('## ') or pline == '---':
                    break
                if pline.startswith('* **A)') or pline.startswith('* **B)') or pline.startswith('* **C)') or pline.startswith('* **D)'):
                    options.append(pline[2:])
                elif pline.startswith('* **Answer:'):
                    answer_text = pline[2:]
                else:
                    q_text.append(pline)
                i += 1
            opts_html = "".join(f'<li>{bold_to_strong(o)}</li>' for o in options)
            html_parts.append(bold_to_strong(f'''<div class="practice-box">
<div class="practice-header">🧠 Practice {practice_count}</div>
<div class="practice-body">
<div class="practice-question"><p>{" ".join(q_text)}</p><ul class="content-list">{opts_html}</ul></div>
<button class="show-answer-btn" onclick="this.style.display='none'; this.nextElementSibling.classList.add('show');">Show Answer</button>
<div class="practice-answer"><p>{answer_text}</p></div>
</div></div>'''))
            continue
        if line == '---' or not line:
            i += 1
            continue
        i += 1
    return '\n'.join(html_parts)

def build_overview():
    with open(PDF_TEXT, 'r', encoding='utf-8') as f:
        raw = f.read()
    lines = [l.strip() for l in raw.strip().split('\n') if l.strip()]
    items = []
    for l in lines:
        m = re.match(r'^(\d+)\.\s*(.*)', l)
        if m:
            items.append(f'<li><span class="overview-num">{m.group(1)}.</span> {m.group(2)}</li>')
    return '\n'.join(items)

def build_html(questions):
    overview_items = build_overview()

    # Build category tabs
    cat_btns = ['<button class="cat-btn active" data-cat="overview">Question Overview</button>']
    cat_panes = []

    # Overview pane
    cat_panes.append(f'''<div id="cat-overview" class="cat-pane active">
<div class="container">
<div class="overview-section">
<div class="section-header"><span class="section-number">OVERVIEW</span><h2>50 Most Important GED Math Questions</h2></div>
<ol class="overview-list">{overview_items}</ol>
</div></div></div>''')

    for cat_name, cat_id in CAT_IDS.items():
        q_nums = CATEGORIES[cat_name]
        cat_btns.append(f'<button class="cat-btn" data-cat="{cat_id}">{cat_name}</button>')
        sub_btns = []
        sub_panes = []
        for idx, qn in enumerate(q_nums):
            q = questions.get(qn)
            if not q: continue
            active = ' active' if idx == 0 else ''
            sub_btns.append(f'<button class="tab-btn{active}" data-target="{cat_id}-q{qn}">Q{qn}</button>')
            body_html = md_to_html_body(q["body"])
            title_html = bold_to_strong(q["title"])
            sub_panes.append(f'''<div class="section tab-pane{active}" id="{cat_id}-q{qn}">
<div class="section-header"><span class="section-number">QUESTION {qn}</span><h2>{title_html}</h2><button class="formula-btn" onclick="document.getElementById('formulaModal').classList.add('show')" aria-label="Formula Sheet">📐</button></div>
{body_html}
</div>''')
        tabs_nav = '\n'.join(sub_btns)
        panes = '\n'.join(sub_panes)
        cat_panes.append(f'''<div id="cat-{cat_id}" class="cat-pane">
<div class="container">
<div class="tabs-wrapper" id="wrapper-{cat_id}">
<button class="scroll-btn" onclick="this.nextElementSibling.scrollBy({{left:-200,behavior:'smooth'}})">&lsaquo;</button>
<nav class="tabs-nav">{tabs_nav}</nav>
<button class="scroll-btn" onclick="this.previousElementSibling.scrollBy({{left:200,behavior:'smooth'}})">&rsaquo;</button>
</div>
{panes}
</div></div>''')

    cat_btns_html = '\n'.join(cat_btns)
    cat_panes_html = '\n'.join(cat_panes)

    return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GED Math Study Guide - 50 Important Questions</title>
<meta name="description" content="Master the 50 most important GED Math questions with step-by-step solutions, explanations, and interactive practice problems.">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body,{{delimiters:[{{left:'$$',right:'$$',display:true}},{{left:'$',right:'$',display:false}}],throwOnError:false}});"></script>
<style>
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{--transition-speed:0.3s}}
[data-theme="dark"]{{
--bg-primary:#000;--bg-secondary:#0a0a0a;--bg-card:#111;--bg-code:#1a1a1a;
--bg-tip:rgba(255,255,255,0.04);--bg-important:rgba(255,255,255,0.04);--bg-note:rgba(255,255,255,0.04);
--text-primary:#fff;--text-secondary:#a0a0a0;--text-muted:#666;
--accent:#fff;--border:#222;--border-light:#1a1a1a;
--tip-border:#3b82f6;--important-border:#f59e0b;--note-border:#8b5cf6;--caution-border:#ef4444;
--scrollbar-thumb:#333;--scrollbar-track:#111;--toggle-bg:#222;--toggle-knob:#fff;
--shadow:0 1px 3px rgba(0,0,0,0.5)}}
[data-theme="light"]{{
--bg-primary:#fff;--bg-secondary:#f8f8f8;--bg-card:#fff;--bg-code:#f5f5f5;
--bg-tip:rgba(0,0,0,0.03);--bg-important:rgba(0,0,0,0.03);--bg-note:rgba(0,0,0,0.03);
--text-primary:#000;--text-secondary:#555;--text-muted:#999;
--accent:#000;--border:#e0e0e0;--border-light:#eee;
--tip-border:#2563eb;--important-border:#d97706;--note-border:#7c3aed;--caution-border:#dc2626;
--scrollbar-thumb:#ccc;--scrollbar-track:#f0f0f0;--toggle-bg:#e0e0e0;--toggle-knob:#000;
--shadow:0 1px 3px rgba(0,0,0,0.1)}}
body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg-primary);color:var(--text-secondary);line-height:1.7;-webkit-font-smoothing:antialiased;transition:background var(--transition-speed),color var(--transition-speed)}}
::-webkit-scrollbar{{width:6px}}::-webkit-scrollbar-track{{background:var(--scrollbar-track)}}::-webkit-scrollbar-thumb{{background:var(--scrollbar-thumb);border-radius:3px}}
/* === TOP NAV (Tier 1) === */
.top-level-nav{{position:sticky;top:0;z-index:200;display:flex;align-items:center;justify-content:space-between;padding:10px 24px;background:var(--bg-primary);border-bottom:2px solid var(--border);transition:background var(--transition-speed),border var(--transition-speed)}}
.top-nav-left{{display:flex;align-items:center;gap:10px}}
.master-tab{{background:transparent;border:2px solid var(--accent);color:var(--text-primary);font-size:0.9rem;font-weight:700;padding:8px 20px;border-radius:8px;cursor:default;font-family:inherit;box-shadow:var(--shadow)}}
.top-nav-right{{display:flex;align-items:center;gap:12px}}
.theme-toggle{{width:52px;height:28px;border-radius:14px;background:var(--toggle-bg);border:none;cursor:pointer;position:relative;transition:background var(--transition-speed);flex-shrink:0;overflow:hidden}}
.theme-toggle::after{{content:'';position:absolute;width:22px;height:22px;border-radius:50%;background:var(--toggle-knob);top:3px;left:3px;transition:transform var(--transition-speed);z-index:2}}
[data-theme="light"] .theme-toggle::after{{transform:translateX(24px)}}
.toggle-icons{{position:absolute;width:100%;display:flex;justify-content:space-between;align-items:center;padding:0 6px;font-size:0.55rem;top:50%;transform:translateY(-50%);pointer-events:none;z-index:1}}
/* === CATEGORY NAV (Tier 2) === */
.cat-nav-wrapper{{position:sticky;top:50px;z-index:190;background:var(--bg-primary);border-bottom:1px solid var(--border);transition:background var(--transition-speed),border var(--transition-speed);display:flex;align-items:center;overflow:hidden}}
.cat-nav{{display:flex;overflow-x:auto;white-space:nowrap;scrollbar-width:none;-webkit-overflow-scrolling:touch;flex:1;padding:0 16px}}
.cat-nav::-webkit-scrollbar{{display:none}}
.cat-btn{{padding:10px 18px;font-size:0.8rem;font-weight:600;color:var(--text-muted);background:transparent;border:none;border-bottom:2px solid transparent;cursor:pointer;transition:all var(--transition-speed);font-family:inherit;white-space:nowrap}}
.cat-btn:hover{{color:var(--text-secondary);background:var(--bg-code)}}
.cat-btn.active{{color:var(--text-primary);border-bottom-color:var(--accent)}}
.cat-scroll-btn{{width:32px;height:100%;display:flex;align-items:center;justify-content:center;background:var(--bg-primary);border:none;color:var(--text-muted);cursor:pointer;font-size:1rem;flex-shrink:0;transition:color var(--transition-speed)}}
.cat-scroll-btn:hover{{color:var(--text-primary)}}
/* === CATEGORY PANES === */
.cat-pane{{display:none}}.cat-pane.active{{display:block;animation:fadeIn 0.3s ease-in-out}}
.container{{max-width:780px;margin:0 auto;padding:40px 24px 80px}}
/* === QUESTION TABS (Tier 3) === */
.tabs-wrapper{{display:flex;align-items:center;margin-bottom:32px;border-bottom:1px solid var(--border);position:relative}}
.tabs-nav{{display:flex;overflow-x:auto;white-space:nowrap;scrollbar-width:none;-webkit-overflow-scrolling:touch;flex:1}}
.tabs-nav::-webkit-scrollbar{{display:none}}
.tab-btn{{padding:12px 20px;font-size:0.9rem;font-weight:600;color:var(--text-muted);background:transparent;border:none;border-bottom:2px solid transparent;cursor:pointer;transition:all var(--transition-speed);font-family:inherit;white-space:nowrap}}
.tab-btn:hover{{color:var(--text-secondary);background:var(--bg-code)}}
.tab-btn.active{{color:var(--text-primary);border-bottom:2px solid var(--accent)}}
.scroll-btn{{width:36px;height:36px;display:flex;align-items:center;justify-content:center;background:transparent;border:none;color:var(--text-muted);cursor:pointer;font-size:1.2rem;flex-shrink:0;transition:color var(--transition-speed)}}
.scroll-btn:hover{{color:var(--text-primary)}}
/* === SECTIONS === */
.section{{margin-bottom:56px}}.tab-pane{{display:none}}.tab-pane.active{{display:block;animation:fadeIn 0.3s ease-in-out}}
.section-header{{display:flex;align-items:center;gap:12px;padding-bottom:12px;border-bottom:1px solid var(--border);margin-bottom:20px;flex-wrap:wrap}}
.section-number{{font-size:0.75rem;font-weight:700;color:var(--text-muted);background:var(--bg-code);border:1px solid var(--border);padding:4px 10px;border-radius:4px;text-transform:uppercase;letter-spacing:0.05em;white-space:nowrap}}
.section-header h2{{font-size:1.4rem;font-weight:700;letter-spacing:-0.02em;color:var(--text-primary);flex:1}}
.formula-btn{{background:transparent;border:1px solid var(--border);border-radius:6px;padding:4px 10px;cursor:pointer;font-size:1rem;color:var(--text-muted);transition:all var(--transition-speed);flex-shrink:0}}
.formula-btn:hover{{color:var(--text-primary);border-color:var(--text-muted);background:var(--bg-code)}}
h3{{font-size:1.1rem;font-weight:600;letter-spacing:-0.01em;margin:28px 0 12px;color:var(--text-primary)}}
h4{{font-size:1rem;font-weight:600;margin:20px 0 10px;color:var(--text-primary)}}
p{{margin-bottom:12px}}strong{{font-weight:600;color:var(--text-primary)}}
.callout{{border-left:3px solid var(--tip-border);border-radius:0 8px 8px 0;padding:16px 20px;margin:20px 0;font-size:0.9rem;background:var(--bg-tip)}}
.callout.tip{{border-left-color:var(--tip-border)}}
.callout-title{{font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.05em;display:flex;align-items:center;gap:6px;margin-bottom:8px;color:var(--tip-border)}}
.step-item{{margin:8px 0;padding-left:8px}}
.math-display{{text-align:center;margin:8px 0 16px;font-size:1.1rem}}
.content-list{{padding-left:24px;margin:8px 0 14px;color:var(--text-secondary)}}.content-list li{{margin-bottom:4px;list-style:none}}
.practice-box{{margin-top:28px;border:1px solid var(--note-border);border-radius:8px;overflow:hidden;background:var(--bg-card)}}
.practice-header{{background:var(--bg-secondary);padding:12px 16px;font-weight:700;font-size:1rem;border-bottom:1px solid var(--border);color:var(--note-border)}}
.practice-body{{padding:20px}}.practice-question{{font-size:0.95rem;margin-bottom:15px;line-height:1.5}}.practice-question p{{margin-bottom:10px}}
.show-answer-btn{{background:var(--note-border);color:#fff;border:none;padding:10px 18px;border-radius:6px;font-weight:600;cursor:pointer;font-family:inherit;font-size:0.9rem;transition:opacity var(--transition-speed)}}
.show-answer-btn:hover{{opacity:0.85}}
.practice-answer{{display:none;margin-top:20px;padding-top:15px;border-top:1px dashed var(--border)}}.practice-answer.show{{display:block}}
/* === OVERVIEW === */
.overview-list{{list-style:none;padding:0;counter-reset:none}}
.overview-list li{{padding:12px 16px;border-bottom:1px solid var(--border);font-size:0.95rem;color:var(--text-secondary);display:flex;gap:10px;transition:background var(--transition-speed)}}
.overview-list li:hover{{background:var(--bg-code)}}
.overview-num{{font-weight:700;color:var(--text-primary);min-width:28px}}
/* === FORMULA MODAL === */
.formula-modal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;z-index:9999;background:rgba(0,0,0,0.85);align-items:center;justify-content:center;padding:20px}}
.formula-modal.show{{display:flex}}
.formula-modal-inner{{position:relative;max-width:700px;max-height:90vh;width:100%}}
.formula-modal-inner img{{width:100%;height:auto;border-radius:8px;display:block;max-height:85vh;object-fit:contain}}
.formula-close{{position:absolute;top:-14px;right:-14px;width:36px;height:36px;border-radius:50%;background:#ef4444;border:none;color:#fff;font-size:1.2rem;font-weight:700;cursor:pointer;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,0.4);transition:transform 0.2s}}
.formula-close:hover{{transform:scale(1.1)}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
@media(max-width:640px){{
.top-level-nav{{padding:8px 12px}}
.master-tab{{font-size:0.8rem;padding:6px 14px}}
.cat-btn{{font-size:0.72rem;padding:8px 12px}}
.cat-scroll-btn{{display:none}}
.container{{padding:24px 16px 60px}}
.section{{margin-bottom:40px}}
.section-header{{flex-direction:row;gap:8px}}
.section-header h2{{font-size:1.15rem}}
.callout{{padding:14px 16px}}
.scroll-btn{{display:none}}
.tab-btn{{padding:10px 14px;font-size:0.8rem}}
.formula-modal-inner{{max-width:95vw}}
.formula-close{{top:-10px;right:-10px;width:30px;height:30px;font-size:1rem}}
}}
@media(max-width:380px){{
.master-tab{{font-size:0.72rem;padding:5px 10px}}
.cat-btn{{font-size:0.65rem;padding:6px 8px}}
}}
</style>
</head>
<body>
<!-- Tier 1: Top Nav -->
<div class="top-level-nav">
<div class="top-nav-left"><button class="master-tab">Math</button></div>
<div class="top-nav-right"><button class="theme-toggle" id="themeToggle" aria-label="Toggle theme"><span class="toggle-icons">🌙 ☀️</span></button></div>
</div>
<!-- Tier 2: Category Nav -->
<div class="cat-nav-wrapper">
<button class="cat-scroll-btn" onclick="document.getElementById('catNav').scrollBy({{left:-200,behavior:'smooth'}})">&lsaquo;</button>
<nav class="cat-nav" id="catNav">{cat_btns_html}</nav>
<button class="cat-scroll-btn" onclick="document.getElementById('catNav').scrollBy({{left:200,behavior:'smooth'}})">&rsaquo;</button>
</div>
<!-- Category Panes -->
{cat_panes_html}
<!-- Formula Modal -->
<div class="formula-modal" id="formulaModal">
<div class="formula-modal-inner">
<button class="formula-close" onclick="document.getElementById('formulaModal').classList.remove('show')">&times;</button>
<img src="math_formula_sheet_page-0001.jpg" alt="GED Math Formula Sheet">
</div>
</div>
<script>
(function(){{
/* Theme Toggle */
var html=document.documentElement;
var toggle=document.getElementById('themeToggle');
var saved=localStorage.getItem('theme')||'dark';
html.setAttribute('data-theme',saved);
toggle.addEventListener('click',function(){{
var c=html.getAttribute('data-theme');
var n=c==='dark'?'light':'dark';
html.setAttribute('data-theme',n);
localStorage.setItem('theme',n);
}});
/* Category Tab Switching */
var catBtns=document.querySelectorAll('.cat-btn');
var catPanes=document.querySelectorAll('.cat-pane');
catBtns.forEach(function(btn){{
btn.addEventListener('click',function(){{
catBtns.forEach(function(b){{b.classList.remove('active')}});
catPanes.forEach(function(p){{p.classList.remove('active')}});
btn.classList.add('active');
var t=document.getElementById('cat-'+btn.getAttribute('data-cat'));
if(t)t.classList.add('active');
window.scrollTo({{top:0,behavior:'smooth'}});
}});
}});
/* Sub-Tab Switching (scoped) */
function initTabs(wid){{
var w=document.getElementById(wid);
if(!w)return;
var c=w.closest('.container');
if(!c)return;
var bs=w.querySelectorAll('.tab-btn');
var ps=c.querySelectorAll('.tab-pane');
bs.forEach(function(b){{
b.addEventListener('click',function(){{
bs.forEach(function(x){{x.classList.remove('active')}});
ps.forEach(function(x){{x.classList.remove('active')}});
b.classList.add('active');
var t=document.getElementById(b.getAttribute('data-target'));
if(t)t.classList.add('active');
window.scrollTo({{top:0,behavior:'smooth'}});
}});
}});
}}
initTabs('wrapper-algebra');
initTabs('wrapper-geometry');
initTabs('wrapper-graphs');
initTabs('wrapper-data');
initTabs('wrapper-numbers');
/* Modal backdrop close */
var modal=document.getElementById('formulaModal');
modal.addEventListener('click',function(e){{
if(e.target===modal)modal.classList.remove('show');
}});
}})();
</script>
</body>
</html>'''

if __name__ == '__main__':
    with open(CONTENT_PRD, 'r', encoding='utf-8') as f:
        md_text = f.read()
    questions = parse_questions(md_text)
    print(f"Parsed {len(questions)} questions")
    for cat, nums in CATEGORIES.items():
        missing = [n for n in nums if n not in questions]
        if missing:
            print(f"WARNING: {cat} missing questions: {missing}")
    html = build_html(questions)
    out_path = os.path.join(SCRIPT_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated index.html ({len(html)} bytes)")
