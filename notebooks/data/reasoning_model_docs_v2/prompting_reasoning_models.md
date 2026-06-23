A simple prompt hack that makes reasoning models 3x more effective has been hiding in plain sight - and it's not "think step by step."

While many developers instinctively add chain-of-thought prompts to their LLM calls, new research shows this actually degrades performance with modern reasoning models like OpenAI's o1 and DeepSeek's recent R1.

Key insights on effective prompting:
(1) Developer-first architecture - modern reasoning models like o3 use a new paradigm where instructions are passed as what's called "developer messages" rather than system prompts, enabling more precise control over model behavior
(2) Zero-shot superiority - these models often perform better without examples, contrary to traditional LLMs
(3) Constraint clarity - explicitly outline limitations (e.g., "solution under $500") instead of asking for step-by-step thinking
(4) Structured input control - use delimiters (XML tags, markdown, section headers) to organize your prompts, significantly improving the model's understanding of distinct input components
(5) Markdown handling - newer versions of reasoning models require explicit activation of markdown formatting through a simple header flag, so don't expect markdown to be generated otherwise

My take: Clearly, reasoning models operate differently from traditional LLMs such as Claude Sonnet and GPT-4o. Comparing these models is like judging a coding model, such as Mistral’s Codestral, by its ability to write poetry—it’s an apples-to-oranges comparison.

This isn't just about better prompts - it's about fundamentally rethinking how we interact with AI systems designed for complex reasoning.