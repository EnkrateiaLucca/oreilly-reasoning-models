These models perform best with straightforward prompts. Some prompt engineering techniques, like instructing the model to "think step by step," may not enhance performance (and can sometimes hinder it). See best practices below, or get started with prompt examples.

Developer messages are the new system messages: Starting with o1-2024-12-17, reasoning models support developer messages rather than system messages, to align with the chain of command behavior described in the model spec.

Keep prompts simple and direct: The models excel at understanding and responding to brief, clear instructions.

Avoid chain-of-thought prompts: Since these models perform reasoning internally, prompting them to "think step by step" or "explain your reasoning" is unnecessary.

Use delimiters for clarity: Use delimiters like markdown, XML tags, and section titles to clearly indicate distinct parts of the input, helping the model interpret different sections appropriately.

Try zero shot first, then few shot if needed: Reasoning models often don't need few-shot examples to produce good results, so try to write prompts without examples first. If you have more complex requirements for your desired output, it may help to include a few examples of inputs and desired outputs in your prompt. Just ensure that the examples align very closely with your prompt instructions, as discrepancies between the two may produce poor results.

Provide specific guidelines: If there are ways you explicitly want to constrain the model's response (like "propose a solution with a budget under $500"), explicitly outline those constraints in the prompt.

Be very specific about your end goal: In your instructions, try to give very specific parameters for a successful response, and encourage the model to keep reasoning and iterating until it matches your success criteria.

Markdown formatting: Starting with o1-2024-12-17, reasoning models in the API will avoid generating responses with markdown formatting. To signal to the model when you do want markdown formatting in the response, include the string Formatting re-enabled on the first line of your developer message.
