"""Data models for MyReminder."""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EmailTemplateRef:
    folder: str
    subject_contains: str


@dataclass
class ReminderActions:
    email_template: Optional[EmailTemplateRef] = None
    open_files: list[str] = field(default_factory=list)
    open_folders: list[str] = field(default_factory=list)
    create_calendar_event: bool = False


@dataclass
class Schedule:
    type: str  # "daily", "weekly", "monthly", "once"
    time: str = "09:00"
    day: Optional[str] = None  # for weekly: "monday", "tuesday", etc.
    day_of_month: Optional[int] = None  # for monthly: 1-28


@dataclass
class Notification:
    title: str
    message: str


@dataclass
class Reminder:
    id: str
    name: str
    enabled: bool
    schedule: Schedule
    notification: Notification
    actions: ReminderActions
