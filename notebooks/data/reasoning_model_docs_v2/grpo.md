# GRPO (Group Relative Policy Optimization)

The go-to RL algorithm for reasoning training (Shao et al., "DeepSeekMath", 2024). Like PPO it does two things: **(1) maximize advantages** and **(2) don't deviate too far** from the old/reference model. The key difference is *how it computes the advantage* → see [[GRPO vs PPO]].

**Core idea.** For a query `q`, sample a **group** of G completions `o₁…o_G` from the old policy. Score each (verifiable reward), then judge each completion *relative to its group* instead of using a learned value/critic network.

**Advantage** (group-relative baseline):
```
Â_i = ( R(q,oᵢ) − mean(R₁…R_G) ) / std(R₁…R_G)
```
(the lecture intro shows just `Reward − mean`; the std normalization is the fuller form — and a source of bias, see [[GRPO advantage refinements]].)

**Objective** (clipped ratio + explicit KL):
```
J_GRPO(θ) = (1/G) Σᵢ (1/|oᵢ|) Σ_t  min[ ρ·Âᵢ , clip(ρ,1−ε,1+ε)·Âᵢ ]  − β·KL(π_θ ‖ π_ref)
   where ρ = π_θ(o_{i,t}|·) / π_θold(o_{i,t}|·)
```
The `1/|oᵢ|` per-output normalization is load-bearing — it causes a length bias → [[GRPO length-normalization bias]].

Related: [[GRPO vs PPO]] · [[KL regularization in RL fine-tuning]] · [[GRPO length-normalization bias]] · [[GRPO advantage refinements]] · [[verifiable rewards]]

_Source: Stanford CME295 Fall 2025, Lecture 6; Shao et al. 2024._
