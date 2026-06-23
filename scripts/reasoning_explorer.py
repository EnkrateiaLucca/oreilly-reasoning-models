# /// script
# requires-python = ">=3.12"
# dependencies = ["openai", "anthropic", "python-dotenv"]
# ///
"""
Reasoning Explorer — tiny local web app to inspect reasoning traces from
OpenAI (Responses API reasoning summaries) and Anthropic (extended thinking blocks).

Run:
    uv run scripts/reasoning_explorer.py
Then open http://localhost:8765
"""
from __future__ import annotations

import json
import os
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PORT = int(os.environ.get("PORT", "8765"))


def call_openai(prompt: str, model: str, effort: str) -> dict:
    from openai import OpenAI

    client = OpenAI()
    resp = client.responses.create(
        model=model,
        reasoning={"effort": effort, "summary": "auto"},
        input=[{"role": "user", "content": prompt}],
    )

    # Extract reasoning summary items + final text
    reasoning_chunks: list[str] = []
    for item in resp.output:
        if getattr(item, "type", None) == "reasoning":
            for s in (item.summary or []):
                txt = getattr(s, "text", None)
                if txt:
                    reasoning_chunks.append(txt)

    usage = resp.usage.model_dump() if hasattr(resp, "usage") and resp.usage else {}
    return {
        "provider": "openai",
        "model": model,
        "reasoning": reasoning_chunks,
        "output": resp.output_text,
        "usage": usage,
        "note": "OpenAI does not expose raw reasoning tokens — what you see is an auto-generated summary.",
    }


def call_anthropic(prompt: str, model: str, budget: int) -> dict:
    from anthropic import Anthropic

    client = Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=max(budget + 2000, 4000),
        thinking={"type": "enabled", "budget_tokens": budget},
        messages=[{"role": "user", "content": prompt}],
    )

    reasoning_chunks: list[str] = []
    output_chunks: list[str] = []
    for block in msg.content:
        if block.type == "thinking":
            reasoning_chunks.append(block.thinking)
        elif block.type == "text":
            output_chunks.append(block.text)

    usage = msg.usage.model_dump() if hasattr(msg, "usage") else {}
    return {
        "provider": "anthropic",
        "model": model,
        "reasoning": reasoning_chunks,
        "output": "\n".join(output_chunks),
        "usage": usage,
        "note": "Anthropic exposes the full extended-thinking text directly.",
    }


INDEX_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>Reasoning Explorer</title>
<style>
  :root { --bg:#0e1116; --panel:#161b22; --border:#30363d; --fg:#e6edf3; --muted:#8b949e; --accent:#7ee787; --accent2:#79c0ff; }
  * { box-sizing: border-box; }
  body { margin:0; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif; background:var(--bg); color:var(--fg); }
  header { padding: 16px 24px; border-bottom:1px solid var(--border); display:flex; align-items:center; gap:16px;}
  header h1 { margin:0; font-size:18px; font-weight:600; }
  header span { color:var(--muted); font-size:13px; }
  main { display:grid; grid-template-columns: 380px 1fr; gap:0; height: calc(100vh - 57px); }
  .sidebar { padding:20px; border-right:1px solid var(--border); overflow-y:auto; }
  .sidebar label { display:block; font-size:12px; text-transform:uppercase; color:var(--muted); margin: 14px 0 6px; letter-spacing:.5px;}
  .sidebar select, .sidebar input, .sidebar textarea {
    width:100%; background:var(--panel); color:var(--fg); border:1px solid var(--border);
    border-radius:6px; padding:8px 10px; font-size:13px; font-family:inherit;
  }
  .sidebar textarea { min-height: 180px; resize: vertical; }
  .sidebar button {
    margin-top:18px; width:100%; padding:10px; background:var(--accent); color:#0e1116;
    border:none; border-radius:6px; font-weight:600; cursor:pointer; font-size:14px;
  }
  .sidebar button:disabled { opacity:.5; cursor:not-allowed; }
  .results { padding:20px 28px; overflow-y:auto; }
  .tabs { display:flex; gap:4px; border-bottom:1px solid var(--border); margin-bottom:16px;}
  .tab { padding:10px 16px; cursor:pointer; color:var(--muted); border-bottom:2px solid transparent; font-size:13px;}
  .tab.active { color:var(--accent2); border-bottom-color:var(--accent2); }
  .panel { display:none; }
  .panel.active { display:block; }
  pre { background:var(--panel); border:1px solid var(--border); border-radius:8px;
        padding:14px 16px; white-space:pre-wrap; word-wrap:break-word; font-size:13px; line-height:1.55; }
  .reasoning-step { border-left:3px solid var(--accent2); padding:10px 14px; background:#0d1117;
                    border-radius:0 6px 6px 0; margin-bottom:10px; }
  .reasoning-step .num { color:var(--accent2); font-size:11px; text-transform:uppercase; font-weight:600; }
  .reasoning-step pre { background:transparent; border:none; padding:6px 0 0; }
  .meta { color:var(--muted); font-size:12px; margin-bottom:12px; }
  .pill { display:inline-block; background:var(--panel); border:1px solid var(--border);
          padding:3px 8px; border-radius:999px; font-size:11px; margin-right:6px; }
  .empty { color:var(--muted); font-style:italic; padding:20px; }
  .error { color:#f85149; background:#2d1517; border:1px solid #f85149; padding:12px; border-radius:6px;}
  .controls-anth, .controls-oai { display:none; }
  .controls-anth.show, .controls-oai.show { display:block; }
</style>
</head>
<body>
<header>
  <h1>🧠 Reasoning Explorer</h1>
  <span>Inspect intermediate reasoning traces from OpenAI &amp; Anthropic</span>
</header>
<main>
  <div class="sidebar">
    <label>Provider</label>
    <select id="provider">
      <option value="openai">OpenAI (Responses API)</option>
      <option value="anthropic">Anthropic (Extended Thinking)</option>
    </select>

    <div class="controls-oai show">
      <label>Model</label>
      <select id="oai-model">
        <option>gpt-5.2</option>
        <option>o4-mini</option>
        <option>o3</option>
      </select>
      <label>Reasoning effort</label>
      <select id="oai-effort">
        <option>low</option>
        <option selected>medium</option>
        <option>high</option>
      </select>
    </div>

    <div class="controls-anth">
      <label>Model</label>
      <select id="anth-model">
        <option>claude-sonnet-4-5-20250929</option>
        <option>claude-opus-4-5</option>
      </select>
      <label>Thinking budget (tokens)</label>
      <input id="anth-budget" type="number" value="5000" min="1024" step="1000" />
    </div>

    <label>Prompt</label>
    <textarea id="prompt" placeholder="e.g. A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?">A bat and a ball cost $1.10. The bat costs $1.00 more than the ball. How much does the ball cost?</textarea>

    <button id="run">Run ▶</button>
  </div>

  <div class="results">
    <div class="tabs">
      <div class="tab active" data-tab="reasoning">🧩 Reasoning Trace</div>
      <div class="tab" data-tab="output">✅ Final Output</div>
      <div class="tab" data-tab="raw">🔬 Raw JSON</div>
    </div>
    <div id="meta" class="meta"></div>
    <div class="panel active" id="panel-reasoning"><div class="empty">Run a prompt to see reasoning steps.</div></div>
    <div class="panel" id="panel-output"><div class="empty">Run a prompt to see the final answer.</div></div>
    <div class="panel" id="panel-raw"><div class="empty">Run a prompt to see the raw response.</div></div>
  </div>
</main>

<script>
const $ = (id) => document.getElementById(id);
const provider = $("provider");
provider.addEventListener("change", () => {
  document.querySelector(".controls-oai").classList.toggle("show", provider.value === "openai");
  document.querySelector(".controls-anth").classList.toggle("show", provider.value === "anthropic");
});
document.querySelectorAll(".tab").forEach(t => t.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach(x => x.classList.remove("active"));
  document.querySelectorAll(".panel").forEach(x => x.classList.remove("active"));
  t.classList.add("active");
  $("panel-" + t.dataset.tab).classList.add("active");
}));

$("run").addEventListener("click", async () => {
  const btn = $("run"); btn.disabled = true; btn.textContent = "Thinking…";
  const body = { provider: provider.value, prompt: $("prompt").value };
  if (provider.value === "openai") {
    body.model = $("oai-model").value;
    body.effort = $("oai-effort").value;
  } else {
    body.model = $("anth-model").value;
    body.budget = parseInt($("anth-budget").value, 10);
  }
  try {
    const r = await fetch("/api/run", { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify(body) });
    const data = await r.json();
    if (data.error) { render({ error: data.error, traceback: data.traceback }); }
    else { render(data); }
  } catch (e) {
    render({ error: e.message });
  } finally {
    btn.disabled = false; btn.textContent = "Run ▶";
  }
});

function escapeHtml(s) { return (s||"").replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c])); }

function render(data) {
  if (data.error) {
    $("panel-reasoning").innerHTML = `<div class="error">${escapeHtml(data.error)}<pre>${escapeHtml(data.traceback||"")}</pre></div>`;
    $("panel-output").innerHTML = ""; $("panel-raw").innerHTML = ""; $("meta").innerHTML = "";
    return;
  }
  const u = data.usage || {};
  $("meta").innerHTML =
    `<span class="pill">${data.provider}</span>` +
    `<span class="pill">${data.model}</span>` +
    Object.entries(u).filter(([k,v]) => typeof v === "number").map(([k,v]) => `<span class="pill">${k}: ${v}</span>`).join("") +
    (data.note ? `<div style="margin-top:8px;">${escapeHtml(data.note)}</div>` : "");

  const r = data.reasoning || [];
  if (r.length === 0) {
    $("panel-reasoning").innerHTML = `<div class="empty">No reasoning trace returned. (Model may not have produced one, or summary was empty.)</div>`;
  } else {
    $("panel-reasoning").innerHTML = r.map((step, i) =>
      `<div class="reasoning-step"><div class="num">Step ${i+1}</div><pre>${escapeHtml(step)}</pre></div>`
    ).join("");
  }
  $("panel-output").innerHTML = `<pre>${escapeHtml(data.output || "")}</pre>`;
  $("panel-raw").innerHTML = `<pre>${escapeHtml(JSON.stringify(data, null, 2))}</pre>`;
}
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # quieter
        pass

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = INDEX_HTML.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path != "/api/run":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(length) or b"{}")
            provider = req.get("provider")
            prompt = (req.get("prompt") or "").strip()
            if not prompt:
                return self._send_json(400, {"error": "Empty prompt"})

            if provider == "openai":
                if not os.getenv("OPENAI_API_KEY"):
                    return self._send_json(400, {"error": "OPENAI_API_KEY not set"})
                result = call_openai(prompt, req.get("model", "gpt-5.2"), req.get("effort", "medium"))
            elif provider == "anthropic":
                if not os.getenv("ANTHROPIC_API_KEY"):
                    return self._send_json(400, {"error": "ANTHROPIC_API_KEY not set"})
                result = call_anthropic(
                    prompt,
                    req.get("model", "claude-sonnet-4-5-20250929"),
                    int(req.get("budget", 5000)),
                )
            else:
                return self._send_json(400, {"error": f"Unknown provider: {provider}"})

            self._send_json(200, result)
        except Exception as e:
            self._send_json(500, {"error": str(e), "traceback": traceback.format_exc()})


def main():
    print(f"→ Reasoning Explorer running at http://localhost:{PORT}")
    print("  (Ctrl+C to stop)")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
