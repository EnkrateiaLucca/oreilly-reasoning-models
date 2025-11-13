# Comprehensive Research Report: Claude Code & Claude Agents SDK

## Executive Summary

This report provides an in-depth analysis of **Claude Code** (Anthropic's official CLI tool) and the **Claude Agents SDK** (framework for building custom AI agents). Both tools enable developers to integrate Claude's capabilities directly into their workflows, with Claude Code focusing on terminal-based development and the Agents SDK providing programmatic agent creation.

**Key Findings:**
- Claude Code transforms the terminal into an AI-powered development environment
- The Agents SDK enables production-ready custom agents with TypeScript and Python support
- Agent Skills provide modular, reusable capabilities across both platforms
- Model Context Protocol (MCP) enables integration with external tools and data sources

---

## Table of Contents

1. [Claude Code: Terminal-Based AI Development](#claude-code-terminal-based-ai-development)
2. [Claude Agents SDK: Building Custom AI Agents](#claude-agents-sdk-building-custom-ai-agents)
3. [Agent Skills: Modular Capabilities](#agent-skills-modular-capabilities)
4. [Model Context Protocol (MCP)](#model-context-protocol-mcp)
5. [Practical Implementation Guide](#practical-implementation-guide)
6. [Use Cases & Applications](#use-cases--applications)
7. [Best Practices & Recommendations](#best-practices--recommendations)

---

## Claude Code: Terminal-Based AI Development

### What is Claude Code?

Claude Code is Anthropic's official command-line interface that embeds Claude directly into developers' terminals and IDEs. It's designed as an agentic coding tool that operates within existing workflows rather than requiring context switching to separate applications.

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

### Core Philosophy

Claude Code follows **Unix philosophy principles**, making it composable and scriptable for complex workflows. Unlike passive chat interfaces, it actively edits files, executes commands, and creates commits—functioning as an autonomous development partner.

**Source:** [Claude Code Product Page](https://www.claude.com/product/claude-code)

### Key Capabilities

#### 1. **Code Development & Problem-Solving**
- Describe features in natural language; Claude plans, writes code, and ensures it works
- Analyzes codebases to identify and fix bugs from error descriptions
- Instant searching across million-line codebases
- Visual diff viewing for code changes

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

#### 2. **Codebase Intelligence**
- Maintains awareness of entire project structures
- Answers questions about codebases by combining:
  - Local project knowledge
  - Web-based information retrieval
  - External data sources via MCP connections (Google Drive, Figma, Slack)

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

#### 3. **Automation Capabilities**
- Resolves lint issues automatically
- Manages merge conflicts
- Generates release notes
- Executes from individual machines or CI/CD pipelines

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

### Integration Points

#### Terminal & IDE Integration
- **Native VS Code extension** available in marketplace
- **JetBrains environments** with enhanced capabilities
- **Web-based access** at claude.ai/code
- Works in any IDE terminal

**Source:** [Claude Code Product Page](https://www.claude.com/product/claude-code)

### Installation

Quick installation via OS-specific commands:

**macOS/Linux:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Other methods:** Homebrew, PowerShell, npm installation

**Source:** [Claude Code Product Page](https://www.claude.com/product/claude-code)

### Enterprise Features

- Operates through Claude API
- Deployment on AWS or GCP
- Built-in security and privacy protections
- Compliance infrastructure
- Used by Fortune 500 companies (Stripe, Figma, Brex)

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

---

## Claude Agents SDK: Building Custom AI Agents

### Overview

The Claude Agents SDK enables developers to build custom AI agents with production-ready features. Built on the same technology powering Claude Code, it provides "all the building blocks you need to build production-ready agents."

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

### Available SDKs

1. **TypeScript SDK** - For Node.js and web applications
2. **Python SDK** - For Python applications and data science

Both SDKs support two operational modes: **streaming** and **single mode**.

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

### Core Features

#### 1. **Automatic Context Management**
The SDK automatically handles context compaction and management to prevent agents from exhausting their context window—a critical feature for long-running agent sessions.

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### 2. **Rich Tool Ecosystem**
Agents have access to:
- File operations (Read, Write, Edit)
- Code execution (Bash)
- Web capabilities (WebFetch, WebSearch)
- File system operations (Glob, Grep)
- MCP resource management
- Extensibility through Model Context Protocol

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### 3. **Fine-Grained Permissions**
Granular control over agent capabilities:
- `allowedTools` - Whitelist specific tools
- `disallowedTools` - Blacklist specific tools
- `permissionMode` - Control execution behavior:
  - `default` - Standard permissions
  - `acceptEdits` - Auto-approve file edits
  - `bypassPermissions` - Full autonomy
  - `plan` - Planning mode only

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### 4. **Production-Ready Features**
- Built-in error handling
- Session management
- Monitoring capabilities
- Usage tracking and cost analytics

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

---

## TypeScript SDK Deep Dive

### Installation

```bash
npm install @anthropic-ai/claude-agent-sdk
```

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

### Core Functions

#### `query()`
Primary interface for interacting with Claude Code. Accepts a prompt and returns an async generator that streams messages.

```typescript
const result = await query({
  prompt: "Analyze this codebase",
  options: {
    model: "claude-sonnet-4-5-20250929",
    permissionMode: "default",
    allowedTools: ["Read", "Grep", "Glob"]
  }
});
```

**Key parameters:**
- `prompt` - User input as string or async iterable for streaming
- `options` - Configuration object

**Returns:** A `Query` object extending `AsyncGenerator` with methods like `interrupt()` and `setPermissionMode()`

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### `tool()`
Creates type-safe MCP tool definitions with Zod schema validation:

```typescript
const myTool = tool(
  "tool_name",
  "Description of what the tool does",
  z.object({ param: z.string() }),
  async (input) => {
    // Tool implementation
    return { result: "success" };
  }
);
```

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### `createSdkMcpServer()`
Instantiates an in-process MCP server with specified tools:

```typescript
const server = createSdkMcpServer({
  name: "my-tools",
  tools: [myTool, anotherTool],
  version: "1.0.0"
});
```

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

### Configuration Options

| Option | Purpose |
|--------|---------|
| `model` | Claude model selection (default from CLI) |
| `systemPrompt` | Custom or preset system instructions |
| `settingSources` | Load filesystem settings ('user', 'project', 'local') |
| `allowedTools` / `disallowedTools` | Control available tools |
| `agents` | Define programmatic subagents |
| `mcpServers` | Configure MCP server connections |
| `permissionMode` | Execution control mode |
| `hooks` | Register event callbacks |

**Important:** `settingSources` defaults to empty for isolation. Explicitly include sources for legacy behavior.

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

### Message Types

The SDK emits several message categories:

- **SDKAssistantMessage** - Claude's responses
- **SDKUserMessage** - User input
- **SDKResultMessage** - Final execution result with usage stats
- **SDKSystemMessage** - Initialization and system events
- **SDKPartialAssistantMessage** - Streaming updates (when enabled)

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

---

## Python SDK Deep Dive

### Installation

```bash
pip install claude-agent-sdk
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### Core Functions

#### `query()`
Creates a new session for each interaction. Returns an async iterator yielding messages as they arrive.

```python
async def query(
    *,
    prompt: str | AsyncIterable[dict[str, Any]],
    options: ClaudeAgentOptions | None = None
) -> AsyncIterator[Message]
```

**Best for:** One-off tasks without needing conversation history.

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

#### `ClaudeSDKClient`
Maintains conversation context across multiple exchanges within a single session.

```python
async with ClaudeSDKClient(options) as client:
    await client.query("Your prompt here")
    async for message in client.receive_response():
        print(message)
```

**Key differences from `query()`:**
- Reuses the same session
- Supports interrupts and hooks
- Enables custom tools
- Remembers previous context

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### Configuration

`ClaudeAgentOptions` configures Claude's behavior:

| Option | Purpose |
|--------|---------|
| `allowed_tools` | List of available tools |
| `system_prompt` | Custom or preset instructions |
| `permission_mode` | Controls tool execution |
| `mcp_servers` | Model Context Protocol server configs |
| `cwd` | Working directory |
| `env` | Environment variables |

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### Custom Tools

Define tools using the `@tool` decorator:

```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("greet", "Greet a user", {"name": str})
async def greet(args: dict[str, Any]) -> dict[str, Any]:
    return {
        "content": [{
            "type": "text",
            "text": f"Hello, {args['name']}!"
        }]
    }

# Create MCP server with tools
calculator = create_sdk_mcp_server(
    name="calculator",
    tools=[add, multiply, greet]
)
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### Message Types

- **UserMessage** - User input
- **AssistantMessage** - Claude response with content blocks
- **SystemMessage** - System metadata
- **ResultMessage** - Final result with cost/usage data

**Content blocks include:** `TextBlock`, `ThinkingBlock`, `ToolUseBlock`, `ToolResultBlock`

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### Error Handling

- `CLINotFoundError` - Claude Code not installed
- `ProcessError` - Process execution failed
- `CLIJSONDecodeError` - Response parsing failed

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### Advanced Features

#### Hooks
Intercept events for logging or modification:

```python
async def log_tools(input_data, tool_use_id, context):
    print(f"Tool: {input_data.get('tool_name')}")
    return {}

options = ClaudeAgentOptions(
    hooks={
        'PreToolUse': [HookMatcher(hooks=[log_tools])]
    }
)
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

#### Streaming Input
Supports async iterables for dynamic prompts, enabling real-time data feeds to Claude.

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

---

## Agent Skills: Modular Capabilities

### What Are Agent Skills?

Agent Skills are **reusable, filesystem-based resources** that provide Claude with domain-specific expertise: workflows, context, and best practices. They package three components:

1. **Instructions** for Claude to follow
2. **Metadata** for discovery
3. **Optional resources** (scripts, templates)

**Source:** [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

### Key Benefits

#### 1. **Specialization**
Tailor Claude's capabilities for specific domains (legal review, financial analysis, code reviews, etc.)

#### 2. **Reusability**
Create once, deploy across multiple conversations—unlike traditional prompts that only work in single conversations.

#### 3. **Composition**
Combine multiple Skills (up to 8) to build complex workflows.

**Source:** [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

### How Skills Work: Progressive Disclosure

Skills use a three-stage loading model to optimize context usage:

- **Level 1: Metadata** (always loaded) - Brief YAML descriptions
- **Level 2: Instructions** (when triggered) - Main guidance files
- **Level 3: Resources** (as needed) - Scripts, references, templates

This ensures only relevant content consumes context tokens.

**Source:** [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

### Availability Across Platforms

| Platform | Pre-built Skills | Custom Skills |
|----------|------------------|---------------|
| Claude.ai | ✓ | ✓ (individual user) |
| Claude API | ✓ | ✓ (workspace-wide) |
| Claude Code | ✓ | ✓ (filesystem-based) |
| Agent SDK | ✓ | ✓ |

**Source:** [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

### Pre-built Anthropic Skills

Four managed Skills available:

1. **PowerPoint (pptx)** - Create and edit presentations
2. **Excel (xlsx)** - Create and analyze spreadsheets
3. **Word (docx)** - Create and edit documents
4. **PDF (pdf)** - Generate PDF documents

**Source:** [Agent Skills Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)

### Creating Custom Skills

#### Basic Structure

Every Skill requires a `SKILL.md` file with YAML frontmatter:

```markdown
---
name: processing-pdfs
description: Extract and analyze content from PDF documents
---

# Instructions for Claude

[Your detailed instructions here]

## When to Use This Skill

Use this skill when the user needs to...

## Examples

...
```

**Source:** [Agent Skills Overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)

#### Using Skills in API

Specify Skills via the `container` parameter (up to 8 Skills per request):

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{
            "type": "anthropic",
            "skill_id": "xlsx",
            "version": "latest"
        }]
    },
    messages=[{"role": "user", "content": "Create a sales report"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)
```

**Source:** [Skills Guide with API](https://docs.claude.com/en/docs/build-with-claude/skills-guide)

### Managing Custom Skills

#### Creating Skills
- Upload via directory path or zip file using Skills API
- Must include `SKILL.md` at top level
- Maximum 8MB total upload size
- YAML frontmatter requires: `name` (max 64 chars) and `description` (max 1024 chars)

#### Operations
- **List all Skills** (filter by `source: "custom"`)
- **Retrieve specific Skill details**
- **Create new versions** for updates
- **Delete Skills** (requires deleting all versions first)

**Source:** [Skills Guide with API](https://docs.claude.com/en/docs/build-with-claude/skills-guide)

### Skills Best Practices

#### 1. **Conciseness is Critical**
Keep `SKILL.md` body under 500 lines. "Default assumption: Claude is already very smart"—only add context Claude doesn't possess. Each token competes with conversation history.

#### 2. **Appropriate Freedom Levels**
- **High-freedom** instructions for flexible tasks (code reviews)
- **Low-freedom** scripts for error-prone operations (database migrations)

#### 3. **Cross-Model Testing**
Verify Skills work across Claude Haiku, Sonnet, and Opus—effectiveness varies by model capability.

#### 4. **Naming Conventions**
- Use gerund form (verb + -ing)
- Lowercase letters and hyphens only
- Examples: `processing-pdfs`, `analyzing-spreadsheets`

#### 5. **Descriptions**
Write in third person and be specific. Include both what the Skill does and when to use it—essential for discovery among 100+ Skills.

#### 6. **Progressive Disclosure Structure**
Structure content so Claude loads `SKILL.md` first, then reads additional files only when needed. Keep references one level deep from `SKILL.md`.

#### 7. **Error Handling**
Scripts should solve problems, not punt to Claude. Document constants and handle edge cases explicitly.

**Source:** [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

### Anti-Patterns to Avoid

- Windows-style paths (use forward slashes: `reference/guide.md`)
- Offering too many options without defaults
- Time-sensitive information
- Inconsistent terminology
- Deeply nested file references

**Source:** [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

### Skill Constraints

- No network access in execution environment
- No runtime package installation
- Maximum 8 Skills per request
- 8MB upload size limit

**Source:** [Skills Guide with API](https://docs.claude.com/en/docs/build-with-claude/skills-guide)

---

## Model Context Protocol (MCP)

### Overview

The Model Context Protocol (MCP) is a framework for integrating external tools and data sources with Claude. It enables agents to access platforms like Google Drive, Figma, Slack, and custom data sources.

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

### MCP Integration in Agent SDK

The Agent SDK provides built-in MCP support through:

- **MCP server configuration** via `mcpServers` option
- **MCP resource management** tools
- **Remote MCP servers** for external integrations
- **MCP connector** for API integration

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

### Key Features

MCP enables:
- **External data access** (databases, cloud storage, APIs)
- **Tool extensibility** (custom tools beyond built-ins)
- **Third-party integrations** (Slack, Google Drive, Figma)
- **Context enrichment** (bring external knowledge into conversations)

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

---

## Practical Implementation Guide

### 1. Getting Started with Claude Code

#### Step 1: Installation
```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows
irm https://claude.ai/install.ps1 | iex
```

#### Step 2: First Commands
```bash
# Start interactive session
claude

# Ask about your codebase
claude "Explain the authentication flow"

# Fix bugs
claude "Fix the error in api/users.ts"

# Refactor code
claude "Refactor this function to be more readable"
```

**Source:** [Claude Code Product Page](https://www.claude.com/product/claude-code)

### 2. Building Your First Agent (TypeScript)

#### Step 1: Install SDK
```bash
npm install @anthropic-ai/claude-agent-sdk
```

#### Step 2: Create Basic Agent
```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

async function runAgent() {
  const result = await query({
    prompt: "Analyze the codebase and find potential bugs",
    options: {
      model: "claude-sonnet-4-5-20250929",
      permissionMode: "default",
      allowedTools: ["Read", "Grep", "Glob"]
    }
  });

  for await (const message of result) {
    if (message.type === 'assistant') {
      console.log(message.content);
    }
  }
}

runAgent();
```

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

### 3. Building Your First Agent (Python)

#### Step 1: Install SDK
```bash
pip install claude-agent-sdk
```

#### Step 2: Create Basic Agent
```python
from claude_agent_sdk import query, ClaudeAgentOptions

async def run_agent():
    options = ClaudeAgentOptions(
        model="claude-sonnet-4-5-20250929",
        allowed_tools=["Read", "Grep", "Glob"],
        permission_mode="default"
    )

    async for message in query(
        prompt="Analyze the codebase and find potential bugs",
        options=options
    ):
        if message.type == "assistant":
            print(message.content)

# Run the agent
import asyncio
asyncio.run(run_agent())
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### 4. Creating Your First Skill

#### Step 1: Create SKILL.md
```markdown
---
name: code-reviewer
description: Performs comprehensive code reviews with security and performance analysis
---

# Code Review Skill

This skill helps Claude perform thorough code reviews.

## Process

1. Read the code files
2. Check for:
   - Security vulnerabilities (SQL injection, XSS, etc.)
   - Performance issues
   - Code style consistency
   - Error handling
3. Provide actionable feedback

## Examples

[Include examples of good vs. bad code patterns]
```

#### Step 2: Use in API
```python
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [{
            "type": "custom",
            "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",
            "version": "latest"
        }]
    },
    messages=[{"role": "user", "content": "Review this pull request"}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)
```

**Source:** [Agent Skills Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)

### 5. Creating Custom Tools

#### TypeScript Example
```typescript
import { tool, createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

const databaseQuery = tool(
  "database_query",
  "Query the production database",
  z.object({
    query: z.string(),
    database: z.enum(['users', 'orders', 'products'])
  }),
  async (input) => {
    // Execute database query safely
    const result = await executeQuery(input.query, input.database);
    return { result };
  }
);

const dbServer = createSdkMcpServer({
  name: "database-tools",
  tools: [databaseQuery],
  version: "1.0.0"
});
```

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### Python Example
```python
from claude_agent_sdk import tool, create_sdk_mcp_server

@tool("database_query", "Query the production database", {
    "query": str,
    "database": str
})
async def database_query(args: dict) -> dict:
    # Execute database query safely
    result = await execute_query(args['query'], args['database'])
    return {"content": [{"type": "text", "text": str(result)}]}

db_server = create_sdk_mcp_server(
    name="database-tools",
    tools=[database_query]
)
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

---

## Use Cases & Applications

### 1. Coding & Development

#### SRE Diagnostics Agent
```python
options = ClaudeAgentOptions(
    system_prompt="You are an SRE specialist. Diagnose system issues and provide remediation steps.",
    allowed_tools=["Bash", "Read", "Grep"],
    permission_mode="default"
)

async for message in query(
    prompt="High CPU usage on production server. Investigate.",
    options=options
):
    process_message(message)
```

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### Security Audit Agent
- Scan codebases for vulnerabilities
- Check for OWASP Top 10 issues
- Review dependencies for known CVEs
- Generate security reports

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### Incident Triage Agent
- Analyze error logs
- Identify root causes
- Suggest remediation steps
- Create incident reports

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### Code Review Agent
- Review pull requests
- Check style consistency
- Identify potential bugs
- Suggest improvements

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

### 2. Business Applications

#### Legal Review Agent
- Analyze contracts
- Identify risky clauses
- Ensure compliance
- Generate summaries

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### Financial Analysis Agent
- Process financial data
- Generate reports
- Identify trends
- Create visualizations using Excel Skill

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### Customer Support Agent
- Answer common questions
- Access knowledge bases via MCP
- Escalate complex issues
- Track conversation history

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### Content Creation Agent
- Generate presentations using PowerPoint Skill
- Create documents using Word Skill
- Generate PDFs
- Maintain brand consistency

**Source:** [Agent Skills Quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)

### 3. Automation & CI/CD

#### Release Note Generator
```bash
# In CI/CD pipeline
claude "Generate release notes from commits since last release"
```

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

#### Automated Bug Fixing
```bash
# Resolve lint issues
claude "Fix all ESLint errors in src/"

# Handle merge conflicts
claude "Resolve merge conflicts in feature branch"
```

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

---

## Best Practices & Recommendations

### For Claude Code Users

#### 1. **Start Small**
Begin with simple queries before complex refactoring:
```bash
# Good starting point
claude "What does the authenticate function do?"

# Then progress to
claude "Refactor authentication to use JWT tokens"
```

#### 2. **Use Specific Prompts**
```bash
# Vague
claude "Fix the bug"

# Specific
claude "Fix the null pointer exception in api/users.ts line 42"
```

#### 3. **Leverage Codebase Context**
Claude Code understands your entire project—ask questions that span multiple files:
```bash
claude "How does the authentication flow work from login to API access?"
```

#### 4. **Review Changes**
Always review Claude's changes using visual diffs before committing.

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

### For Agent SDK Developers

#### 1. **Choose the Right Permission Mode**

| Mode | Use Case |
|------|----------|
| `default` | Development and testing |
| `acceptEdits` | Trusted file operations |
| `bypassPermissions` | Fully autonomous agents |
| `plan` | Planning without execution |

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### 2. **Limit Tool Access**
Only grant necessary tools:
```typescript
{
  allowedTools: ["Read", "Grep"],  // Limited for security
  disallowedTools: ["Bash", "Write"]  // Prevent destructive actions
}
```

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### 3. **Implement Error Handling**
```python
from claude_agent_sdk import CLINotFoundError, ProcessError

try:
    async for message in query(prompt="...", options=options):
        process_message(message)
except CLINotFoundError:
    print("Claude Code not installed")
except ProcessError as e:
    print(f"Execution failed: {e}")
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

#### 4. **Use Hooks for Observability**
```python
async def log_tool_use(input_data, tool_use_id, context):
    logger.info(f"Tool {input_data.get('tool_name')} called")
    return {}

options = ClaudeAgentOptions(
    hooks={'PreToolUse': [HookMatcher(hooks=[log_tool_use])]}
)
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

#### 5. **Monitor Costs**
Track usage via `ResultMessage`:
```python
async for message in query(prompt="...", options=options):
    if message.type == "result":
        print(f"Input tokens: {message.usage.input_tokens}")
        print(f"Output tokens: {message.usage.output_tokens}")
```

**Source:** [Python SDK Reference](https://docs.claude.com/en/docs/agent-sdk/python)

### For Skill Developers

#### 1. **Follow the 500-Line Rule**
Keep `SKILL.md` under 500 lines. Use progressive disclosure to link to additional resources.

**Source:** [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

#### 2. **Test Across Models**
Verify Skills work with Haiku (speed), Sonnet (balance), and Opus (complex tasks).

**Source:** [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

#### 3. **Provide Defaults**
Don't offer too many options without recommended defaults.

**Source:** [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

#### 4. **Include Error Handling in Scripts**
Pre-built scripts should handle edge cases rather than delegating to Claude.

**Source:** [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

#### 5. **Build Evaluations First**
Create evaluation datasets before extensive documentation to ensure you're solving real problems.

**Source:** [Agent Skills Best Practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

### For Enterprise Deployments

#### 1. **Use Appropriate Authentication**
- Claude API with API keys
- Amazon Bedrock authentication
- Google Vertex AI authentication

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

#### 2. **Implement Permission Controls**
Use granular permissions to control agent capabilities in production.

**Source:** [TypeScript SDK Reference](https://docs.claude.com/en/docs/agent-sdk/typescript)

#### 3. **Monitor Usage and Costs**
Track token usage and set budgets for agent operations.

**Source:** [Claude Code Overview](https://code.claude.com/docs/en/overview)

#### 4. **Maintain Skill Libraries**
Create workspace-wide Skill repositories for consistency across teams.

**Source:** [Skills Guide with API](https://docs.claude.com/en/docs/build-with-claude/skills-guide)

---

## Key Takeaways

### Claude Code
✓ Terminal-native AI development tool
✓ Integrates with VS Code, JetBrains, and web
✓ Handles million-line codebases
✓ Automates repetitive tasks
✓ Enterprise-ready with security built-in

### Claude Agents SDK
✓ TypeScript and Python support
✓ Production-ready features (error handling, monitoring)
✓ Fine-grained permission controls
✓ Automatic context management
✓ Rich tool ecosystem + MCP extensibility

### Agent Skills
✓ Modular, reusable capabilities
✓ Progressive disclosure for efficiency
✓ Pre-built Skills (Office suite + PDF)
✓ Custom Skills up to 8MB
✓ Combine up to 8 Skills per request

### Model Context Protocol (MCP)
✓ Extends agents with external tools
✓ Integrates with cloud platforms (Drive, Slack, Figma)
✓ Enables custom data source connections
✓ Enriches agent context

---

## Additional Resources

### Official Documentation
- **Claude Code Docs:** [code.claude.com/docs](https://code.claude.com/docs)
- **Agent SDK Overview:** [docs.claude.com/en/docs/agent-sdk/overview](https://docs.claude.com/en/docs/agent-sdk/overview)
- **TypeScript SDK:** [docs.claude.com/en/docs/agent-sdk/typescript](https://docs.claude.com/en/docs/agent-sdk/typescript)
- **Python SDK:** [docs.claude.com/en/docs/agent-sdk/python](https://docs.claude.com/en/docs/agent-sdk/python)
- **Agent Skills:** [docs.claude.com/en/docs/agents-and-tools/agent-skills/overview](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview)
- **Skills Best Practices:** [docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)

### Getting Started
- **Claude Code Product Page:** [claude.com/product/claude-code](https://www.claude.com/product/claude-code)
- **Agent Skills Quickstart:** [docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/quickstart)
- **Skills API Guide:** [docs.claude.com/en/docs/build-with-claude/skills-guide](https://docs.claude.com/en/docs/build-with-claude/skills-guide)

---

## Branding Note

Products using the Agent SDK should use naming like **"Claude Agent"** (preferred) rather than "Claude Code" to maintain distinct branding.

**Source:** [Claude Agents SDK Overview](https://docs.claude.com/en/docs/agent-sdk/overview)

---

*Report compiled from official Anthropic documentation. All information sourced and cited from publicly available Claude documentation as of the research date.*
