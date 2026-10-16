"""
Generates high-resolution 1280x720 executive featured cards for LinkedIn and GitHub Social Previews.
Uses modern HTML5/CSS3 with SVG vector elements rendered via headless Microsoft Edge.
"""

import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CARD_1_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1280px; height: 720px; overflow: hidden;
    background: radial-gradient(circle at 80% 20%, #13271f 0%, #0a0e17 60%, #06090e 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #f8fafc; padding: 50px 60px; display: flex; flex-direction: column; justify-content: space-between;
    position: relative;
  }
  /* Grid pattern overlay */
  .grid-bg {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 32px 32px; pointer-events: none;
  }
  .header { z-index: 1; }
  .tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.4);
    color: #34d399; font-size: 13px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; padding: 6px 14px; border-radius: 9999px; margin-bottom: 16px;
  }
  .tag-dot { width: 8px; height: 8px; border-radius: 50%; background: #10b981; box-shadow: 0 0 10px #10b981; }
  h1 { font-size: 44px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; line-height: 1.1; margin-bottom: 8px; }
  h1 span { background: linear-gradient(90deg, #34d399, #10b981); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .subtitle { font-size: 19px; color: #94a3b8; font-weight: 400; max-width: 800px; }
  
  /* Diagram section */
  .diagram-container {
    z-index: 1; display: grid; grid-template-columns: 280px 60px 420px 60px 280px;
    align-items: center; gap: 10px; margin: 20px 0;
  }
  .diag-box {
    background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px); border-radius: 12px; padding: 18px 20px;
  }
  .diag-box.highlight {
    background: rgba(16, 185, 129, 0.08); border: 1.5px solid rgba(16, 185, 129, 0.45);
    box-shadow: 0 0 30px rgba(16, 185, 129, 0.15);
  }
  .box-title { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; }
  .box-title.green { color: #34d399; }
  .item-list { display: flex; flex-direction: column; gap: 7px; font-size: 13px; font-weight: 500; }
  .item-entry { display: flex; align-items: center; gap: 8px; color: #cbd5e1; }
  .item-icon { width: 14px; height: 14px; color: #64748b; }
  
  .flow-arrow { display: flex; justify-content: center; align-items: center; color: #475569; font-size: 20px; font-weight: bold; }

  /* Footer badges */
  .footer { z-index: 1; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 20px; }
  .badges-group { display: flex; gap: 10px; }
  .badge {
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0; font-size: 13px; font-weight: 600; padding: 7px 16px; border-radius: 8px;
  }
  .author { font-size: 14px; font-weight: 600; color: #64748b; }
  .author span { color: #94a3b8; }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="header">
    <div class="tag"><div class="tag-dot"></div> AI Agent & Systems Architecture</div>
    <h1>Enterprise CSM <span>Engine</span></h1>
    <div class="subtitle">Autonomous AI engine for mission-critical account governance, SLA monitoring, and executive briefings.</div>
  </div>

  <div class="diagram-container">
    <div class="diag-box">
      <div class="box-title">Pluggable Ports</div>
      <div class="item-list">
        <div class="item-entry">📊 CRM & Delta Streams</div>
        <div class="item-entry">🚨 Outage & SLA Monitor</div>
        <div class="item-entry">✉️ Outlook Communications</div>
        <div class="item-entry">📓 Obsidian Vault Store</div>
      </div>
    </div>
    
    <div class="flow-arrow">➔</div>

    <div class="diag-box highlight">
      <div class="box-title green">Core Cognitive Engine (Agnostic Domain)</div>
      <div class="item-list">
        <div class="item-entry" style="color:#ffffff;">⚙️ <strong>Clean Architecture (Ports & Adapters)</strong></div>
        <div class="item-entry">🧠 Severity Heuristics & Churn Risk Scoring</div>
        <div class="item-entry">🔄 4-Stage Operational Loop (Sense ➔ Reason ➔ Act)</div>
        <div class="item-entry">🛡️ Human-in-the-Loop Governance & Simulation</div>
      </div>
    </div>

    <div class="flow-arrow">➔</div>

    <div class="diag-box">
      <div class="box-title">Executive Output</div>
      <div class="item-list">
        <div class="item-entry">📑 Executive Morning Briefing</div>
        <div class="item-entry">📌 Prioritized Sticky Actions</div>
        <div class="item-entry">⏱️ MTTR Breach Alerts</div>
        <div class="item-entry">💾 State Memory & Telemetry</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="badges-group">
      <div class="badge">Python 3.11+</div>
      <div class="badge">Clean Architecture</div>
      <div class="badge">Privacy by Design (Zero Hardcoding)</div>
      <div class="badge">90% Token Reduction</div>
    </div>
    <div class="author">Architecture by <span>Luiz Ramos</span></div>
  </div>
</body>
</html>"""

CARD_2_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1280px; height: 720px; overflow: hidden;
    background: radial-gradient(circle at 80% 20%, #10223d 0%, #0a1120 60%, #060a12 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #f8fafc; padding: 50px 60px; display: flex; flex-direction: column; justify-content: space-between;
    position: relative;
  }
  .grid-bg {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 32px 32px; pointer-events: none;
  }
  .header { z-index: 1; }
  .tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(59, 130, 246, 0.12); border: 1px solid rgba(59, 130, 246, 0.4);
    color: #60a5fa; font-size: 13px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; padding: 6px 14px; border-radius: 9999px; margin-bottom: 16px;
  }
  .tag-dot { width: 8px; height: 8px; border-radius: 50%; background: #3b82f6; box-shadow: 0 0 10px #3b82f6; }
  h1 { font-size: 44px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; line-height: 1.1; margin-bottom: 8px; }
  h1 span { background: linear-gradient(90deg, #60a5fa, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .subtitle { font-size: 19px; color: #94a3b8; font-weight: 400; max-width: 820px; }
  
  /* Pipeline grid */
  .pipeline-grid {
    z-index: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0;
  }
  .stage-card {
    background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px; padding: 22px 18px; backdrop-filter: blur(12px);
    position: relative; display: flex; flex-direction: column; justify-content: space-between;
  }
  .stage-num { font-size: 12px; font-weight: 800; color: #3b82f6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
  .stage-title { font-size: 17px; font-weight: 700; color: #ffffff; margin-bottom: 12px; }
  .stage-items { display: flex; flex-direction: column; gap: 8px; font-size: 13px; color: #94a3b8; }
  .stage-items li { list-style: none; display: flex; align-items: center; gap: 6px; }
  .stage-items li::before { content: "•"; color: #3b82f6; font-size: 16px; }

  /* Footer badges */
  .footer { z-index: 1; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 20px; }
  .badges-group { display: flex; gap: 10px; }
  .badge {
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0; font-size: 13px; font-weight: 600; padding: 7px 16px; border-radius: 8px;
  }
  .author { font-size: 14px; font-weight: 600; color: #64748b; }
  .author span { color: #94a3b8; }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="header">
    <div class="tag"><div class="tag-dot"></div> Commercial Governance & Revenue Operations</div>
    <h1>Sales Operations <span>Playbooks</span></h1>
    <div class="subtitle">Operational frameworks for predictable B2B sales cycles, forecast discipline, and pipeline health.</div>
  </div>

  <div class="pipeline-grid">
    <div class="stage-card">
      <div>
        <div class="stage-num">Framework 01</div>
        <div class="stage-title">Pipeline Governance</div>
        <ul class="stage-items">
          <li>Hygiene & Ageing Rules</li>
          <li>Stage Gate Validation</li>
          <li>Conversion Ratios</li>
        </ul>
      </div>
    </div>

    <div class="stage-card">
      <div>
        <div class="stage-num">Framework 02</div>
        <div class="stage-title">Forecast Predictability</div>
        <ul class="stage-items">
          <li>Commit vs Best Case</li>
          <li>Weekly Operating Cadence</li>
          <li>Variance Analysis</li>
        </ul>
      </div>
    </div>

    <div class="stage-card">
      <div>
        <div class="stage-num">Framework 03</div>
        <div class="stage-title">Deal Execution & SLA</div>
        <ul class="stage-items">
          <li>Contract Approvals</li>
          <li>Zero-Cost Adjustments</li>
          <li>Early Delivery Handover</li>
        </ul>
      </div>
    </div>

    <div class="stage-card">
      <div>
        <div class="stage-num">Framework 04</div>
        <div class="stage-title">Executive Reviews</div>
        <ul class="stage-items">
          <li>Commercial QBR Cadence</li>
          <li>Win/Loss Post-Mortems</li>
          <li>Account Plan Scorecards</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="badges-group">
      <div class="badge">Sales Governance</div>
      <div class="badge">Pipeline Health</div>
      <div class="badge">Forecast Cadence</div>
      <div class="badge">Enterprise B2B</div>
    </div>
    <div class="author">Framework by <span>Luiz Ramos</span></div>
  </div>
</body>
</html>"""

CARD_3_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1280px; height: 720px; overflow: hidden;
    background: radial-gradient(circle at 80% 20%, #2b1f0d 0%, #0d0f17 60%, #07090f 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #f8fafc; padding: 50px 60px; display: flex; flex-direction: column; justify-content: space-between;
    position: relative;
  }
  .grid-bg {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
    background-size: 32px 32px; pointer-events: none;
  }
  .header { z-index: 1; }
  .tag {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.4);
    color: #fbbf24; font-size: 13px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; padding: 6px 14px; border-radius: 9999px; margin-bottom: 16px;
  }
  .tag-dot { width: 8px; height: 8px; border-radius: 50%; background: #f59e0b; box-shadow: 0 0 10px #f59e0b; }
  h1 { font-size: 44px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff; line-height: 1.1; margin-bottom: 8px; }
  h1 span { background: linear-gradient(90deg, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .subtitle { font-size: 19px; color: #94a3b8; font-weight: 400; max-width: 820px; }
  
  /* Mockup dashboard container */
  .dashboard-mockup {
    z-index: 1; display: grid; grid-template-columns: repeat(3, 1fr) 300px; gap: 16px; margin: 20px 0;
  }
  .kpi-card {
    background: rgba(15, 23, 42, 0.75); border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px; padding: 20px; backdrop-filter: blur(12px); display: flex; flex-direction: column; justify-content: space-between;
  }
  .kpi-label { font-size: 12px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.5px; }
  .kpi-value { font-size: 34px; font-weight: 800; color: #ffffff; margin: 8px 0; }
  .kpi-trend { font-size: 12px; font-weight: 600; color: #34d399; display: flex; align-items: center; gap: 4px; }
  
  .side-summary {
    background: rgba(245, 158, 11, 0.06); border: 1.5px solid rgba(245, 158, 11, 0.35);
    border-radius: 12px; padding: 20px; backdrop-filter: blur(12px); display: flex; flex-direction: column; justify-content: center;
  }
  .side-title { font-size: 12px; font-weight: 800; color: #fbbf24; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }
  .side-desc { font-size: 13px; color: #cbd5e1; line-height: 1.5; }

  /* Footer badges */
  .footer { z-index: 1; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 20px; }
  .badges-group { display: flex; gap: 10px; }
  .badge {
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1);
    color: #e2e8f0; font-size: 13px; font-weight: 600; padding: 7px 16px; border-radius: 8px;
  }
  .author { font-size: 14px; font-weight: 600; color: #64748b; }
  .author span { color: #94a3b8; }
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="header">
    <div class="tag"><div class="tag-dot"></div> Business Intelligence & Data Modeling</div>
    <h1>Power BI & <span>Sales Analytics</span></h1>
    <div class="subtitle">End-to-end sales analytics, DAX performance modeling, and automated executive decision cockpits.</div>
  </div>

  <div class="dashboard-mockup">
    <div class="kpi-card">
      <div class="kpi-label">Monitored Portfolio ARR</div>
      <div class="kpi-value">$10.4M</div>
      <div class="kpi-trend">▲ +8.2% vs Previous Quarter</div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">SLA Availability Benchmark</div>
      <div class="kpi-value">99.85%</div>
      <div class="kpi-trend" style="color:#60a5fa;">● Zero High-Severity Breaches</div>
    </div>

    <div class="kpi-card">
      <div class="kpi-label">Global Account Retention</div>
      <div class="kpi-value">98.2%</div>
      <div class="kpi-trend">▲ Proactive Churn Mitigation</div>
    </div>

    <div class="side-summary">
      <div class="side-title">DAX & Automation</div>
      <div class="side-desc">Data warehouse ingestion, star schema modeling, Power Automate schedules, and real-time executive reporting.</div>
    </div>
  </div>

  <div class="footer">
    <div class="badges-group">
      <div class="badge">Power BI</div>
      <div class="badge">Advanced DAX</div>
      <div class="badge">Power Automate</div>
      <div class="badge">Data Warehousing</div>
    </div>
    <div class="author">Solutions by <span>Luiz Ramos</span></div>
  </div>
</body>
</html>"""


def render_card(html_content: str, output_png_path: str):
    temp_html = output_png_path.replace(".png", ".html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [
        EDGE_PATH,
        "--headless=new",
        "--disable-gpu",
        f"--screenshot={output_png_path}",
        "--window-size=1280,720",
        f"file:///{temp_html.replace(os.sep, '/')}",
    ]
    subprocess.run(cmd, check=True)
    time.sleep(1)
    if os.path.exists(temp_html):
        os.remove(temp_html)
    print(f"Generated: {output_png_path}")


def main():
    cards = [
        ("featured_1_enterprise_csm_engine.png", CARD_1_HTML),
        ("featured_2_sales_ops_playbook.png", CARD_2_HTML),
        ("featured_3_powerbi_portfolio.png", CARD_3_HTML),
    ]
    for filename, html in cards:
        out_path = os.path.join(BASE_DIR, filename)
        render_card(html, out_path)


if __name__ == "__main__":
    main()
