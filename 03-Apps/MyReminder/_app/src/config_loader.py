"""Load and save reminder configurations."""
import json
import os
from pathlib import Path
from typing import Optional

from .models import (
    EmailTemplateRef,
    Notification,
    Reminder,
    ReminderActions,
    Schedule,
)

CONFIG_DIR = Path(__file__).parent.parent.parent / "config"


def get_reminders_path() -> Path:
    return CONFIG_DIR / "reminders.json"


def get_settings_path() -> Path:
    return CONFIG_DIR / "settings.json"


def load_settings() -> dict:
    path = get_settings_path()
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _parse_email_template(data: Optional[dict]) -> Optional[EmailTemplateRef]:
    if not data:
        return None
    return EmailTemplateRef(
        folder=data.get("folder", "drafts"),
        subject_contains=data.get("subjectContains", ""),
    )


def _parse_actions(data: dict) -> ReminderActions:
    return ReminderActions(
        email_template=_parse_email_template(data.get("emailTemplate")),
        open_files=data.get("openFiles", []),
        open_folders=data.get("openFolders", []),
        create_calendar_event=data.get("createCalendarEvent", False),
    )


def _parse_schedule(data: dict) -> Schedule:
    return Schedule(
        type=data["type"],
        time=data.get("time", "09:00"),
        day=data.get("day"),
        day_of_month=data.get("dayOfMonth"),
    )


def _parse_reminder(data: dict) -> Reminder:
    return Reminder(
        id=data["id"],
        name=data["name"],
        enabled=data.get("enabled", True),
        schedule=_parse_schedule(data["schedule"]),
        notification=Notification(
            title=data["notification"]["title"],
            message=data["notification"]["message"],
        ),
        actions=_parse_actions(data.get("actions", {})),
    )


def load_reminders() -> list[Reminder]:
    path = get_reminders_path()
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [_parse_reminder(r) for r in data.get("reminders", [])]


def save_reminders(reminders: list[Reminder]) -> None:
    path = get_reminders_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    def _serialize_reminder(r: Reminder) -> dict:
        actions = {
            "openFiles": r.actions.open_files,
            "openFolders": r.actions.open_folders,
            "createCalendarEvent": r.actions.create_calendar_event,
        }
        if r.actions.email_template:
            actions["emailTemplate"] = {
                "folder": r.actions.email_template.folder,
                "subjectContains": r.actions.email_template.subject_contains,
            }
        else:
            actions["emailTemplate"] = None

        sched = {"type": r.schedule.type, "time": r.schedule.time}
        if r.schedule.day:
            sched["day"] = r.schedule.day
        if r.schedule.day_of_month:
            sched["dayOfMonth"] = r.schedule.day_of_month

        return {
            "id": r.id,
            "name": r.name,
            "enabled": r.enabled,
            "schedule": sched,
            "notification": {
                "title": r.notification.title,
                "message": r.notification.message,
            },
            "actions": actions,
        }

    data = {"reminders": [_serialize_reminder(r) for r in reminders]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
