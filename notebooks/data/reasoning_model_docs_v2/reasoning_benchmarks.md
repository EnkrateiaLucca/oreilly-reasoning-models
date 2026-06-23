# Reasoning benchmarks

Reasoning is quantified on tasks with **verifiable answers**, in two families:

**Coding** — solve a problem or fix a bug. Pipeline: `Problem → Solution → Verification` against test cases (#1…#t), each must pass ✅.
- **HumanEval** — ~164 hand-written coding problems ("human" eval).
- **Codeforces** — competitive-programming problems (often reported as an Elo rating).
- **SWE-bench** — real-world tasks derived from GitHub issues.

**Math** — solve a hard problem (often olympiad-level). Pipeline: `Problem → Reasoning → compare final answer to Ground truth`.
- **AIME** — qualifying exam for the US Math Olympiad; a very common headline benchmark.
- **GSM8K** — grade-school math word problems.

Reported with metrics like [[pass@k metric]], [[consensus@k and self-consistency]], accuracy, and exact match — always alongside the sampling [[temperature vs pass@k|temperature]].

Related: [[verifiable rewards]] · [[pass@k metric]] · [[GSM-Symbolic Understanding the Limitations of Mathematical Reasoning in Large Language Models]]

_Source: Stanford CME295 Fall 2025, Lecture 6._
