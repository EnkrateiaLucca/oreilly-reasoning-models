# GRPO vs PPO

Both optimize the same clipped policy-ratio objective with a KL leash; they differ in **how the advantage is estimated** and **what extra model must be trained**.

**Similarities:** both use the new/old policy ratio `ρ = π_θ/π_θold` and a `clip(ρ, 1−ε, 1+ε)` mechanism to keep updates small.

**Differences:**

| | PPO | GRPO |
|---|---|---|
| Advantage | from a **Value Model** + GAE (generalized advantage estimation), per-token | **group-relative**: reward − group mean (÷ std), shared across all tokens of an output |
| Value/critic network | **trained** (extra cost) | **none** — eliminated |
| KL term | folded **into the reward** before GAE | a **separate term in the objective** (−β·KL to reference) |
| Models trained | Policy **and** Value | Policy **only** |
| Models frozen | Reference, Reward | Reference, Reward |

**Why GRPO wins for reasoning:** dropping the jointly-trained value function is a big compute/memory saving, and the group baseline naturally contextualizes reward (a correct answer to a *hard* problem — where most group samples fail — gets a larger advantage than to an easy one).

In the reasoning setting the "Reward Model" is replaced by a [[verifiable rewards|verifiable reward]], so PPO's and GRPO's reward boxes are identical there.

Related: [[GRPO]] · [[KL regularization in RL fine-tuning]] · [[GRPO advantage refinements]]

_Source: Stanford CME295 Fall 2025, Lecture 6; Shao et al. 2024 (DeepSeekMath); PPO Schulman et al. 2017._
