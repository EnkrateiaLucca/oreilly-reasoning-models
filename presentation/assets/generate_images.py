# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy"]
# ///
"""Generate synthetic slide images for the reasoning LLMs deck.

The four paper-derived images (AIME curve, aha moment, GRPO objective,
distillation table) are cropped directly from arxiv.org/pdf/2501.12948
with a separate pymupdf step — not generated here.

Run: uv run presentation/assets/generate_images.py
"""
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

OUT = Path(__file__).parent
plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 160,
                     "savefig.bbox": "tight", "figure.facecolor": "white"})


def save(fig, name):
    fig.savefig(OUT / name)
    plt.close(fig)
    print("wrote", name)


# ---------- 01: direct vs thinking ----------
def direct_vs_thinking():
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    for ax in axes:
        ax.set_xticks([]); ax.set_yticks([])
    axes[0].set_title("GPT-4 — direct answer", fontsize=13, fontweight="bold")
    axes[0].text(0.05, 0.9,
        "Q: A train leaves Lisbon at 3pm\n"
        "   going 80 km/h. Another leaves\n"
        "   Porto at 4pm going 100 km/h.\n"
        "   When do they meet?\n\n"
        "A: They meet at 5:30pm.",
        family="monospace", va="top", fontsize=11)
    for s in axes[0].spines.values(): s.set_edgecolor("#bbb")

    axes[1].set_title("o1 / R1 — with <think> trace", fontsize=13, fontweight="bold")
    axes[1].text(0.05, 0.95,
        "<think>\n"
        " Distance Lisbon↔Porto ≈ 300 km.\n"
        " At 3pm train A starts. By 4pm\n"
        " it has gone 80 km, so 220 km\n"
        " remain. Closing speed 180 km/h.\n"
        " t = 220/180 ≈ 1.22 h ≈ 1h13m.\n"
        " 4pm + 1h13m = 5:13pm.\n"
        "</think>\n\n"
        "A: They meet around 5:13pm.",
        family="monospace", va="top", fontsize=10,
        bbox=dict(facecolor="#f3f7ff", edgecolor="#5b8def"))
    for s in axes[1].spines.values(): s.set_edgecolor("#bbb")
    save(fig, "01_direct_vs_thinking.png")


# ---------- 01: timeline ----------
def timeline():
    """Curated reasoning-model milestones, Sep 2024 → Sep 2025.
    Labels stagger above/below the line to fit 10 entries legibly.
    """
    fig, ax = plt.subplots(figsize=(15, 5.5))
    events = [
        ("2024-09", "OpenAI\no1-preview",   "first public\nreasoning model"),
        ("2024-11", "Qwen\nQwQ-32B",        "first open\nreasoning weights"),
        ("2025-01", "DeepSeek\nR1",         "open recipe\n@ o1 level"),
        ("2025-02", "xAI\nGrok 3",          "\"Think\" mode"),
        ("2025-02", "Claude\n3.7 Sonnet",   "hybrid\nthinking toggle"),
        ("2025-03", "Gemini\n2.5 Pro",      "thinking\nbuilt-in"),
        ("2025-04", "OpenAI\no3 / o4-mini", "tools inside\nthe reasoning loop"),
        ("2025-04", "Qwen3",                "open hybrid\nthinking family"),
        ("2025-06", "Mistral\nMagistral",   "first European\nreasoning model"),
        ("2025-08", "OpenAI\nGPT-5",        "unified router\n(fast + think)"),
    ]
    n = len(events)
    xs = np.arange(n)
    ax.hlines(0, -0.5, n - 0.5, color="#333", lw=2.2)

    for i, (date, name, why) in enumerate(events):
        above = (i % 2 == 0)
        y_dot = 0
        y_name =  0.45 if above else -0.45
        y_date =  0.18 if above else -0.18
        y_why  =  1.05 if above else -1.05
        ax.plot(i, y_dot, "o", ms=14, color="#5b8def", zorder=3)
        # connector from dot to label
        ax.plot([i, i], [y_dot, y_name], color="#5b8def", lw=1, zorder=2)
        ax.text(i, y_date, date, ha="center",
                va="bottom" if above else "top",
                fontsize=9, color="#555")
        ax.text(i, y_name, name, ha="center",
                va="bottom" if above else "top",
                fontsize=10, fontweight="bold")
        ax.text(i, y_why, why, ha="center",
                va="bottom" if above else "top",
                fontsize=8, color="#666", style="italic")

    ax.set_ylim(-1.7, 1.7)
    ax.set_xlim(-0.8, n - 0.2)
    ax.axis("off")
    ax.set_title("The reasoning-model wave  ·  Sep 2024 → Aug 2025",
                 fontsize=15, fontweight="bold", pad=18)
    save(fig, "01_timeline.png")


# ---------- 01: decision chart ----------
def decision_chart():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")
    ax.set_title("When to reach for a reasoning model", fontsize=14, fontweight="bold")

    def box(x, y, w, h, text, color="#e8f0ff", edge="#5b8def"):
        ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h,
            boxstyle="round,pad=0.1", fc=color, ec=edge, lw=1.8))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=10)

    def arrow(x1, y1, x2, y2, label=""):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color="#555"))
        if label:
            ax.text((x1 + x2) / 2 + 0.15, (y1 + y2) / 2, label, fontsize=9, color="#555")

    box(3.5, 6.5, 3, 1, "Task needs\nmulti-step reasoning?")
    box(0.3, 4, 3, 1, "Vanilla LLM\n+ step-by-step", color="#f0f0f0", edge="#888")
    box(6.7, 4, 3, 1, "Latency-critical?")
    box(4.2, 1.8, 3, 1, "Low effort\n(o1-mini / R1-Distill)")
    box(7.3, 0.3, 2.5, 1, "Full reasoning\n(o1 / R1)")

    arrow(4.5, 6.5, 2.3, 5.0, "no")
    arrow(6.0, 6.5, 8.0, 5.0, "yes")
    arrow(7.5, 4.0, 6.0, 2.8, "yes")
    arrow(8.8, 4.0, 8.5, 1.3, "no")
    save(fig, "01_decision_chart.png")


# ---------- 02: aha moment ----------
def aha_moment():
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.axis("off")
    ax.set_title('The "aha moment" — emergent self-correction',
                 fontsize=14, fontweight="bold")
    text = (
        "...so the derivative is 2x + 3.\n"
        "Plugging in x = 4 gives 11.\n\n"
        "Wait — let me reconsider. I think I\n"
        "mis-read the problem. The function was\n"
        "f(x) = x² + 3x + 1, so f'(x) = 2x + 3,\n"
        "and f'(4) = 11. Actually that's correct.\n\n"
        "Hmm, let me double-check by computing\n"
        "from first principles..."
    )
    ax.text(0.5, 0.45, text, ha="center", va="center", family="monospace",
            fontsize=12,
            bbox=dict(facecolor="#fff8e1", edgecolor="#f5a623", lw=2, pad=15))
    ax.text(0.5, 0.02, "illustrative — after DeepSeek R1 paper, Fig. 3",
            ha="center", fontsize=9, color="#888", style="italic",
            transform=ax.transAxes)
    save(fig, "02_aha_moment.png")


# ---------- 02: AIME accuracy curve ----------
def aime_curve():
    fig, ax = plt.subplots(figsize=(9, 5))
    steps = np.linspace(0, 8000, 200)
    acc = 15 + 56 * (1 - np.exp(-steps / 2500)) + np.random.default_rng(1).normal(0, 1.0, 200)
    ax.plot(steps, acc, color="#5b8def", lw=2)
    ax.axhline(71, ls="--", color="#888", lw=1)
    ax.text(100, 72.5, "o1-0912 (71.0)", fontsize=10, color="#555")
    ax.set_xlabel("RL training steps", fontsize=12)
    ax.set_ylabel("AIME 2024 pass@1 (%)", fontsize=12)
    ax.set_title("R1-Zero: accuracy emerges from pure RL",
                 fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.text(0.02, 0.97, "illustrative (after R1 Fig. 2)",
            transform=ax.transAxes, fontsize=9, color="#888",
            style="italic", va="top")
    save(fig, "02_aime_curve.png")


# ---------- 02: GRPO objective ----------
def grpo_objective():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.axis("off")
    ax.set_title("GRPO objective (DeepSeek R1 §2.2.1)",
                 fontsize=14, fontweight="bold", pad=20)
    eq = (
        r"$\mathcal{J}_{GRPO}(\theta) = \mathbb{E}_{q,\{o_i\}}"
        r"\Big[\frac{1}{G}\sum_{i=1}^{G}"
        r"\min\Big(r_i(\theta)\hat{A}_i,\ "
        r"\mathrm{clip}(r_i(\theta),1-\epsilon,1+\epsilon)\hat{A}_i\Big)"
        r"- \beta\, D_{KL}(\pi_\theta\|\pi_{ref})\Big]$"
    )
    ax.text(0.5, 0.65, eq, ha="center", va="center", fontsize=15)
    ax.text(0.5, 0.25,
            r"$\hat{A}_i = \dfrac{R_i - \mathrm{mean}(R)}{\mathrm{std}(R)}$"
            "     — group-relative advantage, no critic",
            ha="center", va="center", fontsize=13)
    ax.text(0.5, 0.03,
            "Sample G completions per prompt · reward against the group mean",
            ha="center", fontsize=10, color="#555", style="italic")
    save(fig, "02_grpo_objective.png")


# ---------- 02: distillation table ----------
def distillation_table():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.axis("off")
    ax.set_title("Distillation: small models inherit the reasoning",
                 fontsize=14, fontweight="bold", pad=15)
    cols = ["Model", "AIME 2024", "MATH-500", "GPQA", "LiveCode"]
    rows = [
        ["GPT-4o-0513",              "9.3",  "74.6", "49.9", "32.9"],
        ["Claude-3.5-Sonnet-1022",   "16.0", "78.3", "65.0", "38.9"],
        ["OpenAI o1-mini",           "63.6", "90.0", "60.0", "53.8"],
        ["DeepSeek-R1-Distill-Qwen-7B", "55.5", "92.8", "49.1", "37.6"],
        ["DeepSeek-R1-Distill-Qwen-32B","72.6","94.3","62.1","57.2"],
    ]
    table = ax.table(cellText=rows, colLabels=cols, loc="center",
                     cellLoc="center", colLoc="center")
    table.auto_set_font_size(False); table.set_fontsize(11)
    table.scale(1, 1.7)
    for i in range(len(cols)):
        table[0, i].set_facecolor("#5b8def")
        table[0, i].set_text_props(color="white", fontweight="bold")
    for i in (4, 5):
        for j in range(len(cols)):
            table[i, j].set_facecolor("#e8f0ff")
    ax.text(0.5, 0.02, "illustrative — after R1 paper, Table 5",
            ha="center", fontsize=9, color="#888", style="italic",
            transform=ax.transAxes)
    save(fig, "02_distillation_table.png")


# ---------- 02: 5-stage recipe diagram ----------
def recipe_diagram():
    fig, ax = plt.subplots(figsize=(13, 3.5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 3); ax.axis("off")
    ax.set_title("The R1 recipe — 5 stages", fontsize=14, fontweight="bold")
    stages = ["Pretrain", "Cold-start\nSFT", "RL\n(GRPO)",
              "Rejection-\nsampling SFT", "Distillation"]
    colors = ["#c8d6ff", "#a3b9ff", "#7c9cff", "#5b8def", "#3e6dd1"]
    w = 2.1; gap = 0.35
    for i, (s, c) in enumerate(zip(stages, colors)):
        x = 0.3 + i * (w + gap)
        ax.add_patch(mpatches.FancyBboxPatch((x, 0.8), w, 1.3,
            boxstyle="round,pad=0.08", fc=c, ec="#2a4a9c", lw=1.5))
        ax.text(x + w / 2, 1.45, s, ha="center", va="center",
                fontsize=12, fontweight="bold",
                color="white" if i >= 2 else "#222")
        if i < 4:
            ax.annotate("", xy=(x + w + gap, 1.45), xytext=(x + w, 1.45),
                        arrowprops=dict(arrowstyle="->", lw=2, color="#2a4a9c"))
    save(fig, "02_recipe_diagram.png")


# ---------- 02: GRPO intuition diagram ----------
def grpo_intuition():
    """One prompt → G rollouts → rule-based rewards → group-relative
    advantages. Meant to make the formula slide's notation click."""
    fig, ax = plt.subplots(figsize=(13, 6.5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis("off")
    ax.set_title("GRPO in one picture — the group IS the baseline",
                 fontsize=15, fontweight="bold", pad=12)

    # Prompt box
    ax.add_patch(mpatches.FancyBboxPatch((0.3, 3.3), 2.3, 1.4,
        boxstyle="round,pad=0.1", fc="#e8f0ff", ec="#5b8def", lw=1.8))
    ax.text(1.45, 4.0, "Prompt q\n\"Solve 2x+3=11\"",
            ha="center", va="center", fontsize=10)

    # G rollouts with rewards
    rollouts = [
        ("o₁: ... x=4 ✓",  "r=1.0", 6.3, "#c8e6c9", "#2e7d32"),
        ("o₂: ... x=4 ✓",  "r=1.0", 4.9, "#c8e6c9", "#2e7d32"),
        ("o₃: ... x=5 ✗",  "r=0.0", 3.5, "#ffcdd2", "#c62828"),
        ("o₄: ... x=4 ✓",  "r=1.0", 2.1, "#c8e6c9", "#2e7d32"),
        ("o₅: ... x=3 ✗",  "r=0.0", 0.7, "#ffcdd2", "#c62828"),
    ]
    for text, rlabel, y, fc, ec in rollouts:
        ax.add_patch(mpatches.FancyBboxPatch((3.7, y), 3.2, 1.0,
            boxstyle="round,pad=0.08", fc=fc, ec=ec, lw=1.3))
        ax.text(5.3, y + 0.5, text, ha="center", va="center",
                fontsize=10, family="monospace")
        ax.text(7.25, y + 0.5, rlabel, ha="left", va="center",
                fontsize=10, fontweight="bold", color=ec)
        # arrow from prompt
        ax.annotate("", xy=(3.65, y + 0.5), xytext=(2.65, 4.0),
                    arrowprops=dict(arrowstyle="->", lw=1.2, color="#999"))

    # Group stats
    ax.add_patch(mpatches.FancyBboxPatch((8.5, 3.1), 2.0, 1.8,
        boxstyle="round,pad=0.1", fc="#fff8e1", ec="#f5a623", lw=1.6))
    ax.text(9.5, 4.55, "group stats", ha="center", fontsize=9, color="#8a6d3b")
    ax.text(9.5, 4.15, "mean = 0.6", ha="center", fontsize=10,
            family="monospace")
    ax.text(9.5, 3.75, "std ≈ 0.49", ha="center", fontsize=10,
            family="monospace")
    ax.text(9.5, 3.35, "no critic!", ha="center", fontsize=9,
            style="italic", color="#8a6d3b")

    for _, _, y, _, _ in rollouts:
        ax.annotate("", xy=(8.45, 4.0), xytext=(6.95, y + 0.5),
                    arrowprops=dict(arrowstyle="->", lw=0.8, color="#bbb"))

    # Advantages
    advs = [
        ("A₁ = +0.82", 6.3, "#2e7d32"),
        ("A₂ = +0.82", 4.9, "#2e7d32"),
        ("A₃ = −1.22", 3.5, "#c62828"),
        ("A₄ = +0.82", 2.1, "#2e7d32"),
        ("A₅ = −1.22", 0.7, "#c62828"),
    ]
    for label, y, color in advs:
        ax.text(11.3, y + 0.5, label, ha="left", va="center",
                fontsize=11, fontweight="bold", color=color,
                family="monospace")
        ax.annotate("", xy=(11.25, y + 0.5), xytext=(10.55, 4.0),
                    arrowprops=dict(arrowstyle="->", lw=0.8, color="#bbb"))

    # Stage labels
    for x, label in [(1.45, "1. sample"),
                     (5.3,  "2. score with rules"),
                     (9.5,  "3. group baseline"),
                     (11.8, "4. z-score advantage")]:
        ax.text(x, 7.5, label, ha="center", fontsize=10,
                fontweight="bold", color="#333")

    # Footer
    ax.text(6.5, 0.05,
            "Push policy ↑ toward better-than-average completions, "
            "↓ away from worse-than-average.  That's GRPO.",
            ha="center", fontsize=10, style="italic", color="#555")
    save(fig, "02_grpo_intuition.png")


if __name__ == "__main__":
    direct_vs_thinking()
    timeline()
    decision_chart()
    recipe_diagram()
    grpo_intuition()
    print("done")
