# MCP Server Guide

> Model Context Protocol (MCP) servers extend your AI assistant with tool access — reading files, searching vaults, managing git repos, and more.

---

## Recommended MCP Servers

### Essential (Start Here)

| Server | Purpose | Install |
|--------|---------|---------|
| **Filesystem** | Read/write files in allowed directories | `npx -y @anthropic/mcp-filesystem` |
| **Obsidian** | Read/write/search your Obsidian vault | `npx -y obsidian-mcp-server` |
| **Git** | Manage git repos (status, diff, commit) | `uvx mcp-server-git` |

### Productivity

| Server | Purpose | Install |
|--------|---------|---------|
| **Memory** | Persistent knowledge graph across sessions | `npx -y @anthropic/mcp-memory` |
| **Sequential Thinking** | Structured problem-solving for complex tasks | `npx -y @anthropic/mcp-sequential-thinking` |
| **Web Search** | Real-time web queries (Brave Search API) | `npx -y @anthropic/mcp-web-search` |

### Development

| Server | Purpose | Install |
|--------|---------|---------|
| **GitHub** | Issues, PRs, code search | `npx -y @anthropic/mcp-github` |
| **Docker** | Container management | `npx -y @anthropic/mcp-docker` |
| **Playwright** | Browser automation and screenshots | `npx -y @anthropic/mcp-playwright` |

### Document Processing

| Server | Purpose | Install |
|--------|---------|---------|
| **MD-to-PDF** | Convert Markdown to professional PDFs | `uvx md-to-pdf-mcp` |
| **PDF Reader** | Read large PDFs with chunking and OCR | `uvx pdf-mcp` |

### Microsoft 365

| Server | Purpose | Install |
|--------|---------|---------|
| **Office 365** | Email, calendar, Teams, Planner, OneDrive | Requires Graph API auth setup |
| **Grasp** | Microsoft Graph integration | VS Code workspace config |

---

## Installation Prerequisites

### For `npx` servers:
```bash
# Install Node.js (includes npx)
# Download from: https://nodejs.org/
node --version   # Verify: should show v18+
```

### For `uvx` servers:
```bash
# Install uv (Python package runner)
pip install uv
uvx --version    # Verify installation
```

---

## Configuration

### Kiro
File: `.kiro/settings/mcp.json` (workspace) or `~/.kiro/settings/mcp.json` (global)

### Claude Desktop
File: `%APPDATA%\Claude\claude_desktop_config.json`

### Format
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx or uvx",
      "args": ["-y", "package-name", ...additional-args],
      "env": {
        "ENV_VAR": "value"
      },
      "disabled": false,
      "autoApprove": ["tool-name-1", "tool-name-2"]
    }
  }
}
```

---

## Obsidian MCP Setup (Detailed)

The Obsidian MCP server is the most important one for this methodology — it lets the AI read and write notes in your vault.

### Step 1: Install the Obsidian Plugin

1. Open Obsidian → Settings → Community Plugins → Turn off Restricted Mode
2. Browse → Search "Local REST API"
3. Install and Enable
4. Go to plugin settings → Note your API key and port (default: 27124)

### Step 2: Add to MCP Config

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "npx",
      "args": ["-y", "obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_REST_URL": "http://127.0.0.1:27124",
        "OBSIDIAN_API_KEY": "your-api-key-from-step-1"
      }
    }
  }
}
```

### Step 3: Verify

In your AI chat, try: "List the files in my Obsidian vault"

If it returns your vault contents, you're connected.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `npx` not found | Install Node.js from nodejs.org |
| `uvx` not found | Run `pip install uv` |
| Obsidian MCP can't connect | Ensure Obsidian is open and Local REST API plugin is enabled |
| Server timeout on start | Some servers take 5-10s to initialize. Retry. |
| Permission denied | Run terminal as administrator, or check file path access |
| GitHub MCP auth error | Set `GITHUB_TOKEN` env var with a personal access token |
