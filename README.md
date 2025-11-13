# O'Reilly Live Training: Working with o1, DeepSeek, and Gemini 2.5 Pro Reasoning Capabilities

This repository contains materials for the O'Reilly live training course on reasoning capabilities of modern LLMs.

## Course Information

Link: [Working with o1, DeepSeek, and Gemini 2.5 Reasoning Capabilities](https://www.oreilly.com/live-events/working-with-o1-deepseek-and-gemini-20-reasoning-capabilities/0642572015593/)

## Repository Structure

- `notebooks/`: Jupyter notebooks for hands-on exercises
  - `gpt5-reasoning-demo.ipynb`: **New!** Comprehensive guide to OpenAI's GPT-5 reasoning models with the Responses API
  - `introduction-to-reasoning-models.ipynb`: Introduction to reasoning model concepts
  - `assets-resources/`: Additional resources and reference materials
- `presentation/`: Slides and presentation materials
- `project-notes.md`: Notes and resources for the live course

## Notebooks

### GPT-5 Reasoning Demo (`gpt5-reasoning-demo.ipynb`)

A practical, hands-on guide to OpenAI's GPT-5 reasoning capabilities featuring:

- **Reasoning Effort Levels**: Compare minimal, medium, and high reasoning efforts with real examples
- **Verbosity Control**: Learn how to control output length independently from reasoning depth
- **Practical Use Cases**:
  - Simple classification with minimal reasoning
  - Code generation with medium reasoning
  - Complex algorithm design with high reasoning
  - Bug detection and code review
- **Best Practices**: Based on OpenAI's latest guidelines for optimal performance
- **Token Usage Analysis**: See how different settings affect cost and performance

All examples are designed to run quickly and demonstrate clear, practical applications.

### Prerequisites

```bash
pip install openai
```

Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## About This Course

This course explores the reasoning capabilities of the latest AI models including OpenAI's GPT-5, o-series models, DeepSeek, and Google's Gemini 2.0. Learn how to effectively leverage these models' advanced reasoning abilities for your applications.

## Key Concepts Covered

- What defines a reasoning/thinking model
- When to use reasoning models vs. traditional LLMs
- How to choose the right reasoning effort level
- Best practices for prompting reasoning models
- Cost and performance optimization strategies
- Integration patterns for production workflows