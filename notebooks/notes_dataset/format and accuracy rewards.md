# Format and accuracy rewards

The reasoning RL reward is a sum of two cheap, verifiable components:

**Reward = formatting reward + accuracy reward**

1. **Formatting reward** — did the model place its chain-of-thought inside the required delimiters? Check for the presence of `<think> … </think>` (and `<answer> … </answer>`) tokens. This trains the *structure* of reasoning.
2. **Accuracy reward** — is the final solution correct? Verified deterministically: test cases for code, ground-truth comparison for math. See [[verifiable rewards]].

Neither requires a learned reward model. Over many RL iterations the model learns that producing — and sometimes revising — a visible chain-of-thought raises its probability of a high reward, which drives the observed growth in reasoning length and self-correction.

DeepSeek R1 later adds a third term, a **language-consistency reward** (see [[DeepSeek R1 training pipeline]]), to stop the model from mixing languages mid-chain.

Related: [[verifiable rewards]] · [[GRPO]] · [[DeepSeek R1-Zero]] · [[output length growth during RL]]

_Source: Stanford CME295 Fall 2025, Lecture 6; DeepSeek-R1 (2025)._
