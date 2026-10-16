"""
Generates refined executive featured cards for LinkedIn and GitHub:
- Card 1: Clean Architecture Flowchart diagram (Ports ➔ Core Engine ➔ Executive Output).
- Card 2: 4-Stage Sequential Pipeline Process Flowchart (Hygiene ➔ Forecast ➔ Deal Governance ➔ QBRs).
- Card 3: Executive Metric & KPI Cards for Power BI (The preferred analytics cockpit layout).
"""

import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

COMMON_BASE_CSS = """
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    width: 1280px; height: 720px; overflow: hidden;
    background: #090d16;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
    color: #f8fafc; padding: 50px 64px; display: flex; flex-direction: column; justify-content: space-between;
    position: relative;
  }
  .grid-bg {
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image: linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
    background-size: 32px 32px; pointer-events: none;
  }
  .header { z-index: 1; }
  .tag {
    display: inline-block;
    background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.12);
    color: #94a3b8; font-size: 11px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; padding: 5px 12px; border-radius: 6px; margin-bottom: 14px;
  }
  h1 { font-size: 42px; font-weight: 700; letter-spacing: -0.5px; color: #ffffff; line-height: 1.1; margin-bottom: 8px; }
  .subtitle { font-size: 18px; color: #94a3b8; font-weight: 400; max-width: 860px; line-height: 1.4; }

  .footer { z-index: 1; display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 18px; }
  .badges-group { display: flex; gap: 10px; }
  .badge {
    background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08);
    color: #cbd5e1; font-size: 12px; font-weight: 600; padding: 6px 14px; border-radius: 6px;
  }
  .author { font-size: 13px; font-weight: 500; color: #64748b; }
  .author span { color: #cbd5e1; font-weight: 600; }
"""

# Card 1: Flowchart Architecture (Ports ➔ Core Cognitive Engine ➔ Executive Output)
CARD_1_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
{COMMON_BASE_CSS}
  .flowchart-container {{
    z-index: 1; display: grid; grid-template-columns: 290px 48px 460px 48px 280px;
    align-items: center; gap: 8px; margin: 18px 0;
  }}
  .box {{
    background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px; padding: 20px 20px;
  }}
  .box.core {{
    background: rgba(17, 24, 39, 0.85); border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
  }}
  .box-label {{ font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }}
  .box-label.highlight {{ color: #e2e8f0; }}
  .list {{ display: flex; flex-direction: column; gap: 9px; font-size: 13px; }}
  .item {{ display: flex; align-items: center; gap: 8px; color: #cbd5e1; }}
  .arrow {{ text-align: center; color: #475569; font-size: 22px; font-weight: bold; }}
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="header">
    <div class="tag">System Architecture</div>
    <h1>Enterprise CSM Engine</h1>
    <div class="subtitle">Autonomous system engineered to streamline account governance, SLA tracking, and executive morning briefings.</div>
  </div>

  <div class="flowchart-container">
    <div class="box">
      <div class="box-label">Pluggable Ports</div>
      <div class="list">
        <div class="item">📊 CRM & Delta Streams</div>
        <div class="item">🚨 Incident & SLA Monitor</div>
        <div class="item">✉️ Communication Channels</div>
        <div class="item">📓 Markdown Knowledge Store</div>
      </div>
    </div>

    <div class="arrow">➔</div>

    <div class="box core">
      <div class="box-label highlight">Core Cognitive Engine (Agnostic Domain)</div>
      <div class="list">
        <div class="item" style="color:#ffffff; font-weight:600;">⚙️ Clean Architecture (Ports & Adapters)</div>
        <div class="item">🧠 SLA, MTTR & Churn Heuristic Scoring</div>
        <div class="item">🔄 4-Stage Loop (Sense ➔ Reason ➔ Act ➔ Memory)</div>
        <div class="item">🛡️ Human-in-the-Loop Governance & Simulation</div>
      </div>
    </div>

    <div class="arrow">➔</div>

    <div class="box">
      <div class="box-label">Executive Output</div>
      <div class="list">
        <div class="item">📑 Morning Briefing Notes</div>
        <div class="item">📌 Prioritized Action Items</div>
        <div class="item">⏱️ MTTR Breach Warnings</div>
        <div class="item">💾 State History Telemetry</div>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="badges-group">
      <div class="badge">Python 3.11+</div>
      <div class="badge">Clean Architecture</div>
      <div class="badge">Zero Data Leakage</div>
      <div class="badge">-90% Token Load</div>
    </div>
    <div class="author">System Architecture by <span>Luiz Ramos</span></div>
  </div>
</body>
</html>"""

# Card 2: 4-Stage Sequential Process Flowchart (Hygiene ➔ Forecast ➔ Execution ➔ QBRs)
CARD_2_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
{COMMON_BASE_CSS}
  .pipeline-flow {{
    z-index: 1; display: grid; grid-template-columns: 1fr 24px 1fr 24px 1fr 24px 1fr;
    align-items: center; gap: 4px; margin: 20px 0;
  }}
  .step-box {{
    background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px; padding: 22px 18px; display: flex; flex-direction: column; justify-content: space-between;
    min-height: 200px;
  }}
  .step-num {{ font-size: 11px; font-weight: 800; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }}
  .step-title {{ font-size: 16px; font-weight: 700; color: #ffffff; margin-bottom: 12px; line-height: 1.2; }}
  .step-items {{ display: flex; flex-direction: column; gap: 7px; font-size: 13px; color: #94a3b8; list-style: none; }}
  .step-items li {{ display: flex; align-items: center; gap: 6px; }}
  .step-items li::before {{ content: "•"; color: #475569; font-size: 14px; }}
  .flow-arrow {{ text-align: center; color: #475569; font-size: 18px; font-weight: bold; }}
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="header">
    <div class="tag">Commercial Governance</div>
    <h1>Sales Operations Playbooks</h1>
    <div class="subtitle">Operational process frameworks for enterprise B2B sales cycles, forecast discipline, and pipeline health.</div>
  </div>

  <div class="pipeline-flow">
    <div class="step-box">
      <div>
        <div class="step-num">Phase 01</div>
        <div class="step-title">Pipeline Hygiene</div>
        <ul class="step-items">
          <li>Stage Gate Validation</li>
          <li>Stalled Deal Detection</li>
          <li>Conversion Velocity</li>
        </ul>
      </div>
    </div>

    <div class="flow-arrow">➔</div>

    <div class="step-box">
      <div>
        <div class="step-num">Phase 02</div>
        <div class="step-title">Forecast Cadence</div>
        <ul class="step-items">
          <li>Commit vs Best Case</li>
          <li>Weekly Operating Rhythm</li>
          <li>Variance Tracking</li>
        </ul>
      </div>
    </div>

    <div class="flow-arrow">➔</div>

    <div class="step-box">
      <div>
        <div class="step-num">Phase 03</div>
        <div class="step-title">Deal Governance</div>
        <ul class="step-items">
          <li>Contract Approvals</li>
          <li>Billing Dispute Control</li>
          <li>Early Handover SLAs</li>
        </ul>
      </div>
    </div>

    <div class="flow-arrow">➔</div>

    <div class="step-box">
      <div>
        <div class="step-num">Phase 04</div>
        <div class="step-title">Executive Reviews</div>
        <ul class="step-items">
          <li>QBR Cadence Structure</li>
          <li>Win/Loss Post-Mortems</li>
          <li>Cross-Team Alignment</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="footer">
    <div class="badges-group">
      <div class="badge">Pipeline Health</div>
      <div class="badge">Forecast Discipline</div>
      <div class="badge">Contract SLAs</div>
      <div class="badge">Executive QBRs</div>
    </div>
    <div class="author">Frameworks by <span>Luiz Ramos</span></div>
  </div>
</body>
</html>"""

# Card 3: Metric & KPI Cards (The user's favorite layout)
CARD_3_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
{COMMON_BASE_CSS}
  .cards-grid {{
    z-index: 1; display: grid; grid-template-columns: repeat(3, 1fr) 300px; gap: 16px; margin: 24px 0;
  }}
  .tile {{
    background: rgba(17, 24, 39, 0.6); border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px; padding: 22px 20px; display: flex; flex-direction: column; justify-content: space-between;
  }}
  .tile-label {{ font-size: 11px; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 8px; }}
  .tile-main {{ font-size: 34px; font-weight: 700; color: #ffffff; margin-bottom: 6px; }}
  .tile-desc {{ font-size: 13px; color: #94a3b8; line-height: 1.4; }}

  .side-tile {{
    background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px; padding: 22px 20px; display: flex; flex-direction: column; justify-content: center;
  }}
  .side-title {{ font-size: 12px; font-weight: 700; color: #e2e8f0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; }}
  .side-desc {{ font-size: 13px; color: #94a3b8; line-height: 1.5; }}
</style>
</head>
<body>
  <div class="grid-bg"></div>
  <div class="header">
    <div class="tag">Business Intelligence</div>
    <h1>Power BI & Sales Analytics</h1>
    <div class="subtitle">End-to-end sales analytics, DAX performance modeling, and automated executive decision cockpits for enterprise teams.</div>
  </div>

  <div class="cards-grid">
    <div class="tile">
      <div>
        <div class="tile-label">Monitored Portfolio ARR</div>
        <div class="tile-main">$10.4M+</div>
      </div>
      <div class="tile-desc">Multi-account enterprise contract tracking and quarterly revenue expansion monitoring.</div>
    </div>

    <div class="tile">
      <div>
        <div class="tile-label">SLA Availability Benchmark</div>
        <div class="tile-main">99.85%</div>
      </div>
      <div class="tile-desc">Zero critical service breaches with automated outage duration and MTTR tracking.</div>
    </div>

    <div class="tile">
      <div>
        <div class="tile-label">Global Account Retention</div>
        <div class="tile-main">98.2%</div>
      </div>
      <div class="tile-desc">Proactive churn risk scoring and customer health index modeling.</div>
    </div>

    <div class="side-tile">
      <div class="side-title">Data Architecture</div>
      <div class="side-desc">Data warehouse ingestion, star schema modeling, Power Automate schedules, and real-time executive reporting.</div>
    </div>
  </div>

  <div class="footer">
    <div class="badges-group">
      <div class="badge">Power BI</div>
      <div class="badge">Advanced DAX</div>
      <div class="badge">Power Automate</div>
      <div class="badge">KPI Automation</div>
    </div>
    <div class="author">Analytics by <span>Luiz Ramos</span></div>
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
    print(f"Rendered: {output_png_path}")


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
