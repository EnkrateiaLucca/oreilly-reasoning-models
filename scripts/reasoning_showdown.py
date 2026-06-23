# /// script
# requires-python = ">=3.12"
# dependencies = ["anthropic>=0.40.0", "openai>=1.55.0", "python-dotenv"]
# ///
"""
Reasoning Showdown: Claude Opus 4.6 (extended thinking) vs GPT-5.4 (high reasoning effort).

Generates 3 one-pager markdown reports with each model, measures latency, token usage,
and cost, then writes an interactive HTML dashboard.
"""
from __future__ import annotations

import json
import os
import time
import webbrowser
from dataclasses import dataclass, asdict
from pathlib import Path

from dotenv import load_dotenv
from anthropic import Anthropic
from openai import OpenAI

load_dotenv()

# --- Pricing ($ per 1M tokens). Update if upstream pricing changes. ---
PRICING = {
    "claude-opus-4-6": {"input": 5.00, "output": 25.00},
    # GPT-5.4 standard pricing per developers.openai.com/api/docs/pricing
    "gpt-5.4":         {"input": 2.50, "output": 15.00},
}

CLAUDE_MODEL = "claude-opus-4-6"
OPENAI_MODEL = "gpt-5.4"
THINKING_BUDGET = 8000   # Claude extended-thinking budget tokens
MAX_TOKENS_OUT = 16000

PROMPTS = [
    {
        "id": "quantum",
        "title": "Quantum Computing 2025-2026",
        "prompt": (
            "Write a one-page markdown executive briefing on the state of quantum computing "
            "in 2025-2026. Cover: hardware leaders, error-correction milestones, near-term "
            "commercial applications, and the realistic 3-year outlook. Use headings, bullets, "
            "and a short risk table. Keep it under ~500 words."
        ),
    },
    {
        "id": "agents",
        "title": "AI Agent Frameworks Landscape",
        "prompt": (
            "Write a one-page markdown executive briefing comparing today's AI agent frameworks "
            "(LangGraph, CrewAI, OpenAI Agents SDK, Claude Agent SDK, etc.). Include strengths, "
            "weaknesses, ideal use cases, and a recommendation matrix. Use headings, bullets, "
            "and a comparison table. Keep it under ~500 words."
        ),
    },
    {
        "id": "edge",
        "title": "Edge AI & On-Device Inference",
        "prompt": (
            "Write a one-page markdown executive briefing on edge AI and on-device inference. "
            "Cover hardware (NPUs, Apple Silicon, Qualcomm), model compression techniques, "
            "privacy advantages, and key business use cases. Use headings, bullets, and a "
            "trade-offs table. Keep it under ~500 words."
        ),
    },
]


@dataclass
class RunResult:
    provider: str
    model: str
    prompt_id: str
    prompt_title: str
    latency_s: float
    input_tokens: int
    output_tokens: int          # visible output only
    reasoning_tokens: int       # thinking/reasoning tokens (billed as output)
    total_output_tokens: int    # output + reasoning
    cost_usd: float
    markdown: str
    error: str | None = None


def cost_for(model: str, in_tok: int, out_tok: int) -> float:
    p = PRICING[model]
    return (in_tok / 1_000_000) * p["input"] + (out_tok / 1_000_000) * p["output"]


def run_claude(client: Anthropic, prompt: dict) -> RunResult:
    t0 = time.perf_counter()
    try:
        resp = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=MAX_TOKENS_OUT,
            thinking={"type": "enabled", "budget_tokens": THINKING_BUDGET},
            messages=[{"role": "user", "content": prompt["prompt"]}],
        )
        latency = time.perf_counter() - t0

        # Pull out visible text + thinking blocks
        visible_md = ""
        thinking_chars = 0
        for block in resp.content:
            if block.type == "text":
                visible_md += block.text
            elif block.type == "thinking":
                thinking_chars += len(getattr(block, "thinking", "") or "")

        in_tok = resp.usage.input_tokens
        out_tok = resp.usage.output_tokens  # Anthropic includes thinking in output_tokens
        # Approximate split: Anthropic doesn't break out thinking tokens directly in usage,
        # so we estimate from the ratio of visible vs thinking text length.
        total_chars = max(1, len(visible_md) + thinking_chars)
        visible_share = len(visible_md) / total_chars
        visible_tok = int(round(out_tok * visible_share))
        reasoning_tok = out_tok - visible_tok

        return RunResult(
            provider="Anthropic",
            model=CLAUDE_MODEL,
            prompt_id=prompt["id"],
            prompt_title=prompt["title"],
            latency_s=round(latency, 3),
            input_tokens=in_tok,
            output_tokens=visible_tok,
            reasoning_tokens=reasoning_tok,
            total_output_tokens=out_tok,
            cost_usd=round(cost_for(CLAUDE_MODEL, in_tok, out_tok), 6),
            markdown=visible_md.strip(),
        )
    except Exception as e:
        return RunResult("Anthropic", CLAUDE_MODEL, prompt["id"], prompt["title"],
                         round(time.perf_counter() - t0, 3), 0, 0, 0, 0, 0.0, "", str(e))


def run_openai(client: OpenAI, prompt: dict) -> RunResult:
    t0 = time.perf_counter()
    try:
        resp = client.responses.create(
            model=OPENAI_MODEL,
            reasoning={"effort": "high"},
            input=[
                {"role": "developer", "content": "You are a precise executive briefing writer."},
                {"role": "user", "content": prompt["prompt"]},
            ],
        )
        latency = time.perf_counter() - t0
        md = resp.output_text or ""

        usage = resp.usage
        in_tok = getattr(usage, "input_tokens", 0)
        out_tok = getattr(usage, "output_tokens", 0)  # includes reasoning tokens
        details = getattr(usage, "output_tokens_details", None)
        reasoning_tok = getattr(details, "reasoning_tokens", 0) if details else 0
        visible_tok = max(0, out_tok - reasoning_tok)

        return RunResult(
            provider="OpenAI",
            model=OPENAI_MODEL,
            prompt_id=prompt["id"],
            prompt_title=prompt["title"],
            latency_s=round(latency, 3),
            input_tokens=in_tok,
            output_tokens=visible_tok,
            reasoning_tokens=reasoning_tok,
            total_output_tokens=out_tok,
            cost_usd=round(cost_for(OPENAI_MODEL, in_tok, out_tok), 6),
            markdown=md.strip(),
        )
    except Exception as e:
        return RunResult("OpenAI", OPENAI_MODEL, prompt["id"], prompt["title"],
                         round(time.perf_counter() - t0, 3), 0, 0, 0, 0, 0.0, "", str(e))


def build_dashboard(results: list[RunResult], out_path: Path) -> None:
    data_json = json.dumps([asdict(r) for r in results])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Reasoning Showdown — Claude Opus 4.6 vs GPT-5.4</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<style>
  :root {{ --bg:#0b1020; --card:#141a33; --ink:#e7ecff; --muted:#9aa6c7;
          --anthropic:#d97757; --openai:#10a37f; --accent:#7c9cff; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:-apple-system,Segoe UI,Inter,sans-serif;
          background:var(--bg); color:var(--ink); }}
  header {{ padding:32px 40px; border-bottom:1px solid #222a4d; }}
  h1 {{ margin:0 0 6px; font-size:28px; }}
  header p {{ margin:0; color:var(--muted); }}
  main {{ padding:24px 40px 60px; max-width:1400px; margin:auto; }}
  .grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:28px; }}
  .card {{ background:var(--card); border:1px solid #222a4d; border-radius:14px;
           padding:20px; }}
  .card h3 {{ margin:0 0 14px; font-size:14px; color:var(--muted);
              text-transform:uppercase; letter-spacing:.08em; }}
  .controls {{ display:flex; gap:12px; flex-wrap:wrap; margin:0 0 22px; }}
  .controls button {{ background:var(--card); color:var(--ink); border:1px solid #2a345f;
                      padding:8px 16px; border-radius:999px; cursor:pointer; font-size:13px; }}
  .controls button.active {{ background:var(--accent); border-color:var(--accent); color:#0b1020; font-weight:600; }}
  .reports {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }}
  .report {{ background:var(--card); border:1px solid #222a4d; border-radius:14px; padding:22px; }}
  .report .badge {{ display:inline-block; padding:3px 10px; border-radius:999px;
                    font-size:11px; font-weight:600; letter-spacing:.05em; text-transform:uppercase; }}
  .badge.anthropic {{ background:rgba(217,119,87,.18); color:var(--anthropic); }}
  .badge.openai    {{ background:rgba(16,163,127,.18); color:var(--openai); }}
  .stats {{ display:flex; gap:18px; margin:12px 0 16px; font-size:12px; color:var(--muted); }}
  .stats b {{ color:var(--ink); font-size:13px; }}
  .md {{ background:#0b1020; border:1px solid #222a4d; border-radius:10px;
         padding:16px 18px; max-height:420px; overflow:auto; font-size:13px; line-height:1.55; }}
  .md h1,.md h2,.md h3 {{ color:var(--accent); }}
  .md table {{ border-collapse:collapse; width:100%; margin:8px 0; }}
  .md th,.md td {{ border:1px solid #2a345f; padding:6px 10px; font-size:12px; }}
  .err {{ color:#ff6b8a; font-family:monospace; font-size:12px; white-space:pre-wrap; }}
  footer {{ text-align:center; color:var(--muted); font-size:12px; padding:20px; }}
</style>
</head>
<body>
<header>
  <h1>🧠 Reasoning Showdown</h1>
  <p>Claude Opus 4.6 (extended thinking) vs GPT-5.4 (high reasoning effort) — one-pager generation benchmark.</p>
</header>
<main>
  <div class="grid">
    <div class="card"><h3>Latency by prompt (s)</h3><canvas id="cLat"></canvas></div>
    <div class="card"><h3>Total output tokens (visible + reasoning)</h3><canvas id="cTok"></canvas></div>
    <div class="card"><h3>Cost per run (USD)</h3><canvas id="cCost"></canvas></div>
  </div>

  <div class="card" style="margin-bottom:28px;">
    <h3>Reasoning vs visible output tokens</h3>
    <canvas id="cStack" height="90"></canvas>
  </div>

  <div class="controls" id="promptTabs"></div>
  <div class="reports" id="reports"></div>
</main>
<footer>Generated locally · click prompt tabs to switch reports</footer>

<script>
const DATA = {data_json};
const A = "#d97757", O = "#10a37f";
const prompts = [...new Set(DATA.map(d => d.prompt_id))];
const titles  = Object.fromEntries(DATA.map(d => [d.prompt_id, d.prompt_title]));
const byProvider = p => DATA.filter(d => d.provider === p);

function mkBar(id, label1, label2, vals1, vals2) {{
  new Chart(document.getElementById(id), {{
    type:'bar',
    data: {{ labels: prompts.map(p=>titles[p]),
             datasets:[
               {{label:label1, data:vals1, backgroundColor:A}},
               {{label:label2, data:vals2, backgroundColor:O}}
             ]}},
    options: {{ responsive:true, plugins:{{legend:{{labels:{{color:'#e7ecff'}}}}}},
               scales:{{x:{{ticks:{{color:'#9aa6c7'}}}}, y:{{ticks:{{color:'#9aa6c7'}}}}}} }}
  }});
}}

const claude = byProvider("Anthropic"), oai = byProvider("OpenAI");
const get = (arr, key) => prompts.map(p => {{ const r = arr.find(x=>x.prompt_id===p); return r? r[key] : 0; }});

mkBar('cLat',  'Claude Opus 4.6', 'GPT-5.4', get(claude,'latency_s'),         get(oai,'latency_s'));
mkBar('cTok',  'Claude Opus 4.6', 'GPT-5.4', get(claude,'total_output_tokens'),get(oai,'total_output_tokens'));
mkBar('cCost', 'Claude Opus 4.6', 'GPT-5.4', get(claude,'cost_usd'),          get(oai,'cost_usd'));

new Chart(document.getElementById('cStack'), {{
  type:'bar',
  data: {{
    labels: DATA.map(d => `${{d.provider==='Anthropic'?'C':'G'}} · ${{d.prompt_title}}`),
    datasets:[
      {{label:'Visible output',  data:DATA.map(d=>d.output_tokens),    backgroundColor:'#7c9cff'}},
      {{label:'Reasoning tokens',data:DATA.map(d=>d.reasoning_tokens), backgroundColor:'#ffb86b'}}
    ]
  }},
  options:{{ responsive:true, indexAxis:'y',
            scales:{{x:{{stacked:true,ticks:{{color:'#9aa6c7'}}}}, y:{{stacked:true,ticks:{{color:'#9aa6c7'}}}}}},
            plugins:{{legend:{{labels:{{color:'#e7ecff'}}}}}} }}
}});

// Tabs + reports
const tabsEl = document.getElementById('promptTabs');
const reportsEl = document.getElementById('reports');
prompts.forEach((p,i) => {{
  const b = document.createElement('button');
  b.textContent = titles[p];
  if (i===0) b.classList.add('active');
  b.onclick = () => {{ document.querySelectorAll('#promptTabs button').forEach(x=>x.classList.remove('active'));
                       b.classList.add('active'); render(p); }};
  tabsEl.appendChild(b);
}});

function render(pid) {{
  reportsEl.innerHTML = '';
  DATA.filter(d => d.prompt_id === pid).forEach(d => {{
    const cls = d.provider === 'Anthropic' ? 'anthropic' : 'openai';
    const body = d.error
      ? `<div class="err">ERROR: ${{d.error}}</div>`
      : `<div class="md">${{marked.parse(d.markdown || '_(empty)_')}}</div>`;
    reportsEl.insertAdjacentHTML('beforeend', `
      <div class="report">
        <span class="badge ${{cls}}">${{d.provider}} · ${{d.model}}</span>
        <div class="stats">
          <span><b>${{d.latency_s}}s</b> latency</span>
          <span><b>${{d.input_tokens}}</b> in</span>
          <span><b>${{d.output_tokens}}</b> visible</span>
          <span><b>${{d.reasoning_tokens}}</b> reasoning</span>
          <span><b>$${{d.cost_usd.toFixed(4)}}</b></span>
        </div>
        ${{body}}
      </div>`);
  }});
}}
render(prompts[0]);
</script>
</body>
</html>
"""
    out_path.write_text(html, encoding="utf-8")


def main() -> None:
    if not os.getenv("ANTHROPIC_API_KEY") or not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY and OPENAI_API_KEY in your environment / .env")

    anthropic_client = Anthropic()
    openai_client = OpenAI()

    results: list[RunResult] = []
    for p in PROMPTS:
        print(f"\n▶ {p['title']}")
        print("  · Claude Opus 4.6 (extended thinking)…")
        rc = run_claude(anthropic_client, p)
        print(f"    {rc.latency_s}s  in={rc.input_tokens}  vis={rc.output_tokens}  "
              f"think={rc.reasoning_tokens}  ${rc.cost_usd:.4f}"
              + (f"  ERR: {rc.error}" if rc.error else ""))
        results.append(rc)

        print("  · GPT-5.4 (reasoning effort=high)…")
        ro = run_openai(openai_client, p)
        print(f"    {ro.latency_s}s  in={ro.input_tokens}  vis={ro.output_tokens}  "
              f"think={ro.reasoning_tokens}  ${ro.cost_usd:.4f}"
              + (f"  ERR: {ro.error}" if ro.error else ""))
        results.append(ro)

    out_dir = Path(__file__).parent
    html_path = out_dir / "reasoning_showdown_dashboard.html"
    json_path = out_dir / "reasoning_showdown_results.json"
    json_path.write_text(json.dumps([asdict(r) for r in results], indent=2))
    build_dashboard(results, html_path)

    print(f"\n✅ Dashboard:  {html_path}")
    print(f"📄 Raw JSON:   {json_path}")
    webbrowser.open(f"file://{html_path}")


if __name__ == "__main__":
    main()
