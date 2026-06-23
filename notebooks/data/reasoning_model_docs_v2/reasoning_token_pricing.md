# Reasoning token pricing

A reasoning model's output is **reasoning chain + answer**, and **you are billed for both** — the reasoning ("thinking") tokens count as output tokens on every major API (OpenAI, Anthropic, Google).

Consequences:
- **Incentive to minimize reasoning tokens** while keeping accuracy — get the most reasoning ability per token paid. Motivates [[controlling the thinking budget]] and the length fixes in [[DAPO and Dr. GRPO]].
- **You usually can't see the raw chain.** UIs show a *summarized* "thought" (labeled "Thinking…"), with the full chain hidden. Likely reasons: the raw chain may be barely intelligible, users don't want pages of it, and — competitively — exposed chains could be used to train rival models.

**How to spot a reasoning model:** the UI shows a "thinking" phase / thought summary, and often a toggle (standard vs extended thinking).

Related: [[reasoning model (definition)]] · [[controlling the thinking budget]] · [[output length growth during RL]]

_Source: Stanford CME295 Fall 2025, Lecture 6._
