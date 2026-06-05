"""Reminder scheduler using the schedule library."""
import logging
import schedule
import time
import threading
from typing import Callable

from .models import Reminder
from .config_loader import load_reminders
from .notifier import show_toast, execute_actions

logger = logging.getLogger("myreminder")

_stop_event = threading.Event()


def _fire_reminder(reminder: Reminder) -> None:
    """Fire a single reminder: show toast and execute actions."""
    logger.info(f"Firing reminder: {reminder.name}")
    show_toast(reminder)
    execute_actions(reminder)


def _register_reminder(reminder: Reminder) -> None:
    """Register a single reminder with the schedule library."""
    sched = reminder.schedule
    t = sched.time

    if sched.type == "daily":
        schedule.every().day.at(t).do(_fire_reminder, reminder).tag(reminder.id)

    elif sched.type == "weekly":
        day = (sched.day or "monday").lower()
        day_map = {
            "monday": schedule.every().monday,
            "tuesday": schedule.every().tuesday,
            "wednesday": schedule.every().wednesday,
            "thursday": schedule.every().thursday,
            "friday": schedule.every().friday,
            "saturday": schedule.every().saturday,
            "sunday": schedule.every().sunday,
        }
        job = day_map.get(day, schedule.every().monday)
        job.at(t).do(_fire_reminder, reminder).tag(reminder.id)

    elif sched.type == "monthly":
        # schedule lib doesn't natively support monthly, so we use daily
        # check and filter by day of month
        dom = sched.day_of_month or 1

        def _monthly_check(r=reminder, target_dom=dom):
            import datetime
            if datetime.datetime.now().day == target_dom:
                _fire_reminder(r)

        schedule.every().day.at(t).do(_monthly_check).tag(reminder.id)

    logger.info(
        f"Registered: {reminder.name} ({sched.type} at {t})"
    )


def reload_reminders() -> int:
    """Clear all jobs and reload from config. Returns count of active reminders."""
    schedule.clear()
    reminders = load_reminders()
    count = 0
    for r in reminders:
        if r.enabled:
            _register_reminder(r)
            count += 1
    logger.info(f"Loaded {count} active reminders")
    return count


def run_scheduler() -> None:
    """Run the scheduler loop in the current thread."""
    reload_reminders()
    logger.info("Scheduler started")
    while not _stop_event.is_set():
        schedule.run_pending()
        _stop_event.wait(timeout=30)
    logger.info("Scheduler stopped")


def start_scheduler_thread() -> threading.Thread:
    """Start the scheduler in a background thread."""
    _stop_event.clear()
    t = threading.Thread(target=run_scheduler, daemon=True, name="scheduler")
    t.start()
    return t


def stop_scheduler() -> None:
    """Signal the scheduler to stop."""
    _stop_event.set()
