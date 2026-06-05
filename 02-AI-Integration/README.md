# Layer 2: AI Integration

> Connect your tracking system to an AI coding assistant for automated updates, file generation, and workflow orchestration.

---

## Overview

The AI layer is **optional** — your Obsidian tracking works perfectly without it. But when connected, your AI assistant can:

- Automatically update `Projects.md` when you finish working on something
- Generate reports, documents, and templates on demand
- Read your vault to understand project context before answering questions
- Run the kanban sync script when source files change
- Create new project entries from natural language descriptions

---

## Platform Options

| Platform | Best For | MCP Support | Cost |
|----------|----------|-------------|------|
| **Kiro** | Full IDE integration, hooks, steering | Native | Free (preview) |
| **Claude Desktop** | Chat + file access | Via config | Pro subscription |
| **Cursor** | AI-enhanced coding | Built-in | Pro subscription |
| **VS Code + Copilot** | Code completion + chat | Extensions | Pro subscription |

Choose whichever platform you already use. The methodology works with any of them.

---

## Kiro Setup (Recommended)

### 1. Install Kiro

Download from [kiro.dev](https://kiro.dev) and install.

### 2. Open Your Workspace

Open the folder containing your projects (this repo, your vault, etc.) as a Kiro workspace.

### 3. Configure Steering Files

Copy the templates from `Kiro/steering-templates/` into your workspace's `.kiro/steering/` folder:

```
.kiro/
└── steering/
    ├── master-workflow.md      ← Core behavior rules
    ├── project-structure.md   ← How to structure projects
    └── project-tracking.md    ← How to update Obsidian tracking
```

These files tell the AI *how* to work with your system — what files to update, what format to use, and when to take action.

### 4. Install MCP Servers

MCP (Model Context Protocol) servers give the AI access to external tools. Configure in `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_REST_URL": "http://127.0.0.1:27124",
        "OBSIDIAN_API_KEY": "your-api-key-here"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem"],
      "env": {}
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "."]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-memory"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"]
    }
  }
}
```

**Required for Obsidian MCP:** Install the "Local REST API" community plugin in Obsidian (Settings → Community Plugins → Browse → "Local REST API"). This gives the AI read/write access to your vault.

### 5. Set Up Hooks (Optional)

Hooks trigger automatic actions on IDE events. Create `.kiro/hooks/` files:

**Auto-sync kanban board when tracking files change:**
```json
{
  "name": "Sync Kanban Board",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/Tracking/Projects.md", "**/Tracking/Tasks.md"]
  },
  "then": {
    "type": "runCommand",
    "command": "python sync_project_board.py"
  }
}
```

**Remind AI to update tracking after work:**
```json
{
  "name": "Update Project Tracking",
  "version": "1.0.0",
  "when": {
    "type": "agentStop"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review what was accomplished. If project work was done, update Tracking/Projects.md with completed tasks."
  }
}
```

---

## Claude Desktop Setup

### 1. Install Claude Desktop

Download from [claude.ai/download](https://claude.ai/download).

### 2. Configure MCP

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem", "C:\\Users\\[you]\\Documents\\PM-Vault"]
    },
    "obsidian": {
      "command": "npx",
      "args": ["-y", "obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_REST_URL": "http://127.0.0.1:27124",
        "OBSIDIAN_API_KEY": "your-key"
      }
    }
  }
}
```

### 3. Usage

In Claude Desktop, you can now say:
- "Read my Projects.md and tell me what's overdue"
- "Add a new project called 'Q4 Budget Review' to my In Progress section"
- "Generate a weekly status report from my current projects"

---

## Cursor / VS Code + Copilot

These platforms integrate AI directly into your editor. While they don't have the same hook/steering system as Kiro, you can:

1. Open your vault folder as a workspace
2. Use AI chat to ask questions about your Markdown files
3. Generate content using your templates as context
4. Run scripts via the integrated terminal

See `Alternative-Platforms/` for platform-specific guides.

---

## What the AI Can Do For You

| Task | How to Trigger | What Happens |
|------|---------------|--------------|
| Update project tracking | Automatic (hook) or ask | Marks tasks [x] in Projects.md |
| Generate status report | "Write a status report for [project]" | Reads Projects.md, generates formatted report |
| Create project from template | "Start a new project called X" | Creates folder structure + charter |
| Sync kanban board | Automatic (hook) or `python sync_project_board.py` | Regenerates Project Board.md |
| Search across vault | "Find all notes about [topic]" | Uses Obsidian MCP to search |
| Convert document format | "Convert this MD to Word" | Uses DocForge or built-in tools |

---

## Security Notes

- MCP servers run locally — no data leaves your machine unless you explicitly use cloud APIs
- The Obsidian REST API only listens on localhost (127.0.0.1)
- API keys for local services are stored in your MCP config, not in the vault itself
- Git credentials use your system's credential manager
