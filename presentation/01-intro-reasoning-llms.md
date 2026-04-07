---
marp: true
theme: default
paginate: true
title: Module 1 — Intro to Reasoning LLMs
---

# Reasoning LLMs
### Module 1 — What are they, why now?

Lucas Soares · O'Reilly Live Training

---

## What is "reasoning"?

> Multi-step problem solving — not retrieval.

---

## Vanilla LLM weak spots

- Knowledge cutoffs
- No actions in the world
- Long-horizon planning collapses

---

## Direct answer vs. thinking chain

![w:900](assets/01_direct_vs_thinking.png)

---

## Timeline

![w:1000](assets/01_timeline.png)

---

## Test-time compute scaling

![w:700](assets/01_test_time_compute.png)

> More thinking → more accuracy.

---

## The simplest trick

```text
Q: A train leaves at 3pm…
A: Let's think step by step.
```

---

## When to reach for a reasoning model

![w:850](assets/01_decision_chart.png)

Math · code · planning · multi-constraint puzzles.

---

## Cost & latency

> 5–50× more tokens. Use only when the task needs it.

---

## Reasoning effort knobs

- **OpenAI:** `reasoning_effort = none / low / medium / high`
- **Anthropic:** `thinking.budget_tokens = N`

---

## Live demo →

`notebooks/01_chain_of_thought_intuition.ipynb`

GPT-2 with and without "Let's think step by step"

---

## Recap

- Reasoning ≠ retrieval
- Trade tokens for accuracy
- Next: how DeepSeek **trained** a reasoning model
