# DAPO and Dr. GRPO

Two fixes for the [[GRPO length-normalization bias]] (the `1/|oᵢ|` per-output factor that makes the model prefer longer bad outputs):

- **DAPO** (Yu et al., 2025) — **equalize token-level contributions** by normalizing once over *total* tokens in the group instead of per output:
  ```
  (1/G) Σᵢ (1/|oᵢ|) Σ_t  →  ( 1 / Σᵢ|oᵢ| ) Σᵢ Σ_t
  ```
  Every token gets the same weight regardless of which output it sits in. DAPO also introduces **clip-higher** (asymmetric ε) → see [[GRPO advantage refinements]].

- **Dr. GRPO** ("GRPO Done Right", Liu et al., 2025, *Understanding R1-Zero-Like Training*) — **drop the length factor entirely**:
  ```
  (1/G) Σᵢ (1/|oᵢ|) Σ_t  →  (1/G) Σᵢ Σ_t
  ```

**Result:** response length stops inflating. Correct-answer length tracks vanilla GRPO, but **incorrect-answer length stays flat/short** instead of ballooning — and the model reaches the same reward with far fewer tokens (better token efficiency).

Related: [[GRPO length-normalization bias]] · [[output length growth during RL]] · [[GRPO advantage refinements]] · [[GRPO]]

_Source: Stanford CME295 Fall 2025, Lecture 6; Yu et al. 2025 (DAPO); Liu et al. 2025 (Dr. GRPO)._
