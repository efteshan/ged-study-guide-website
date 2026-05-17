#!/usr/bin/env python3
"""Build script: Parses content_prd.md and generates index.html"""
import re, os

def bold_to_strong(text):
    """Convert markdown **bold** to HTML <strong> tags."""
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

CONTENT_PRD = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '.gemini', 'antigravity', 'brain',
    'f1f65c89-93d3-4722-b1a6-60b30db5fcae', 'content_prd.md')

# If relative path fails, use absolute
if not os.path.exists(CONTENT_PRD):
    CONTENT_PRD = r'C:\Users\User\.gemini\antigravity\brain\f1f65c89-93d3-4722-b1a6-60b30db5fcae\content_prd.md'

# Question-to-category mapping
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
    """Parse content_prd.md into individual question dicts."""
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
    """Convert question markdown body to HTML components."""
    lines = body.strip().split('\n')
    html_parts = []
    i = 0
    in_practice_box = False
    practice_count = 0

    while i < len(lines):
        line = lines[i].strip()

        # Core Concept heading
        if line.startswith('### 💡 Core Concept'):
            i += 1
            concept_lines = []
            while i < len(lines) and not lines[i].strip().startswith('### '):
                if lines[i].strip():
                    concept_lines.append(lines[i].strip())
                i += 1
            html_parts.append(bold_to_strong(f'<div class="callout tip"><div class="callout-title">💡 CORE CONCEPT</div><p>{" ".join(concept_lines)}</p></div>'))
            continue

        # Step-by-Step Solution heading
        if line.startswith('### 📝 Step-by-Step Solution'):
            i += 1
            html_parts.append('<h3>📝 Step-by-Step Solution</h3>')
            # Collect until next ### heading
            while i < len(lines) and not lines[i].strip().startswith('### '):
                sline = lines[i].strip()
                if not sline:
                    i += 1
                    continue
                # Step items
                if sline.startswith('* **Step') or sline.startswith('* **Final Answer'):
                    html_parts.append(bold_to_strong(f'<p class="step-item">{sline[2:]}</p>'))
                # Display math
                elif sline.startswith('$$') and sline.endswith('$$'):
                    html_parts.append(f'<p class="math-display">{sline}</p>')
                # Regular paragraph
                else:
                    html_parts.append(bold_to_strong(f'<p>{sline}</p>'))
                i += 1
            continue

        # GED Practice Problems heading
        if line.startswith('### 🧠 GED Practice Problems'):
            i += 1
            practice_count = 0
            continue

        # Practice sub-heading
        if line.startswith('#### Practice'):
            practice_count += 1
            i += 1
            # Collect question text
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

        # Skip horizontal rules and empty lines
        if line == '---' or not line:
            i += 1
            continue

        i += 1

    return '\n'.join(html_parts)

def build_html(questions):
    """Build the complete index.html."""
    # Build tab panes for each category
    main_tabs_html = []
    for cat_name, cat_id in CAT_IDS.items():
        q_nums = CATEGORIES[cat_name]
        # Sub-tab buttons
        sub_btns = []
        sub_panes = []
        for idx, qn in enumerate(q_nums):
            q = questions.get(qn)
            if not q:
                continue
            active = ' active' if idx == 0 else ''
            short = f'Q{qn}'
            sub_btns.append(f'<button class="tab-btn{active}" data-target="{cat_id}-q{qn}">{short}</button>')
            body_html = md_to_html_body(q["body"])
            title_html = bold_to_strong(q["title"])
            sub_panes.append(f'''<div class="section tab-pane{active}" id="{cat_id}-q{qn}">
<div class="section-header"><span class="section-number">QUESTION {qn}</span><h2>{title_html}</h2></div>
{body_html}
</div>''')

        active_main = ' active' if cat_name == "Algebra & Equations" else ''
        tabs_nav = '\n'.join(sub_btns)
        panes = '\n'.join(sub_panes)

        main_tabs_html.append(f'''<div id="tab-{cat_id}" class="main-tab{active_main}">
<div class="container">
<div class="tabs-wrapper" id="wrapper-{cat_id}">
<button class="scroll-btn" onclick="this.nextElementSibling.scrollBy({{left:-200,behavior:'smooth'}})">&#10094;</button>
<nav class="tabs-nav">{tabs_nav}</nav>
<button class="scroll-btn" onclick="this.previousElementSibling.scrollBy({{left:200,behavior:'smooth'}})">&#10095;</button>
</div>
{panes}
</div></div>''')

    # Main switcher buttons
    main_btns = []
    for cat_name, cat_id in CAT_IDS.items():
        active = ' active' if cat_name == "Algebra & Equations" else ''
        main_btns.append(f'<button class="main-switcher-btn{active}" id="nav-{cat_id}">{cat_name}</button>')

    main_btns_html = '\n'.join(main_btns)
    main_tabs_joined = '\n'.join(main_tabs_html)

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
--bg-table-header:#1a1a1a;--bg-table-row:#111;--bg-table-row-alt:#0d0d0d;
--bg-tip:rgba(255,255,255,0.04);--bg-important:rgba(255,255,255,0.04);--bg-note:rgba(255,255,255,0.04);
--text-primary:#fff;--text-secondary:#a0a0a0;--text-muted:#666;
--accent:#fff;--border:#222;--border-light:#1a1a1a;
--tip-border:#3b82f6;--important-border:#f59e0b;--note-border:#8b5cf6;--caution-border:#ef4444;
--scrollbar-thumb:#333;--scrollbar-track:#111;--toggle-bg:#222;--toggle-knob:#fff;
--shadow:0 1px 3px rgba(0,0,0,0.5)}}
[data-theme="light"]{{
--bg-primary:#fff;--bg-secondary:#f8f8f8;--bg-card:#fff;--bg-code:#f5f5f5;
--bg-table-header:#f0f0f0;--bg-table-row:#fff;--bg-table-row-alt:#fafafa;
--bg-tip:rgba(0,0,0,0.03);--bg-important:rgba(0,0,0,0.03);--bg-note:rgba(0,0,0,0.03);
--text-primary:#000;--text-secondary:#555;--text-muted:#999;
--accent:#000;--border:#e0e0e0;--border-light:#eee;
--tip-border:#2563eb;--important-border:#d97706;--note-border:#7c3aed;--caution-border:#dc2626;
--scrollbar-thumb:#ccc;--scrollbar-track:#f0f0f0;--toggle-bg:#e0e0e0;--toggle-knob:#000;
--shadow:0 1px 3px rgba(0,0,0,0.1)}}
body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:var(--bg-primary);color:var(--text-secondary);line-height:1.7;-webkit-font-smoothing:antialiased;transition:background var(--transition-speed),color var(--transition-speed)}}
::-webkit-scrollbar{{width:6px}}
::-webkit-scrollbar-track{{background:var(--scrollbar-track)}}
::-webkit-scrollbar-thumb{{background:var(--scrollbar-thumb);border-radius:3px}}
.top-level-nav{{position:sticky;top:0;z-index:200;display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:10px;padding:12px 20px;background:var(--bg-primary);border-bottom:2px solid var(--border);transition:background var(--transition-speed),border var(--transition-speed)}}
.main-switcher-btn{{background:transparent;border:2px solid transparent;color:var(--text-secondary);font-size:0.85rem;font-weight:700;padding:8px 16px;border-radius:8px;cursor:pointer;transition:all var(--transition-speed);font-family:inherit;white-space:nowrap}}
.main-switcher-btn:hover{{color:var(--text-primary);background:var(--bg-card)}}
.main-switcher-btn.active{{border-color:var(--accent);background:var(--bg-card);color:var(--text-primary);box-shadow:var(--shadow)}}
.theme-toggle{{width:52px;height:28px;border-radius:14px;background:var(--toggle-bg);border:none;cursor:pointer;position:relative;transition:background var(--transition-speed);flex-shrink:0}}
.theme-toggle::after{{content:'';position:absolute;width:22px;height:22px;border-radius:50%;background:var(--toggle-knob);top:3px;left:3px;transition:transform var(--transition-speed)}}
[data-theme="light"] .theme-toggle::after{{transform:translateX(24px)}}
.toggle-icons{{position:absolute;width:100%;display:flex;justify-content:space-between;align-items:center;padding:0 5px;font-size:0.7rem;top:50%;transform:translateY(-50%);pointer-events:none}}
.main-tab{{display:none}}
.main-tab.active{{display:block;animation:fadeIn 0.3s ease-in-out}}
.container{{max-width:780px;margin:0 auto;padding:40px 24px 80px}}
.hero{{text-align:center;padding:48px 0 40px;border-bottom:1px solid var(--border);margin-bottom:48px}}
.hero h1{{font-size:clamp(1.8rem,5vw,2.6rem);font-weight:800;letter-spacing:-0.03em;line-height:1.2;color:var(--text-primary);margin-bottom:12px}}
.hero p{{color:var(--text-secondary);max-width:520px;margin:0 auto;font-size:1rem}}
.tabs-wrapper{{display:flex;align-items:center;margin-bottom:32px;border-bottom:1px solid var(--border);position:relative}}
.tabs-nav{{display:flex;overflow-x:auto;white-space:nowrap;scrollbar-width:none;-webkit-overflow-scrolling:touch;flex:1}}
.tabs-nav::-webkit-scrollbar{{display:none}}
.tab-btn{{padding:12px 20px;font-size:0.9rem;font-weight:600;color:var(--text-muted);background:transparent;border:none;border-bottom:2px solid transparent;cursor:pointer;transition:all var(--transition-speed);font-family:inherit;white-space:nowrap}}
.tab-btn:hover{{color:var(--text-secondary);background:var(--bg-code)}}
.tab-btn.active{{color:var(--text-primary);border-bottom:2px solid var(--accent)}}
.scroll-btn{{width:36px;height:36px;display:flex;align-items:center;justify-content:center;background:transparent;border:none;color:var(--text-muted);cursor:pointer;font-size:1rem;flex-shrink:0;transition:color var(--transition-speed)}}
.scroll-btn:hover{{color:var(--text-primary)}}
.section{{margin-bottom:56px}}
.tab-pane{{display:none}}
.tab-pane.active{{display:block;animation:fadeIn 0.3s ease-in-out}}
.section-header{{display:flex;align-items:center;gap:12px;padding-bottom:12px;border-bottom:1px solid var(--border);margin-bottom:20px}}
.section-number{{font-size:0.75rem;font-weight:700;color:var(--text-muted);background:var(--bg-code);border:1px solid var(--border);padding:4px 10px;border-radius:4px;text-transform:uppercase;letter-spacing:0.05em;white-space:nowrap}}
.section-header h2{{font-size:1.4rem;font-weight:700;letter-spacing:-0.02em;color:var(--text-primary)}}
h3{{font-size:1.1rem;font-weight:600;letter-spacing:-0.01em;margin:28px 0 12px;color:var(--text-primary)}}
h4{{font-size:1rem;font-weight:600;margin:20px 0 10px;color:var(--text-primary)}}
p{{margin-bottom:12px}}
strong{{font-weight:600;color:var(--text-primary)}}
.callout{{border-left:3px solid var(--tip-border);border-radius:0 8px 8px 0;padding:16px 20px;margin:20px 0;font-size:0.9rem;background:var(--bg-tip)}}
.callout.tip{{border-left-color:var(--tip-border)}}
.callout.important{{border-left-color:var(--important-border);background:var(--bg-important)}}
.callout.note{{border-left-color:var(--note-border);background:var(--bg-note)}}
.callout-title{{font-weight:700;font-size:0.8rem;text-transform:uppercase;letter-spacing:0.05em;display:flex;align-items:center;gap:6px;margin-bottom:8px;color:var(--tip-border)}}
.callout.important .callout-title{{color:var(--important-border)}}
.callout.note .callout-title{{color:var(--note-border)}}
.step-item{{margin:8px 0;padding-left:8px}}
.math-display{{text-align:center;margin:8px 0 16px;font-size:1.1rem}}
.content-list{{padding-left:24px;margin:8px 0 14px;color:var(--text-secondary)}}
.content-list li{{margin-bottom:4px;list-style:none}}
.practice-box{{margin-top:28px;border:1px solid var(--note-border);border-radius:8px;overflow:hidden;background:var(--bg-card)}}
.practice-header{{background:var(--bg-secondary);padding:12px 16px;font-weight:700;font-size:1rem;border-bottom:1px solid var(--border);color:var(--note-border)}}
.practice-body{{padding:20px}}
.practice-question{{font-size:0.95rem;margin-bottom:15px;line-height:1.5}}
.practice-question p{{margin-bottom:10px}}
.show-answer-btn{{background:var(--note-border);color:#fff;border:none;padding:10px 18px;border-radius:6px;font-weight:600;cursor:pointer;font-family:inherit;font-size:0.9rem;transition:opacity var(--transition-speed)}}
.show-answer-btn:hover{{opacity:0.85}}
.practice-answer{{display:none;margin-top:20px;padding-top:15px;border-top:1px dashed var(--border)}}
.practice-answer.show{{display:block}}
hr.divider{{border:none;border-top:1px solid var(--border);margin:48px 0}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
@media(max-width:640px){{
.top-level-nav{{padding:10px 12px;gap:6px}}
.main-switcher-btn{{font-size:0.75rem;padding:6px 10px}}
.container{{padding:24px 16px 60px}}
.hero{{padding:32px 0 28px;margin-bottom:32px}}
.section{{margin-bottom:40px}}
.section-header{{flex-direction:column;align-items:flex-start;gap:6px}}
.section-header h2{{font-size:1.2rem}}
.callout{{padding:14px 16px}}
.scroll-btn{{display:none}}
.tab-btn{{padding:10px 14px;font-size:0.8rem}}
}}
@media(max-width:380px){{
.main-switcher-btn{{font-size:0.7rem;padding:5px 8px}}
.hero h1{{font-size:1.5rem}}
}}
</style>
</head>
<body>
<div class="top-level-nav">
{main_btns_html}
<button class="theme-toggle" id="themeToggle" aria-label="Toggle theme"><span class="toggle-icons">🌙 ☀️</span></button>
</div>
{main_tabs_joined}
<script>
(function(){{
/* Theme Toggle */
const html=document.documentElement;
const toggle=document.getElementById('themeToggle');
const saved=localStorage.getItem('theme')||'dark';
html.setAttribute('data-theme',saved);
toggle.addEventListener('click',function(){{
const current=html.getAttribute('data-theme');
const next=current==='dark'?'light':'dark';
html.setAttribute('data-theme',next);
localStorage.setItem('theme',next);
}});
/* Main Tab Switching */
const mainBtns=document.querySelectorAll('.main-switcher-btn');
const mainTabs=document.querySelectorAll('.main-tab');
mainBtns.forEach(function(btn){{
btn.addEventListener('click',function(){{
mainBtns.forEach(function(b){{b.classList.remove('active')}});
mainTabs.forEach(function(t){{t.classList.remove('active')}});
btn.classList.add('active');
const targetId='tab-'+btn.id.replace('nav-','');
const target=document.getElementById(targetId);
if(target){{target.classList.add('active')}}
window.scrollTo({{top:0,behavior:'smooth'}});
}});
}});
/* Sub-Tab Switching (scoped) */
function initTabs(wrapperSelector){{
const wrapper=document.querySelector(wrapperSelector);
if(!wrapper)return;
const container=wrapper.closest('.container');
if(!container)return;
const btns=wrapper.querySelectorAll('.tab-btn');
const panes=container.querySelectorAll('.tab-pane');
btns.forEach(function(btn){{
btn.addEventListener('click',function(){{
btns.forEach(function(b){{b.classList.remove('active')}});
panes.forEach(function(p){{p.classList.remove('active')}});
btn.classList.add('active');
const target=document.getElementById(btn.getAttribute('data-target'));
if(target){{target.classList.add('active')}}
window.scrollTo({{top:0,behavior:'smooth'}});
}});
}});
}}
initTabs('#wrapper-algebra');
initTabs('#wrapper-geometry');
initTabs('#wrapper-graphs');
initTabs('#wrapper-data');
initTabs('#wrapper-numbers');
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
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Generated index.html ({len(html)} bytes)")
