# /// script
# requires-python = ">=3.11"
# dependencies = ["matplotlib"]
# ///
"""Choosing a reasoning model — a runnable decision aid.

Teaching artifact for deck 01 ("When to reach for a reasoning model").
The slide flowchart answers *whether* to use a reasoning model; this script
answers the next question — *which* current reasoning model, and why.

It does three things:
  1. Prints a side-by-side comparison of the reasoning models this course
     covers (OpenAI gpt-5.5, the o-series, Claude extended thinking, DeepSeek R1).
  2. Recommends one from a short task profile, with a transparent rule it
     prints alongside the pick — so students can see *and edit* the logic.
  3. Optionally ranks the models by a weighted score you control
     (--weights reasoning,speed,cost). This ports the one good idea from the
     old, deleted comparison script — turning preferences into a ranking —
     but builds it on honest tiers instead of invented benchmark numbers.

Numbers here are qualitative tiers (low / med / high), not benchmark claims.
The point is how to choose, not a leaderboard — a single hardcoded score
table rots the moment a model ships. Model facts are current as of 2026-06
(see research/openai-model-currency.md and the deck-01 timeline).

Run:
    python scripts/reasoning_model_selector.py                      # comparison + sample picks
    python scripts/reasoning_model_selector.py --chart              # also save the comparison chart PNG
    python scripts/reasoning_model_selector.py --weights 0.5,0.3,0.2  # weighted ranking: reasoning,speed,cost
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

DIVIDER = "-" * 60
TIER = {1: "low", 2: "med", 3: "high"}

# Generated charts live with the other deck images, not loose in scripts/.
ASSETS_DIR = Path(__file__).resolve().parent.parent / "presentation" / "assets"
DEFAULT_CHART = ASSETS_DIR / "01_reasoning_model_selector.png"


@dataclass(frozen=True)
class ReasoningModel:
    name: str
    provider: str
    effort_control: str  # how you dial reasoning depth
    reasoning: int       # 1 modest .. 3 strongest, at full effort
    latency: int         # 1 fast .. 3 slow, at full reasoning
    cost: int            # 1 cheap .. 3 expensive
    open_weights: bool
    best_for: str


# Current reasoning models the course covers (2026-06).
MODELS: list[ReasoningModel] = [
    ReasoningModel(
        name="gpt-5.5",
        provider="OpenAI",
        effort_control="reasoning.effort = none|low|medium|high|xhigh",
        reasoning=3, latency=2, cost=2, open_weights=False,
        best_for="balanced default — dial effort to fit the task",
    ),
    ReasoningModel(
        name="o4-mini",
        provider="OpenAI",
        effort_control="reasoning.effort (compact)",
        reasoning=2, latency=1, cost=1, open_weights=False,
        best_for="cheap, fast step-by-step at high volume",
    ),
    ReasoningModel(
        name="o3",
        provider="OpenAI",
        effort_control="reasoning.effort + tools in the loop",
        reasoning=3, latency=3, cost=3, open_weights=False,
        best_for="hardest problems; runs tools mid-reasoning",
    ),
    ReasoningModel(
        name="Claude Opus 4.7 (extended thinking)",
        provider="Anthropic",
        effort_control="thinking.budget_tokens = N",
        reasoning=3, latency=2, cost=3, open_weights=False,
        best_for="long, self-checking reasoning + strong writing",
    ),
    ReasoningModel(
        name="DeepSeek R1",
        provider="DeepSeek",
        effort_control="always-on <think> (open recipe)",
        reasoning=3, latency=2, cost=1, open_weights=True,
        best_for="open weights — self-host or study the mechanism",
    ),
]


@dataclass
class TaskProfile:
    """What the task actually demands. Toggle these to change the pick."""
    needs_deep_reasoning: bool = True
    latency_sensitive: bool = False
    cost_sensitive: bool = False
    needs_open_weights: bool = False   # self-host / on-prem / inspect the recipe
    needs_tools_in_loop: bool = False  # search/code/calls *during* reasoning
    writing_heavy: bool = False        # long-form output, verification, drafting


def recommend(task: TaskProfile) -> tuple[str, str]:
    """Transparent decision rules — mirrors and extends the deck-01 flowchart.

    Returns (model_pick, one-line reason). Order matters: the first rule that
    fits wins, so the most constraining requirements are checked first.
    """
    if not task.needs_deep_reasoning:
        return ("Vanilla LLM — or gpt-5.5 at effort=none/low",
                "single-step task: don't pay the reasoning tax (5-50x tokens)")
    if task.needs_open_weights:
        return ("DeepSeek R1",
                "only open-weights reasoner here — self-host / inspect the recipe")
    if task.needs_tools_in_loop:
        return ("OpenAI o3",
                "needs tools running inside the reasoning loop")
    if task.cost_sensitive or task.latency_sensitive:
        return ("OpenAI o4-mini — or gpt-5.5 at effort=low",
                "cost/latency-bound: cheapest fast step-by-step")
    if task.writing_heavy:
        return ("Claude Opus 4.7 (extended thinking)",
                "long, self-checking output — budget thinking tokens")
    return ("gpt-5.5 at effort=medium/high",
            "deep reasoning, no special constraint: the balanced default")


DEFAULT_WEIGHTS = (0.5, 0.25, 0.25)  # reasoning, speed, cost


def parse_weights(spec: str) -> tuple[float, float, float]:
    """Parse 'reasoning,speed,cost' (e.g. '0.5,0.3,0.2') and normalize to sum 1."""
    try:
        parts = [float(x) for x in spec.split(",")]
    except ValueError:
        raise SystemExit(f"--weights: expected numbers like '0.5,0.3,0.2', got {spec!r}")
    if len(parts) != 3 or any(p < 0 for p in parts) or sum(parts) <= 0:
        raise SystemExit("--weights: need 3 non-negative numbers (reasoning,speed,cost)")
    total = sum(parts)
    return tuple(p / total for p in parts)  # type: ignore[return-value]


def weighted_score(model: ReasoningModel, weights: tuple[float, float, float]) -> float:
    """Score in [0,1]; higher is better. Tiers map to 0.33/0.67/1.0. Speed and
    cost are inverted (lower latency/cost is better). Illustrative, not a benchmark."""
    wr, ws, wc = weights
    reasoning = model.reasoning / 3          # high tier -> better
    speed = (4 - model.latency) / 3          # low latency -> better
    cost = (4 - model.cost) / 3              # low cost -> better
    return wr * reasoning + ws * speed + wc * cost


def rank(weights: tuple[float, float, float]) -> list[tuple[ReasoningModel, float]]:
    scored = [(m, weighted_score(m, weights)) for m in MODELS]
    return sorted(scored, key=lambda ms: ms[1], reverse=True)


# A few worked profiles to make the logic concrete.
SAMPLE_TASKS: list[tuple[str, TaskProfile]] = [
    ("Summarize a short email",
     TaskProfile(needs_deep_reasoning=False)),
    ("Grade 50k math solutions overnight",
     TaskProfile(cost_sensitive=True)),
    ("Multi-step research agent that browses + runs code",
     TaskProfile(needs_tools_in_loop=True)),
    ("On-prem deployment, no data leaves the building",
     TaskProfile(needs_open_weights=True)),
    ("Draft + self-verify a long technical proof",
     TaskProfile(writing_heavy=True)),
    ("Hard logic puzzle, latency not a concern",
     TaskProfile()),
]


def print_comparison() -> None:
    print(DIVIDER)
    print("Reasoning models this course covers (current as of 2026-06)")
    print(DIVIDER)
    header = (f"{'Model':<36} {'Provider':<10} {'Reasoning':<10} "
              f"{'Latency':<8} {'Cost':<6} {'Open?':<6}")
    print(header)
    print("-" * len(header))
    for m in MODELS:
        print(f"{m.name:<36} {m.provider:<10} {TIER[m.reasoning]:<10} "
              f"{TIER[m.latency]:<8} {TIER[m.cost]:<6} "
              f"{'yes' if m.open_weights else 'no':<6}")
    print()
    print("Effort control (how you dial reasoning depth):")
    for m in MODELS:
        print(f"  - {m.name}: {m.effort_control}")
    print()
    print("Best for:")
    for m in MODELS:
        print(f"  - {m.name}: {m.best_for}")
    print()


def print_recommendations() -> None:
    print(DIVIDER)
    print("Sample task -> recommended model")
    print(DIVIDER)
    for label, task in SAMPLE_TASKS:
        pick, why = recommend(task)
        print(f"\n• {label}")
        print(f"    -> {pick}")
        print(f"       ({why})")
    print()


def print_ranking(weights: tuple[float, float, float]) -> None:
    wr, ws, wc = weights
    print(DIVIDER)
    print(f"Weighted ranking  (reasoning={wr:.2f}, speed={ws:.2f}, cost={wc:.2f})")
    print(DIVIDER)
    for i, (m, s) in enumerate(rank(weights), 1):
        print(f"{i}. {m.name:<36} score={s:.2f}   "
              f"reasoning={TIER[m.reasoning]}, latency={TIER[m.latency]}, "
              f"cost={TIER[m.cost]}")
    print("\n(Scores are illustrative — derived from qualitative tiers, "
          "not benchmarks. Re-run with your own --weights.)\n")


def make_chart(out_path: Path) -> Path:
    """Comparison matrix (models x axes). Complements the slide flowchart:
    the slide says *whether* to reason; this says *which* model."""
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans", "savefig.dpi": 160,
                         "savefig.bbox": "tight", "figure.facecolor": "white"})
    cols = ["Reasoning", "Latency", "Cost", "Open weights"]
    cell_text, cell_colors = [], []
    good_high = {1: "#ffcdd2", 2: "#fff3c4", 3: "#c8e6c9"}  # high is better
    good_low = {1: "#c8e6c9", 2: "#fff3c4", 3: "#ffcdd2"}   # low is better
    for m in MODELS:
        cell_text.append([TIER[m.reasoning], TIER[m.latency], TIER[m.cost],
                          "yes" if m.open_weights else "no"])
        cell_colors.append([good_high[m.reasoning], good_low[m.latency],
                            good_low[m.cost],
                            "#c8e6c9" if m.open_weights else "#ffcdd2"])

    fig, ax = plt.subplots(figsize=(12.5, 4.2))
    ax.axis("off")
    ax.set_title("Choosing a reasoning model — which one, and why",
                 fontsize=14, fontweight="bold", pad=14)
    table = ax.table(cellText=cell_text, cellColours=cell_colors,
                     rowLabels=[m.name for m in MODELS], colLabels=cols,
                     loc="center", cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 1.9)
    for j in range(len(cols)):
        table[0, j].set_facecolor("#5b8def")
        table[0, j].set_text_props(color="white", fontweight="bold")
    fig.text(0.5, 0.01,
             "Tiers are qualitative, not benchmarks. Pick on constraints "
             "(open weights? tools in loop? cost/latency?), then dial effort. "
             "Rank with --weights reasoning,speed,cost.",
             ha="center", fontsize=9, color="#666", style="italic")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chart", action="store_true",
                        help="also save the comparison chart as a PNG")
    parser.add_argument("--out", type=Path, default=DEFAULT_CHART,
                        help=f"chart output path (default: {DEFAULT_CHART})")
    parser.add_argument("--weights", nargs="?", const="0.5,0.25,0.25",
                        default=None, metavar="R,S,C",
                        help="show a weighted ranking; weights are "
                             "reasoning,speed,cost (default 0.5,0.25,0.25)")
    args = parser.parse_args()

    print_comparison()
    print_recommendations()

    if args.weights is not None:
        print_ranking(parse_weights(args.weights))

    if args.chart:
        out = make_chart(args.out)
        print(DIVIDER)
        print(f"Saved comparison chart -> {out}")
        print(DIVIDER)


if __name__ == "__main__":
    main()
