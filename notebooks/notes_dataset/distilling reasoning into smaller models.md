# Distilling reasoning into smaller models

How to give a *small* model the capability of a large reasoning model without running expensive RL on it.

**Classic distillation** (earlier lectures): teacher and student see the same input; the student is trained to **match the teacher's next-token probability distribution** (logit matching) on fixed data.

**Reasoning distillation** (a different flavor, used for R1-Distill): there are no ready-made reasoning SFT pairs, so:
1. Use the teacher **R1** to *generate* full sample responses **including `<think>` reasoning traces** (done offline).
2. **SFT** the smaller student on those **entire generated token sequences** — just predict the same sequence, not the distribution.

So it's **plain SFT on the teacher's generated reasoning traces**, not logit matching.

**Key finding:** at small scale, **distillation beats RL-from-scratch.** Same Qwen-32B base — R1-Zero-style RL gives AIME 47.0, but distilling from R1 gives AIME **72.6** (and better across MATH-500/GPQA/LiveCodeBench). Distilled models also rival o1-mini. → a better use of compute for small models.

Related: [[DeepSeek R1 training pipeline]] · [[why SFT is a poor start for reasoning]] · [[DeepSeek R1-Zero]]

_Source: Stanford CME295 Fall 2025, Lecture 6; DeepSeek-R1 (2025)._
