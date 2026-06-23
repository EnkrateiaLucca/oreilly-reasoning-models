# GRPO length-normalization bias

The GRPO objective normalizes each output's contribution by its own length — the **`1/|oᵢ|` factor** in `(1/G) Σᵢ (1/|oᵢ|) Σ_t (…)`. Because of it, **per-token gradient magnitude is larger for short outputs and smaller for long ones**.

Effect on updates (arrow size = update magnitude):

| | advantage > 0 (good) | advantage < 0 (bad) |
|---|---|---|
| **short output** | big ↑ | **big ↓** |
| **long output** | small ↑ | small ↓ |

The **bad incentive** is the A<0 column: a *short* wrong answer is penalized hard, but a *long* wrong answer is barely penalized. So the model learns to **prefer longer bad outputs** — a leading hypothesis for the runaway [[output length growth during RL]].

Fixed by equalizing token-level contributions → [[DAPO and Dr. GRPO]].

Related: [[GRPO]] · [[output length growth during RL]] · [[DAPO and Dr. GRPO]]

_Source: Stanford CME295 Fall 2025, Lecture 6._
