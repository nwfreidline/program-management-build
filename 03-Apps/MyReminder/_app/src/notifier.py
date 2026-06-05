"""Windows toast notification handler."""
import os
import subprocess
import logging
import threading
from typing import Optional

from .models import Reminder

logger = logging.getLogger("myreminder")

# Track whether we're in a context where windows_toasts is safe
# (i.e., NOT running alongside a tkinter mainloop)
_use_powershell_fallback = False


def set_powershell_fallback(enabled: bool) -> None:
    """Force PowerShell toast fallback (use when tkinter is active)."""
    global _use_powershell_fallback
    _use_powershell_fallback = enabled


def show_toast(reminder: Reminder) -> None:
    """Show a Windows toast notification for a reminder."""
    message = reminder.notification.message
    if reminder.actions.email_template:
        message += "\n\U0001f4e7 Email template linked."

    title = reminder.notification.title

    if _use_powershell_fallback:
        _powershell_toast(title, message)
        logger.info(f"Toast shown (PowerShell) for: {reminder.name}")
        return

    try:
        from windows_toasts import Toast, WindowsToaster

        toaster = WindowsToaster("MyReminder")
        toast = Toast()
        toast.text_fields = [title, message]
        toaster.show_toast(toast)
        logger.info(f"Toast shown for: {reminder.name}")
    except ImportError:
        _powershell_toast(title, message)
    except Exception as e:
        logger.error(f"Failed to show toast: {e}")
        _powershell_toast(title, message)


def _powershell_toast(title: str, message: str) -> None:
    """Fallback toast via PowerShell."""
    script = f"""
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom, ContentType = WindowsRuntime] | Out-Null
    $template = @"
    <toast>
        <visual>
            <binding template="ToastGeneric">
                <text>{title}</text>
                <text>{message}</text>
            </binding>
        </visual>
    </toast>
"@
    $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xml.LoadXml($template)
    $toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
    [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("MyReminder").Show($toast)
    """
    try:
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-Command", script],
            capture_output=True,
            timeout=10,
        )
    except Exception as e:
        logger.error(f"PowerShell toast fallback failed: {e}")


def _launch_popup(reminder: Reminder) -> None:
    """Launch a popup window as a separate process."""
    try:
        from .popup import launch_popup_process

        # Build actions dict for the popup
        actions_dict = {
            "openFiles": reminder.actions.open_files,
            "openFolders": reminder.actions.open_folders,
            "createCalendarEvent": reminder.actions.create_calendar_event,
        }
        if reminder.actions.email_template:
            actions_dict["emailTemplate"] = {
                "folder": reminder.actions.email_template.folder,
                "subjectContains": reminder.actions.email_template.subject_contains,
            }

        launch_popup_process(
            title=reminder.notification.title,
            message=reminder.notification.message,
            actions=actions_dict,
        )
        logger.info(f"Popup launched for: {reminder.name}")
    except Exception as e:
        logger.error(f"Failed to launch popup: {e}")


def execute_actions(reminder: Reminder) -> None:
    """Execute the linked actions for a reminder."""
    actions = reminder.actions

    # Launch popup window (separate process, non-blocking)
    _launch_popup(reminder)

    # Open linked files
    for filepath in actions.open_files:
        if os.path.exists(filepath):
            os.startfile(filepath)
            logger.info(f"Opened file: {filepath}")

    # Open linked folders
    for folderpath in actions.open_folders:
        if os.path.exists(folderpath):
            os.startfile(folderpath)
            logger.info(f"Opened folder: {folderpath}")

    # GRASP: look up email template
    if actions.email_template:
        try:
            from .grasp_bridge import search_email_template
            result = search_email_template(actions.email_template)
            if result:
                subject = result.get("subject", "Unknown")
                logger.info(f"Found email template: {subject}")
            else:
                logger.info(
                    f"No email template found for: "
                    f"{actions.email_template.subject_contains}"
                )
        except Exception as e:
            logger.error(f"GRASP email lookup failed: {e}")

    # GRASP: create calendar event
    if actions.create_calendar_event:
        try:
            from .grasp_bridge import create_calendar_event
            result = create_calendar_event(
                subject=f"[Reminder] {reminder.name}",
                duration_minutes=15,
                body=reminder.notification.message,
            )
            if result:
                logger.info(f"Calendar event created for: {reminder.name}")
            else:
                logger.warning(f"Calendar event creation returned no result")
        except Exception as e:
            logger.error(f"GRASP calendar event failed: {e}")
