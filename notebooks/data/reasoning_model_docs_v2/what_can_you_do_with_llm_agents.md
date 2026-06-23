**I**’ve been fascinated with the idea of hooking up LLMs to tools ever since I read papers like [TALM](https://arxiv.org/pdf/2205.12255.pdf) and [Toolsformer](https://arxiv.org/pdf/2302.04761.pdf). Obviously [[LLM agents]] have limitations, there is still much concern regarding the reliability of these systems so, it’s not like we can spin up a bunch of little AGIs to do all of our tasks for us right now. However, we are as realistically close to that as we have ever been!

Recently I’ve been experimenting with Agents because I wanted to know the range and scope of tasks I could implement using them. Meaning, when we think of any expertise, any type of knowledge/or not work, we think of a set of sub-skills, combined with knowledge of a bunch of procedures. For example, if you think about the work of a Machine Learning engineer, you might go straight to the idea of training some cool complex models, and running experiments, but the reality of the day to day is actually composed of many things like:

- Data cleaning and processing 
- Communication with the development team
- Annotating and labeling data

The list goes on and on. So, my goal was to look at all these things and ask, ok 


> what can I realistically automate with Agents?


When I say realistically, I mean, automate in the sense of not having to worry about that task anymore while maintaining control over the final output and its quality, and that also counts for communication automations like setting up a chatbot to interact with people from your company’s to speed up operations.

Ok, so given the question *What can I robustly automate with LLM agents today*, yes I changed the word to robustly and you will understand why.

Let’s pick proven use cases for LLM agents with evidence that their outputs are realistic. There aren’t that many validation metrics and benchmarks right now for LLM agents, but effort on that direction has started to both to [formalize a framework for AI agents](https://arxiv.org/pdf/2306.03314.pdf) as well as create a common set of validation benchmark tasks to evaluate the quality and performance of these models, both in terms of their [ability to interact with humans](https://arxiv.org/pdf/2205.13274.pdf) as well as in [their ability to perform useful tasks](https://arxiv.org/pdf/2308.03688.pdf)

OK, so given these parameters, let’s take a look at useful and proven applications for LLM agents. Let’s start by considering recent papers and repositories that explored this idea of using Agents to perform complex tasks:
- [Scientific research capabilities](https://arxiv.org/pdf/2304.05332.pdf): In [Bran et al. 2023](https://arxiv.org/pdf/2304.05376.pdf) they explored the idea of Agents for scientific discovery, hooking up the models with e xpert designed tools. They showed that their model was able to plan the synthesis of an insect repellent, three organocatalysts, as well as other relevant molecules, arguing that this type of approach is actually quite feasible. Despite the limitation of using LLM based evaluation scores, they concluded for the usefulness of such agents to aid on chemistry research. ![[Pasted image 20230826143634.png | 900]]
- [Predicting protein structure](https://pubmed.ncbi.nlm.nih.gov/36927031/)
- Formatted content generation 
	- [Biomedical text generation](https://arxiv.org/pdf/2210.10341.pdf) 
	- [GPT-Engineer](https://github.com/AntonOsika/gpt-engineer) - this repo explores the ability of powerful LLMs to write entire code bases and apps. They seem to demonstrate some amazing capabilities and based on my personal use of the tool combined with anecdotal evidence from other users, this approach seems like a clear winner when it comes to building simple Python applications.
- Complex planning 
	- [Agents as task managers for image and language based tasks](https://arxiv.org/pdf/2303.17580.pdf) 
			![[Pasted image 20230826143401.png | 400]] ![[Pasted image 20230826143441.png | 400]] 			

# Challenges

[source](https://lilianweng.github.io/posts/2023-06-23-agent/#challenges)
After going through key ideas and demos of building LLM-centered agents, I start to see a couple common limitations:

- **Finite context length**: The restricted context capacity limits the inclusion of historical information, detailed instructions, API call context, and responses. The design of the system has to work with this limited communication bandwidth, while mechanisms like self-reflection to learn from past mistakes would benefit a lot from long or infinite context windows. Although vector stores and retrieval can provide access to a larger knowledge pool, their representation power is not as powerful as full attention.
    
- **Challenges in long-term planning and task decomposition**: Planning over a lengthy history and effectively exploring the solution space remain challenging. LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans who learn from trial and error.
    
- **Reliability of natural language interface**: Current agent system relies on natural language as an interface between LLMs and external components such as memory and tools. However, the reliability of model outputs is questionable, as LLMs may make formatting errors and occasionally exhibit rebellious behavior (e.g. refuse to follow an instruction). Consequently, much of the agent demo code focuses on parsing model output.
- [H. Chase agents masterclass](https://youtu.be/DWUdGhRrv2c?si=hp56A5GUp3alEjuC)
	- Use tools in apropriate scenarios
	- Not use tools when not needed
	- Pars llm output to tool invocation
	- Remembering previous steps
	- Incorporating long observations (similar to the issue of finite context length)
	- Staying focused on task
	- Evaluation

The simplified default framework to think about agents:
![[Pasted image 20230826144906.png | 400]]
[Source](https://blog.langchain.dev/agents-round/)

![[Pasted image 20230826150025.png | 600]]

OK, so we’ve seen some examples, let’s now breakdown what should we expect from AI agents:
- Research agent
	- Producing well-formatted research reports
	- Testing hypothesis on different problems
	- Designing and executing experiments
	- Doing Literature review on a topic of interest
	- Gathering data and data sources for a particular problem or research topic
	- Creating exercises and challenges
	- Creating novel flashcards to challenge what I know and help me practice for better encoding
	- Summarizing papers and web-articles
	- Creating curriculums for learning a tough subject
	- Evaluating performance when learning something new and tracking my progress
	- Document Q&A - Chating with papers, research documents and notes
	- Brainstorming tool for learning, research and content
	- Potential tools to use
		- [Metaphor search tool](https://python.langchain.com/docs/integrations/tools/metaphor_search)
		    - [arxiv tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/arxiv.html)
	    - [Pubmed tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/pubmed.html)
	    - [shell tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/bash.html)
	    - [bing search](https://python.langchain.com/en/latest/modules/agents/tools/examples/bing_search.html)
	    - [google search](https://python.langchain.com/en/latest/modules/agents/tools/examples/google_search.html)
	    - [File management tools](https://python.langchain.com/en/latest/modules/agents/tools/examples/filesystem.html)
	    - [Human as a tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/human_tools.html)
	    - [PythonREPL tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/python.html)
- **Machine Learning Agent** 
    - Write scripts to solve ML problems
    - Debug code
    - Write proper machine learning code for miscelaneous tasks like training, inference, deployment etc…
- **Desktop Agent:**
    - handle everything I have to do on my computer (including interacting with agents?)
    - shell tool to organize stuff
    - Within documents search (use ocr and image search to search for specific things within documents)
    - Natural language search over files in the terminal (e.g ”Find me some contract for work”)
    - Tolls to use:
        - [Shell tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/bash.html)
        - [bing search](https://python.langchain.com/en/latest/modules/agents/tools/examples/bing_search.html)
        - [file management tools](https://python.langchain.com/en/latest/modules/agents/tools/examples/filesystem.html)
        - [Google search](https://python.langchain.com/en/latest/modules/agents/tools/examples/google_search.html)
        - [Gradio tools for ocr and image generation?](https://python.langchain.com/en/latest/modules/agents/tools/examples/gradio_tools.html)

        - [Human as a tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/human_tools.html)
        - 
        - [PythonREPL tool](https://python.langchain.com/en/latest/modules/agents/tools/examples/python.html)














# References
- https://towardsdatascience.com/4-autonomous-ai-agents-you-need-to-know-d612a643fa-  
- https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/#external-apis
- https://lilianweng.github.io/posts/2023-06-23-agent/#challenges
- [LLMs for computer assisted 3D design](https://arxiv.org/pdf/2304.10750.pdf)
- [GPT researcher](https://github.com/assafelovic/gpt-researcher)
- [Agentbench](https://arxiv.org/pdf/2308.03688.pdf) 
- https://github.com/shaman-ai/agent-actors

## Related

- [[Usecases for Agents to Build]] - Concrete examples of agent applications
- [[Potential tools for useful agents]] - Tools mentioned for research and desktop agents
- [[Loop of an LLM Agent]] - Core execution loop referenced in the framework diagram
- [[Evaluation of LLM Agents]] - Methods for evaluating the agents described
- [[the memory issue with agents]] - Addressing the finite context length challenge
- [[building-effective-agents]] - Comprehensive guide for building the types of agents discussed
- [[Chains vs Agents]] - Understanding agent architectures vs simpler chains
- [[insights about agents in 2025]] - Future outlook for agent capabilities
- [[Autonomous Interface Agents]] - Desktop agent concepts


