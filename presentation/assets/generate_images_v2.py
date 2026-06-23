# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Generate v2 slide images for the reasoning-LLMs deck (June 2026 refresh).

Brand palette (Automata Learning Lab):
  Ink Black #000000   Warm Cream #F5F3EB
  Coral #E86B5A  Golden #F5C542  Sage #7CB56B  Sky #5B9BD5
  tints: Coral #FBEAE7  Golden #FEF8E6  Sage #EEF5EC  Sky #E8F1F9
  grays: #DDD9D2 / #8A847A / #5C5750 / #2A2825
Conventions: sharp corners, 2px black borders, monospace for code/labels,
restrained accent use (<=2-3 accents per composition).

Run: uv run presentation/assets/generate_images_v2.py
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

OUT = Path(__file__).parent

# ---- brand tokens ----
INK = "#000000"
CREAM = "#F5F3EB"
WHITE = "#FFFFFF"
CORAL, GOLDEN, SAGE, SKY = "#E86B5A", "#F5C542", "#7CB56B", "#5B9BD5"
CORAL_L, GOLDEN_L, SAGE_L, SKY_L = "#FBEAE7", "#FEF8E6", "#EEF5EC", "#E8F1F9"
G100, G300, G500, G600, G800 = "#F5F4F1", "#DDD9D2", "#8A847A", "#5C5750", "#2A2825"

# font fallback: prefer a clean sans, fall back to DejaVu gracefully
from matplotlib import font_manager
_avail = {f.name for f in font_manager.fontManager.ttflist}
SANS = next((f for f in ["IBM Plex Sans", "Arial", "Helvetica Neue",
                         "DejaVu Sans"] if f in _avail), "DejaVu Sans")
MONO = next((f for f in ["JetBrains Mono", "Menlo", "Courier New",
                         "DejaVu Sans Mono"] if f in _avail), "DejaVu Sans Mono")
plt.rcParams.update({
    "font.family": SANS, "savefig.dpi": 150, "savefig.bbox": "tight",
    "figure.facecolor": WHITE, "savefig.facecolor": WHITE,
})


def save(fig, name):
    fig.savefig(OUT / name)
    plt.close(fig)
    p = OUT / name
    print(f"wrote {name:34s} {'OK' if p.exists() else 'MISSING'} "
          f"({p.stat().st_size//1024} KB)")


def box(ax, cx, cy, w, h, text, fc=WHITE, ec=INK, lw=2.0, fs=11,
        weight="normal", fontfamily=None, tcolor=INK):
    ax.add_patch(mpatches.FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="square,pad=0", fc=fc, ec=ec, lw=lw))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs,
            fontweight=weight, color=tcolor,
            family=fontfamily or SANS, zorder=5)


def arrow(ax, p1, p2, color=INK, lw=2.0):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle="-|>", mutation_scale=18,
        lw=lw, color=color, shrinkA=2, shrinkB=2, zorder=4))


# ============================================================
# 1. reasoning_vs_vanilla.png
# ============================================================
def reasoning_vs_vanilla():
    fig, ax = plt.subplots(figsize=(14, 7.2))
    ax.set_xlim(0, 14); ax.set_ylim(0, 7.2); ax.axis("off")
    ax.text(0.3, 6.95, "Reasoning LLM  =  reasoning chain  +  answer",
            fontsize=18, fontweight="bold", color=INK, va="top")

    # ---- Top row: Traditional LLM ----
    ytop = 5.4
    ax.text(0.3, ytop + 0.95, "Traditional LLM", fontsize=13,
            fontweight="bold", color=G600)
    box(ax, 1.7, ytop, 2.0, 1.0, "input", fc=G100)
    box(ax, 5.0, ytop, 2.2, 1.0, "model", fc=SKY_L, ec=SKY, lw=2.4)
    box(ax, 8.3, ytop, 2.0, 1.0, "output", fc=G100)
    arrow(ax, (2.7, ytop), (3.9, ytop))
    arrow(ax, (6.1, ytop), (7.3, ytop))

    # ---- Bottom row: Reasoning LLM ----
    ybot = 2.7
    ax.text(0.3, ybot + 1.55, "Reasoning LLM", fontsize=13,
            fontweight="bold", color=CORAL)
    box(ax, 1.5, ybot, 1.9, 1.0, "input", fc=G100)
    box(ax, 4.4, ybot, 2.0, 1.0, "model", fc=SKY_L, ec=SKY, lw=2.4)
    arrow(ax, (2.45, ybot), (3.4, ybot))
    arrow(ax, (5.4, ybot), (6.2, ybot))

    # reasoning band
    rband_x, rband_w = 6.3, 4.4
    ax.add_patch(mpatches.FancyBboxPatch(
        (rband_x, ybot - 0.95), rband_w, 1.9, boxstyle="square,pad=0",
        fc=GOLDEN_L, ec=GOLDEN, lw=2.4))
    ax.text(rband_x + rband_w / 2, ybot + 0.62,
            "intermediate reasoning steps", fontsize=10.5,
            fontweight="bold", color=G600, ha="center")
    sx = rband_x + 0.85
    for i in range(3):
        lbl = "..." if i == 2 else f"step {i+1}"
        box(ax, sx, ybot - 0.1, 1.0, 0.7, lbl, fc=WHITE, ec=GOLDEN,
            lw=1.6, fs=9.5, fontfamily=MONO)
        if i < 2:
            arrow(ax, (sx + 0.5, ybot - 0.1), (sx + 1.0, ybot - 0.1),
                  color=GOLDEN, lw=1.6)
        sx += 1.5

    # split to answer + reasoning behind answer
    box(ax, 12.6, ybot + 0.95, 2.4, 0.85, "answer", fc=SAGE_L, ec=SAGE,
        lw=2.4, fs=11, weight="bold")
    box(ax, 12.6, ybot - 0.95, 2.4, 0.85, "reasoning\nbehind answer",
        fc=CORAL_L, ec=CORAL, lw=2.4, fs=10, weight="bold")
    arrow(ax, (rband_x + rband_w, ybot + 0.25), (11.4, ybot + 0.95),
          color=SAGE, lw=2.0)
    arrow(ax, (rband_x + rband_w, ybot - 0.25), (11.4, ybot - 0.95),
          color=CORAL, lw=2.0)

    ax.text(7.0, 0.35, "Output = reasoning chain + answer.",
            fontsize=13, style="italic", color=G600, ha="center")
    save(fig, "reasoning_vs_vanilla.png")


# ============================================================
# 2. thinking_in_the_wild.png  (mock chat-UI cards)
# ============================================================
def thinking_in_the_wild():
    fig, ax = plt.subplots(figsize=(14, 7.6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 7.6); ax.axis("off")
    ax.text(7, 7.25, "Thinking shows up everywhere",
            fontsize=20, fontweight="bold", color=INK, ha="center")
    ax.text(7, 6.78, "illustrative mockups — not real screenshots",
            fontsize=10.5, style="italic", color=G500, ha="center")

    cards = [
        ("ChatGPT",  SKY,   "Thought for 6s",
         "<think>\nbreak into sub-steps,\ncheck units, verify...\n</think>"),
        ("Claude",   CORAL, "Thinking… (expanded)",
         "Let me work through this\nstep by step. First I'll\nidentify what's given..."),
        ("Gemini",   GOLDEN, "Show thinking  v",
         "Considering approaches.\nApproach A fails because\nApproach B is cleaner..."),
        ("DeepSeek", SAGE,  "Thought for 11s",
         "<think>\nthe key constraint is X,\nso the answer must...\n</think>"),
    ]
    cw, ch = 3.05, 4.7
    xs = [0.55, 4.0, 7.45, 10.9]
    cy = 3.55
    for (name, accent, ind, trace), x in zip(cards, xs):
        cx = x + cw / 2
        # card
        ax.add_patch(mpatches.FancyBboxPatch(
            (x, cy - ch / 2), cw, ch, boxstyle="square,pad=0",
            fc=WHITE, ec=INK, lw=2.2))
        # title bar
        ax.add_patch(mpatches.Rectangle(
            (x, cy + ch / 2 - 0.7), cw, 0.7, fc=accent, ec=INK, lw=2.2))
        ax.text(cx, cy + ch / 2 - 0.35, name, fontsize=13,
                fontweight="bold", color=INK, ha="center", va="center")
        # collapsed "Thinking" indicator pill
        py = cy + ch / 2 - 1.35
        ax.add_patch(mpatches.FancyBboxPatch(
            (x + 0.25, py - 0.28), cw - 0.5, 0.56,
            boxstyle="round,pad=0.02,rounding_size=0.12",
            fc=G100, ec=G300, lw=1.4))
        ax.text(x + 0.45, py, ">", fontsize=11, color=G500, va="center",
                fontweight="bold")
        ax.text(x + 0.78, py, ind, fontsize=9.5, color=G600, va="center",
                family=MONO)
        # greyed reasoning trace
        ax.add_patch(mpatches.Rectangle(
            (x + 0.25, cy - ch / 2 + 0.35), cw - 0.5, 2.45,
            fc=G100, ec=G300, lw=1.2))
        ax.text(x + 0.42, cy - ch / 2 + 2.65, trace, fontsize=8.2,
                color=G500, va="top", ha="left", family=MONO)
        # answer hint line
        ax.text(x + 0.42, cy - ch / 2 + 0.18, "→ answer…",
                fontsize=8.5, color=accent, fontweight="bold", va="bottom")
    save(fig, "thinking_in_the_wild.png")


# ============================================================
# 3. timeline_2026.png
# ============================================================
def timeline_2026(events=None):
    if events is None:
        events = TIMELINE_EVENTS
    fig, ax = plt.subplots(figsize=(16, 7.0))
    n = len(events)
    xs = np.arange(n)
    ax.hlines(0, -0.5, n - 0.5, color=INK, lw=2.6)
    # accent cycle restrained to brand 4
    accents = [SKY, CORAL, GOLDEN, SAGE]
    for i, (date, name, why) in enumerate(events):
        accent = accents[i % 4]
        above = (i % 2 == 0)
        y_name = 0.55 if above else -0.55
        y_date = 0.16 if above else -0.16
        y_why = 1.35 if above else -1.35
        ax.plot([i, i], [0, y_name * 0.78], color=accent, lw=1.4, zorder=2)
        ax.plot(i, 0, "o", ms=15, color=accent, mec=INK, mew=1.6, zorder=3)
        ax.text(i, y_date, date, ha="center",
                va="bottom" if above else "top", fontsize=9, color=G600,
                family=MONO)
        ax.text(i, y_name, name, ha="center",
                va="bottom" if above else "top", fontsize=10.5,
                fontweight="bold", color=INK)
        ax.text(i, y_why, why, ha="center",
                va="bottom" if above else "top", fontsize=8, color=G500,
                style="italic")
    ax.set_ylim(-2.05, 2.05)
    ax.set_xlim(-0.8, n - 0.2)
    ax.axis("off")
    ax.set_title("The reasoning-model wave  ·  Sep 2024 → mid 2026",
                 fontsize=17, fontweight="bold", pad=16)
    save(fig, "timeline_2026.png")


# ============================================================
# 4. leaderboard_intelligence.png
# ============================================================
def leaderboard_intelligence(data=None):
    if data is None:
        data = LEADERBOARD
    fig, ax = plt.subplots(figsize=(13.5, 8.0))
    names = [d[0] for d in data][::-1]
    scores = [d[1] for d in data][::-1]
    kinds = [d[2] for d in data][::-1]  # 'p' proprietary, 'o' open
    colors = [SKY if k == "p" else SAGE for k in kinds]
    y = np.arange(len(names))
    ax.barh(y, scores, color=colors, edgecolor=INK, lw=1.6, height=0.66)
    for yi, s in zip(y, scores):
        ax.text(s + 0.6, yi, f"{s:g}", va="center", ha="left",
                fontsize=11, fontweight="bold", color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=11)
    ax.set_xlim(0, max(scores) + 8)
    ax.set_xlabel("Intelligence Index  (composite reasoning score)",
                  fontsize=12)
    ax.set_title("Top reasoning models by intelligence index",
                 fontsize=17, fontweight="bold", pad=12, loc="left")
    ax.grid(axis="x", alpha=0.25)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    # legend
    leg = [mpatches.Patch(fc=SKY, ec=INK, label="proprietary"),
           mpatches.Patch(fc=SAGE, ec=INK, label="open-weights")]
    ax.legend(handles=leg, loc="lower right", fontsize=11, frameon=True)
    ax.text(1.0, -0.075,
            "Source: Artificial Analysis Intelligence Index style · "
            "as of June 2026 · approximate, see notes",
            transform=ax.transAxes, ha="right", fontsize=9,
            color=G500, style="italic")
    save(fig, "leaderboard_intelligence.png")


# ============================================================
# 5. open_vs_proprietary.png  (closing the gap, over time)
# ============================================================
def open_vs_proprietary(series=None):
    if series is None:
        series = GAP_SERIES
    quarters = [s[0] for s in series]
    prop = [s[1] for s in series]
    openw = [s[2] for s in series]
    x = np.arange(len(quarters))
    fig, ax = plt.subplots(figsize=(13.5, 7.4))
    ax.plot(x, prop, "-o", color=SKY, lw=3, ms=9, mec=INK, mew=1.4,
            label="best proprietary")
    ax.plot(x, openw, "-s", color=SAGE, lw=3, ms=9, mec=INK, mew=1.4,
            label="best open-weights")
    ax.fill_between(x, openw, prop, color=GOLDEN_L, alpha=0.7, zorder=0)
    # gap annotations at first and last
    for idx in (0, len(x) - 1):
        gap = prop[idx] - openw[idx]
        ax.annotate(f"gap ≈ {gap:g}",
                    xy=(x[idx], (prop[idx] + openw[idx]) / 2),
                    fontsize=10.5, color=G600, ha="center",
                    fontweight="bold",
                    bbox=dict(boxstyle="round,pad=0.3", fc=WHITE,
                              ec=GOLDEN, lw=1.4))
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=11)
    ax.set_ylabel("Intelligence Index", fontsize=12)
    ax.set_title("Closing the gap: open-weights vs proprietary reasoning",
                 fontsize=17, fontweight="bold", pad=12, loc="left")
    ax.grid(alpha=0.25)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
    ax.legend(fontsize=12, loc="lower right", frameon=True)
    ax.text(1.0, -0.12,
            "Source: Artificial Analysis style intelligence scores · "
            "as of June 2026 · approximate",
            transform=ax.transAxes, ha="right", fontsize=9,
            color=G500, style="italic")
    save(fig, "open_vs_proprietary.png")


# ============================================================
# 6. choosing_criteria.png
# ============================================================
def choosing_criteria():
    fig, ax = plt.subplots(figsize=(14, 6.2))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6.2); ax.axis("off")
    ax.text(7, 5.85, "Choosing a reasoning model — 5 criteria",
            fontsize=19, fontweight="bold", color=INK, ha="center")
    items = [
        ("1", "Reasoning\nquality", "can it crack the\nhard problems?", SKY),
        ("2", "Price", "$/M tokens\nin & out", CORAL),
        ("3", "Built-in\nknowledge", "what it knows\nout of the box", GOLDEN),
        ("4", "Speed /\nlatency", "time-to-answer\nunder load", SAGE),
        ("5", "Context\nwindow", "how much it can\nhold at once", SKY),
    ]
    cw, gap = 2.45, 0.28
    total = len(items) * cw + (len(items) - 1) * gap
    x0 = (14 - total) / 2
    cy = 2.9
    for i, (num, title, sub, accent) in enumerate(items):
        x = x0 + i * (cw + gap)
        cx = x + cw / 2
        ax.add_patch(mpatches.Rectangle((x, cy - 1.8), cw, 3.6,
                     fc=WHITE, ec=INK, lw=2.2))
        # accent number chip
        ax.add_patch(mpatches.Rectangle((x, cy + 1.0), cw, 0.8,
                     fc=accent, ec=INK, lw=2.2))
        ax.text(cx, cy + 1.4, num, fontsize=20, fontweight="bold",
                color=INK, ha="center", va="center")
        ax.text(cx, cy + 0.2, title, fontsize=13, fontweight="bold",
                color=INK, ha="center", va="center")
        ax.text(cx, cy - 1.1, sub, fontsize=9.5, color=G600,
                ha="center", va="center", style="italic")
    save(fig, "choosing_criteria.png")


# ============================================================
# 7. when_to_use.png
# ============================================================
def when_to_use():
    fig, ax = plt.subplots(figsize=(14, 7.2))
    ax.set_xlim(0, 14); ax.set_ylim(0, 7.2); ax.axis("off")
    ax.text(7, 6.9, "When to reach for a reasoning model",
            fontsize=19, fontweight="bold", color=INK, ha="center")

    good = [
        "Complex, single-shot problems",
        "Fewer hallucinations needed",
        "Diagnosis-style reasoning",
        "Explanations & step-by-step",
        "Hard problems other LLMs fail",
    ]
    poor = [
        "Speed / latency-critical tasks",
        "Cheap bulk extraction",
        "High-volume summarization",
        "Simple lookups & formatting",
        "Tight per-call cost budgets",
    ]
    cols = [
        ("GOOD FIT", good, SAGE, SAGE_L, "+"),
        ("POOR FIT", poor, G500, G100, "-"),
    ]
    cw = 6.0
    for (title, items, accent, tint, mark), x in zip(cols, [0.7, 7.3]):
        cx = x + cw / 2
        ax.add_patch(mpatches.Rectangle((x, 0.6), cw, 5.6,
                     fc=WHITE, ec=INK, lw=2.4))
        ax.add_patch(mpatches.Rectangle((x, 5.3), cw, 0.9,
                     fc=accent, ec=INK, lw=2.4))
        ax.text(cx, 5.75, title, fontsize=16, fontweight="bold",
                color=WHITE if accent != G500 else WHITE,
                ha="center", va="center")
        for j, it in enumerate(items):
            yy = 4.6 - j * 0.78
            ax.add_patch(mpatches.Rectangle((x + 0.35, yy - 0.28), 0.5, 0.5,
                         fc=tint, ec=accent, lw=1.6))
            ax.text(x + 0.6, yy - 0.03, mark, fontsize=12,
                    fontweight="bold", color=accent, ha="center",
                    va="center")
            ax.text(x + 1.1, yy - 0.03, it, fontsize=12, color=G800,
                    va="center", ha="left")
    save(fig, "when_to_use.png")


# ============================================================
# 8. agent_prompt_anatomy.png
# ============================================================
def agent_prompt_anatomy():
    fig, ax = plt.subplots(figsize=(12, 8.4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8.4); ax.axis("off")
    ax.text(6, 8.05, "Prompt it like an agent, not a model",
            fontsize=19, fontweight="bold", color=INK, ha="center")

    sections = [
        ("Goal", "What you ultimately want accomplished.", SKY),
        ("Return format", "Exact structure / schema of the output.", CORAL),
        ("Warnings", "Edge cases, what to avoid, constraints.", GOLDEN),
        ("Context", "Background, data, prior state.", SAGE),
        ("Tools", "web search · code interpreter · retrieval", SKY),
        ("Actions", "Steps it may take to reach the goal.", CORAL),
    ]
    card_x, card_w = 1.3, 9.4
    top, row_h, pad = 7.1, 0.92, 0.12
    # outer card
    n = len(sections)
    ax.add_patch(mpatches.Rectangle(
        (card_x - 0.2, top - n * row_h - pad * (n - 1) - 0.25),
        card_w + 0.4, n * row_h + pad * (n - 1) + 0.5,
        fc=WHITE, ec=INK, lw=2.6))
    for i, (label, desc, accent) in enumerate(sections):
        y = top - i * (row_h + pad) - row_h / 2
        ax.add_patch(mpatches.Rectangle(
            (card_x, y - row_h / 2), card_w, row_h,
            fc=CREAM, ec=INK, lw=1.6))
        # accent tab
        ax.add_patch(mpatches.Rectangle(
            (card_x, y - row_h / 2), 0.22, row_h, fc=accent, ec="none"))
        ax.text(card_x + 0.5, y, label, fontsize=13, fontweight="bold",
                color=INK, va="center", ha="left", family=MONO)
        ax.text(card_x + 3.5, y, desc, fontsize=10.5, color=G600,
                va="center", ha="left")
    ax.text(6, 0.35, "You're prompting an agent now.",
            fontsize=14, style="italic", fontweight="bold",
            color=CORAL, ha="center")
    save(fig, "agent_prompt_anatomy.png")


# ============================================================
# 9. cot_paper_fig1.png  (faithful stylized recreation)
# ============================================================
def cot_paper_fig1():
    fig, ax = plt.subplots(figsize=(14, 6.6))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6.6); ax.axis("off")
    ax.text(7, 6.35, "Chain-of-thought prompting elicits reasoning",
            fontsize=17, fontweight="bold", color=INK, ha="center")
    ax.text(7, 5.92, "recreation — after Wei et al., 2022 "
            "(arXiv:2201.11903)", fontsize=10, style="italic",
            color=G500, ha="center")

    Q = ("Q: Roger has 5 tennis balls. He buys 2 more\n"
         "cans of 3 balls each. How many does he\n"
         "have now?")
    panels = [
        # title, x, accent, answer-tint, answer-edge, answer text, mark
        ("Standard prompting", 0.6, SKY, CORAL_L, CORAL,
         "A: The answer is 11.\n\n   (no working shown)  X", "wrong"),
        ("Chain-of-thought prompting", 7.2, SAGE, SAGE_L, SAGE,
         "A: Roger started with 5 balls. 2 cans of\n"
         "   3 balls each is 6 balls. 5 + 6 = 11.\n"
         "   The answer is 11.  /", "right"),
    ]
    pw = 6.2
    for title, x, accent, atint, aedge, atext, _ in panels:
        cx = x + pw / 2
        ax.add_patch(mpatches.Rectangle((x, 0.5), pw, 4.9,
                     fc=WHITE, ec=INK, lw=2.4))
        ax.add_patch(mpatches.Rectangle((x, 4.7), pw, 0.7,
                     fc=accent, ec=INK, lw=2.4))
        ax.text(cx, 5.05, title, fontsize=13, fontweight="bold",
                color=WHITE, ha="center", va="center")
        # question block (model input, neutral)
        ax.add_patch(mpatches.Rectangle((x + 0.3, 3.05), pw - 0.6, 1.45,
                     fc=G100, ec=G300, lw=1.4))
        ax.text(x + 0.5, 4.32, Q, fontsize=9, family=MONO,
                color=G800, va="top", ha="left")
        # answer block
        ax.add_patch(mpatches.Rectangle((x + 0.3, 0.8), pw - 0.6, 2.0,
                     fc=atint, ec=aedge, lw=1.8))
        ax.text(x + 0.5, 2.6, atext, fontsize=9, family=MONO,
                color=G800, va="top", ha="left")
    ax.text(3.7, 0.16, "no reasoning -> wrong", fontsize=10,
            color=CORAL, ha="center", style="italic", fontweight="bold")
    ax.text(10.3, 0.16, "reasoning steps -> right", fontsize=10,
            color=SAGE, ha="center", style="italic", fontweight="bold")
    save(fig, "cot_paper_fig1.png")


# ============================================================
# DATA (June 2026 research — see PART B report)
# ============================================================
# Artificial Analysis Intelligence Index (approximate, ~June 2026)
# Composite score (~0-65 scale). Top values from AA articles; rest [approx].
LEADERBOARD = [
    ("Claude Opus 4.8",        61.4, "p"),
    ("GPT-5.5 (xhigh)",        60.2, "p"),
    ("Claude Opus 4.7",        53.5, "p"),
    ("GPT-5.4",                51.4, "p"),
    ("GLM-5.2 (open)",         51.0, "o"),
    ("Gemini 3.5 Flash",       50.2, "p"),
    ("Gemini 3.1 Pro",         46.5, "p"),
    ("Qwen 3.7 Max (open)",    46.0, "o"),
    ("MiniMax M3 (open)",      44.4, "o"),
    ("DeepSeek V4 Pro (open)", 44.3, "o"),
    ("Claude Opus 4.6",        43.7, "p"),
    ("Grok 4.3",               37.6, "p"),
]

# chronological milestones for the timeline (date label, name, blurb)
TIMELINE_EVENTS = [
    ("Sep 2024", "OpenAI\no1-preview",   "first public\nreasoning model"),
    ("Dec 2024", "Gemini 2.0\nFlash Thinking", "Google's first\nthinking model"),
    ("Jan 2025", "DeepSeek\nR1",         "open recipe\n@ o1 level"),
    ("Feb 2025", "Claude\n3.7 Sonnet",   "hybrid thinking\ntoggle"),
    ("Mar 2025", "Gemini\n2.5 Pro",      "thinking\nbuilt-in"),
    ("Apr 2025", "OpenAI\no3 / o4-mini", "tools inside\nthe reasoning loop"),
    ("May 2025", "Claude 4\nOpus / Sonnet", "extended\nthinking"),
    ("Aug 2025", "OpenAI\nGPT-5",        "unified router\n(fast + think)"),
    ("Nov 2025", "Gemini 3 Pro\n+ Opus 4.5", "frontier multimodal\nreasoning"),
    ("Apr 2026", "OpenAI\nGPT-5.5",      "briefly tops the\nAA index (xhigh)"),
    ("Apr 2026", "DeepSeek\nV4 Pro",     "near-frontier,\n~1/34th the cost"),
    ("May 2026", "Claude\nOpus 4.8",     "current AA leader\n(61.4)"),
    ("Jun 2026", "GLM-5.2\n(open)",      "top open-weights\nmodel (51)"),
]

# closing-the-gap series: (quarter, best proprietary, best open-weights)
# AA-style intelligence index; endpoints anchored to Opus 4.8 (61.4) vs
# GLM-5.2 (51) -> ~10-pt gap, down from ~20-25 pts in late 2024 [approx]
GAP_SERIES = [
    ("Q4'24", 42, 18),
    ("Q1'25", 47, 30),
    ("Q3'25", 53, 41),
    ("Q1'26", 58, 47),
    ("Q2'26", 61, 51),
]


if __name__ == "__main__":
    reasoning_vs_vanilla()
    thinking_in_the_wild()
    timeline_2026()
    leaderboard_intelligence()
    open_vs_proprietary()
    choosing_criteria()
    when_to_use()
    agent_prompt_anatomy()
    cot_paper_fig1()
    print("done")
