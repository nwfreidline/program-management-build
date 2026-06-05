"""Bridge to GRASP MCP for email template lookup and calendar integration.

Communicates with grasp-mcp via its MCP stdio protocol (JSON-RPC).
Starts a short-lived grasp-mcp process, sends tool calls, and reads results.
"""
import json
import logging
import subprocess
import datetime
from typing import Optional

from .config_loader import load_settings
from .models import EmailTemplateRef

logger = logging.getLogger("myreminder")


def _get_grasp_exe() -> str:
    settings = load_settings()
    return settings.get("grasp", {}).get(
        "executable",
        "C:\\Users\\nwf\\AppData\\Local\\Toolbox\\bin\\grasp-mcp.exe",
    )


def _call_mcp_tool(tool_name: str, arguments: dict, timeout: int = 45) -> Optional[dict]:
    """Call a GRASP MCP tool via stdio JSON-RPC protocol."""
    exe = _get_grasp_exe()
    cmd = [exe, "serve", "--quiet"]

    # JSON-RPC initialize + tool call
    init_msg = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "myreminder", "version": "0.1.0"},
        },
    })

    initialized_notif = json.dumps({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
    })

    tool_msg = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments,
        },
    })

    # Send all messages via stdin, separated by newlines
    stdin_data = f"{init_msg}\n{initialized_notif}\n{tool_msg}\n"

    try:
        result = subprocess.run(
            cmd,
            input=stdin_data,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        # Parse responses — look for the tool call response (id: 2)
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                if msg.get("id") == 2:
                    # Tool call response
                    if "error" in msg:
                        logger.error(f"MCP tool error: {msg['error']}")
                        return None
                    content = msg.get("result", {}).get("content", [])
                    for item in content:
                        if item.get("type") == "text":
                            return json.loads(item["text"])
                    return msg.get("result")
            except json.JSONDecodeError:
                continue

        logger.warning(f"No response found for tool call: {tool_name}")
        return None

    except subprocess.TimeoutExpired:
        logger.error(f"GRASP MCP call timed out: {tool_name}")
        return None
    except Exception as e:
        logger.error(f"GRASP bridge error: {e}")
        return None


def search_email_template(template_ref: EmailTemplateRef) -> Optional[dict]:
    """Search for an email template/draft matching the reference."""
    result = _call_mcp_tool("get_emails", {
        "folder": template_ref.folder,
        "maxResults": 20,
    })
    if not result:
        return None

    emails = result if isinstance(result, list) else result.get("emails", [])
    search_term = template_ref.subject_contains.lower()

    for email in emails:
        subject = (email.get("subject") or "").lower()
        body = (email.get("bodyPreview") or "").lower()
        if search_term in subject or search_term in body:
            logger.info(f"Found email template: {email.get('subject')}")
            return email

    logger.info(
        f"No email matching '{template_ref.subject_contains}' "
        f"in folder '{template_ref.folder}'"
    )
    return None


def create_calendar_event(
    subject: str,
    duration_minutes: int = 15,
    body: Optional[str] = None,
) -> Optional[dict]:
    """Create a calendar event via GRASP starting now."""
    now = datetime.datetime.now().astimezone()
    start = now.strftime("%Y-%m-%dT%H:%M:%S%z")
    # Insert colon in timezone offset for ISO-8601 compliance
    if "+" in start or start.count("-") > 2:
        start = start[:-2] + ":" + start[-2:]

    args = {
        "subject": subject,
        "startDateTime": start,
        "durationMinutes": duration_minutes,
    }
    if body:
        args["body"] = body

    return _call_mcp_tool("create_calendar_event", args)


def check_grasp_available() -> bool:
    """Check if GRASP MCP is available and authenticated."""
    result = _call_mcp_tool("get_profile", {})
    return result is not None
