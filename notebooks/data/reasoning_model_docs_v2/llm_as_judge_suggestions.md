Here are some suggestions to get the most out of LLM-as-Judge:

- Use pairwise comparisons: Instead of asking the LLM to score a single output on a [Likert](https://en.wikipedia.org/wiki/Likert_scale) scale, present it with two options and ask it to select the better one. This tends to lead to more stable results.
- Control for position bias: The order of options presented can bias the LLM’s decision. To mitigate this, do each pairwise comparison twice, swapping the order of pairs each time. Just be sure to attribute wins to the right option after swapping!
- Allow for ties: In some cases, both options may be equally good. Thus, allow the LLM to declare a tie so it doesn’t have to arbitrarily pick a winner.
- Use Chain-of-Thought: Asking the LLM to explain its decision before giving a final preference can increase eval reliability. As a bonus, this allows you to use a weaker but faster LLM and still achieve similar results. Because frequently this part of the pipeline is in batch mode, the extra latency from CoT isn’t a problem.
- Control for response length: LLMs tend to bias toward longer responses. To mitigate this, ensure response pairs are similar in length.