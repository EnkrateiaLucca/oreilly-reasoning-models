# Chain-of-thought as test-time compute

Chain-of-thought (CoT) = make the model **explain its reasoning before answering** (Wei et al., 2022). The core idea behind reasoning models is **"do CoT, but at a much larger scale."**

Two intuitions for *why* generating a reasoning chain helps:
1. **Decomposition.** A hard problem is unlikely to appear verbatim in training. Breaking it into smaller sub-problems lets the model fall back on patterns it *has* seen — like a student linking a new problem to studied ones.
2. **More compute.** Every generated token is another full forward pass. Letting the model emit more reasoning tokens literally buys it more computation before committing to an answer. This budget is the **"compute budget" / test-time scaling**.

The behavior is *organic*: extended CoT and self-correction ("wait, that's wrong…") emerge from RL on [[verifiable rewards]], not only from CoT fine-tuning examples.

Related: [[reasoning model (definition)]] · [[controlling the thinking budget]] · [[chain-of-thought prompting tips]] · [[prompting reasoning models]]

_Source: Stanford CME295 Fall 2025, Lecture 6; Wei et al. 2022._
