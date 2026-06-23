# DeepSeek R1-Zero

A **proof of concept**: you can get strong reasoning with **pure RL and no SFT at all** (DeepSeek-AI, 2025).

**Recipe (2 steps):**
1. Pretrain a base model the traditional way → **V3-Base** (DeepSeek-V3 architecture: **MoE** with shared+routed experts, **Multi-head Latent Attention (MLA)**; ~671B total / ~37B active params).
2. Run **[[GRPO]]** directly on reasoning data — *skipping SFT entirely* — with a verifiable **[[format and accuracy rewards|format + accuracy reward]]**. A simple prompt template instructs the model to put reasoning in `<think></think>` and the result in `<answer></answer>`.

**Result:** reasoning ability emerges with zero supervision; AIME pass@1 climbs ~0.15 → ~0.71 and cons@16 ~0.25 → ~0.86 over ~8k steps — cons@16 surpassing o1's reference lines. Emergent "aha moment" self-correction ("Wait, wait…") appears in the chains.

**Failure modes (why R1 was needed):** because there's no supervision anchor, the chains have **readability problems** and **mix languages**. Fixed in the full pipeline → [[DeepSeek R1 training pipeline]].

Related: [[DeepSeek R1 training pipeline]] · [[why SFT is a poor start for reasoning]] · [[GRPO]] · [[verifiable rewards]]

_Source: Stanford CME295 Fall 2025, Lecture 6; DeepSeek-R1 (2025)._
