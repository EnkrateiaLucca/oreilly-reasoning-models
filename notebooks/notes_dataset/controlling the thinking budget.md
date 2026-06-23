# Controlling the thinking budget

Not all prompts deserve the same amount of thinking — over-thinking easy prompts wastes tokens/money ([[reasoning token pricing]]), and the model must also respect its finite context window. Techniques to control inference-time "thinking":

- **Dynamic budget** — adapt the allowed reasoning length to the prompt, e.g. a lightweight classifier that tags a prompt as high- vs low-thinking (Han et al., 2024, *Token-Budget-Aware LLM Reasoning*). Still an open problem.
- **Context awareness** — the model should track how much context length remains and not think past it.
- **Budget forcing** (Muennighoff et al., 2025, *s1: Simple test-time scaling*) — inject tokens mid-chain to steer length: append **"Wait"** to *force more* thinking, or **"…time is up, my answer is"** to *force a stop*.
- **Continuous / latent thoughts** (Hao et al., 2024, *Coconut*) — let the "thinking" happen in **hidden-representation space** rather than discrete language tokens — potentially more meaningful and more compressed than verbal CoT. Active research area.

Related: [[chain-of-thought as test-time compute]] · [[output length growth during RL]] · [[reasoning token pricing]] · [[prompting reasoning models]]

_Source: Stanford CME295 Fall 2025, Lecture 6; Han et al. 2024; Muennighoff et al. 2025; Hao et al. 2024._
