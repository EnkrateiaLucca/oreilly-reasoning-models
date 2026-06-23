# KL regularization in RL fine-tuning

During the RL stage we don't want the policy to drift too far from a trusted starting point — it has already learned a lot and we only want to *nudge* it. A **KL-divergence penalty** enforces this "stay close" constraint.

Two reference points it can be measured against:
- the **old policy** (previous RL iteration) — limits per-step change;
- the **base / SFT (reference) model** — limits total drift from the well-behaved starting model. Modern RLHF/reasoning training typically uses the **reference (SFT) model**.

Where the KL lives differs by algorithm:
- **PPO:** KL is folded **into the reward** (per-token) before advantage estimation.
- **GRPO:** KL is a **separate explicit term** `−β·KL(π_θ ‖ π_ref)` in the objective.

The clipping mechanism (`clip(ρ, 1−ε, 1+ε)`) is a *second*, complementary brake that bounds the policy-ratio update size.

Related: [[GRPO]] · [[GRPO vs PPO]] · [[GRPO advantage refinements]]

_Source: Stanford CME295 Fall 2025, Lecture 6._
