# GRPO advantage refinements

Beyond the length fix ([[DAPO and Dr. GRPO]]), two further tweaks to the GRPO advantage/clipping are commonly applied:

**1. Std-deviation (difficulty) bias.** The full advantage divides by the group's reward std:
```
Âᵢ = ( Rᵢ − mean(R₁…R_G) ) / std(R₁…R_G)
```
On very easy or very hard problems almost all completions get the same reward, so **std is tiny** → dividing by it **over-weights** those questions. Mitigation: drop or adjust the std normalization so difficulty doesn't distort the gradient.

**2. Asymmetric epsilon / "clip-higher"** (DAPO, Yu et al. 2025). Replace the symmetric clip with decoupled bounds:
```
clip(ρ, 1−ε, 1+ε)  →  clip(ρ, 1−ε_low, 1+ε_high)
```
A low-probability token can only grow by a factor `(1+ε)`, which is unfairly small; raising the **upper** bound (`ε_high`) lets rare-but-good tokens grow, **preserving exploration/diversity**, while keeping the lower bound modest so high-probability tokens don't collapse to zero.

Related: [[GRPO]] · [[DAPO and Dr. GRPO]] · [[KL regularization in RL fine-tuning]]

_Source: Stanford CME295 Fall 2025, Lecture 6; Yu et al. 2025 (DAPO)._
