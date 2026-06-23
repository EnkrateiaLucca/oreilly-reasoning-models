- https://arc.net/l/quote/wwdhunpb

In chain-of-thought (CoT) prompting, we encourage the LLM to explain its thought process before returning the final answer. Think of it as providing the LLM with a sketchpad so it doesn’t have to do it all in memory. The original approach was to simply add the phrase “Let’s think step-by-step” as part of the instructions. However, we’ve found it helpful to make the CoT more specific, where adding specificity via an extra sentence or two often reduces hallucination rates significantly. For example, when asking an LLM to summarize a meeting transcript, we can be explicit about the steps, such as:

- First, list the key decisions, follow-up items, and associated owners in a sketchpad.
- Then, check that the details in the sketchpad are factually consistent with the transcript.
- Finally, synthesize the key points into a concise summary.