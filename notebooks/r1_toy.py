"""
r1_toy.py — shared toy machinery for the R1-from-scratch notebooks.

One tiny task runs through the whole course: **1-digit integer addition**.
A small character-level transformer (`TinyLM`) learns to emit a short
reasoning scratchpad and then an answer. Every notebook measures the SAME
single metric: **task pass-rate** (fraction of random a+b prompts answered
correctly), so you can watch one number climb across the recipe.

------------------------------------------------------------------------
A NOTE ON THE SCRATCHPAD MARKERS
------------------------------------------------------------------------
In notebook 01 we use human-readable tags: `<think>...</think><answer>...</answer>`.
A tiny char-level model learns those tags fine for plain supervised training.

For the RL stages (notebooks 02-03) we switch to **compact single-character
markers**:

    T  stands in for  <think>
    A  stands in for  <answer>
    .  ends the sequence

    e.g.   3+4=T3+4 A7.

Why the swap?  GRPO needs *variety within a group of sampled completions* to
get a learning signal (its advantage is a z-score across the group). With long
multi-character tags the model becomes confidently right or confidently wrong
on a whole prompt, so every sample in a group gets the same reward, the
advantage collapses to zero, and nothing learns. The compact one-char answer
keeps enough sampling entropy on the answer token for GRPO to find the signal.

So `T`/`A` are just terse aliases for `<think>`/`<answer>` — same idea, smaller
alphabet, RL-friendly. This is a deliberate, documented simplification.
"""

import re
import random
import torch
import torch.nn as nn
import torch.nn.functional as F

# --------------------------------------------------------------------------
# Tokenizer / vocab for the addition task (compact-marker format)
# --------------------------------------------------------------------------
VOCAB = list('0123456789+=TA .')
STOI = {c: i for i, c in enumerate(VOCAB)}
ITOS = {i: c for c, i in STOI.items()}
V = len(VOCAB)
PAD = STOI[' ']
EOS = STOI['.']
BLOCK = 24


def encode(s):
    return [STOI[c] for c in s]


def decode(ids):
    return ''.join(ITOS[i] for i in ids)


# --------------------------------------------------------------------------
# Data: 1-digit addition with a "think then answer" scratchpad
#   format:  {a}+{b}=T{a}+{b} A{a+b}.
#   T (=<think>) opens the scratchpad, A (=<answer>) opens the answer, . ends.
# --------------------------------------------------------------------------
def make_example(a, b):
    """One fully-formatted training string for a+b."""
    return f'{a}+{b}=T{a}+{b} A{a + b}.'


def all_examples():
    """All 100 single-digit addition examples."""
    return [make_example(a, b) for a in range(10) for b in range(10)]


def random_prompt():
    """A random bare prompt like '7+8=' plus its (a, b)."""
    a, b = random.randint(0, 9), random.randint(0, 9)
    return f'{a}+{b}=', a, b


def pad_batch(strings):
    """Encode + right-pad a list of strings into a (B, T) LongTensor."""
    ids = [encode(s) for s in strings]
    L = max(len(x) for x in ids)
    return torch.tensor([x + [PAD] * (L - len(x)) for x in ids])


# --------------------------------------------------------------------------
# Model: a tiny char-level transformer LM
# --------------------------------------------------------------------------
class TinyLM(nn.Module):
    """Minimal decoder-only char transformer. d=64,h=4,L=2 -> ~104K params."""

    def __init__(self, V=V, d=64, h=4, L=2, block=BLOCK):
        super().__init__()
        self.tok = nn.Embedding(V, d)
        self.pos = nn.Embedding(block, d)
        self.blocks = nn.ModuleList([
            nn.TransformerEncoderLayer(
                d, h, dim_feedforward=4 * d, batch_first=True, activation='gelu'
            ) for _ in range(L)
        ])
        self.head = nn.Linear(d, V)
        self.block = block

    def forward(self, x):
        T = x.shape[1]
        h = self.tok(x) + self.pos(torch.arange(T, device=x.device))
        mask = nn.Transformer.generate_square_subsequent_mask(T).to(x.device)
        for blk in self.blocks:
            h = blk(h, src_mask=mask)
        return self.head(h)


def n_params(model):
    """Parameter count in thousands."""
    return sum(p.numel() for p in model.parameters()) / 1e3


# --------------------------------------------------------------------------
# Generation
# --------------------------------------------------------------------------
@torch.no_grad()
def generate(model, prompt, max_new=16):
    """Greedy decode from a prompt; stops at EOS ('.')."""
    x = torch.tensor([encode(prompt)])
    for _ in range(max_new):
        logits = model(x[:, -BLOCK:])[:, -1, :]
        nxt = torch.argmax(logits, -1, keepdim=True)
        x = torch.cat([x, nxt], 1)
        if nxt.item() == EOS:
            break
    return decode(x[0].tolist())


def extract_answer(text):
    """Pull the integer inside the 'A...' answer marker, or None."""
    m = re.search(r'A(\d+)\.', text)
    return int(m.group(1)) if m else None


# --------------------------------------------------------------------------
# The ONE metric every notebook reports: task pass-rate
# --------------------------------------------------------------------------
def pass_rate(model, n=200):
    """Fraction of n random a+b prompts the model answers correctly (greedy)."""
    correct = 0
    for _ in range(n):
        a, b = random.randint(0, 9), random.randint(0, 9)
        out = generate(model, f'{a}+{b}=')
        if extract_answer(out) == a + b:
            correct += 1
    return correct / n


# --------------------------------------------------------------------------
# Reward (rule-based, R1 style): format credit + correctness credit
# --------------------------------------------------------------------------
def reward(prompt, completion):
    """0.1 for using the think/answer format, +1.0 if the answer is correct."""
    text = prompt + completion
    m = re.match(r'(\d)\+(\d)=', prompt)
    if not m:
        return 0.0
    target = int(m.group(1)) + int(m.group(2))
    r = 0.0
    if 'T' in completion and 'A' in completion:   # format reward
        r += 0.1
    ans = re.search(r'A(\d+)\.', text)
    if ans and int(ans.group(1)) == target:       # accuracy reward
        r += 1.0
    return r


# --------------------------------------------------------------------------
# Stochastic sampling with log-probs, used by GRPO and rejection sampling
# --------------------------------------------------------------------------
def sample_completion(model, prompt_ids, max_new=16, temperature=1.0):
    """
    Sample one completion from `prompt_ids` (a (1, P) LongTensor).
    Returns (full_sequence, summed_log_prob_of_generated_tokens).
    The summed log-prob is what GRPO multiplies by the advantage.
    """
    x = prompt_ids.clone()
    logps = []
    for _ in range(max_new):
        logits = model(x[:, -BLOCK:])[:, -1, :] / temperature
        probs = F.softmax(logits, -1)
        nxt = torch.multinomial(probs, 1)
        logps.append(F.log_softmax(logits, -1).gather(1, nxt))
        x = torch.cat([x, nxt], 1)
        if nxt.item() == EOS:
            break
    return x, torch.cat(logps, 1).sum(1)


@torch.no_grad()
def sample_text(model, prompt, max_new=16, temperature=1.0):
    """Sample a completion and return the full decoded string (no grad)."""
    x = torch.tensor([encode(prompt)])
    for _ in range(max_new):
        logits = model(x[:, -BLOCK:])[:, -1, :] / temperature
        nxt = torch.multinomial(F.softmax(logits, -1), 1)
        x = torch.cat([x, nxt], 1)
        if nxt.item() == EOS:
            break
    return decode(x[0].tolist())
