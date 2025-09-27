from datetime import datetime, time, timedelta, date

WORK_START = time(9, 0)   # 09:00
WORK_END   = time(17, 0)  # 17:00
WORKING_DAYS = {0, 1, 2, 3, 4}  # Monday=0 ... Sunday=6 (Mon–Fri)
HOLIDAYS = set()  # e.g., {date(2025, 12, 25), date(2025, 1, 1)}

def is_working_day(d: date) -> bool:
    return d.weekday() in WORKING_DAYS and d not in HOLIDAYS

def within_working_hours(dt: datetime) -> bool:
    return is_working_day(dt.date()) and (WORK_START <= dt.time() < WORK_END)

def next_work_start(after: datetime) -> datetime:
    """Return the next datetime at WORK_START on a valid working day at or after 'after'."""
    d = after.date()
    t = after.time()

    # If we're before work start on a working day, start today at 09:00
    if is_working_day(d) and t < WORK_START:
        return datetime.combine(d, WORK_START)

    # Otherwise move to the next working day at 09:00
    d += timedelta(days=0 if (is_working_day(d) and t < WORK_END and t >= WORK_START) else 1)
    while not is_working_day(d):
        d += timedelta(days=1)
    return datetime.combine(d, WORK_START)

def advance_to_work_start_if_needed(dt: datetime) -> datetime:
    """If dt is outside working hours, jump to the next work start."""
    if within_working_hours(dt):
        return dt
    return next_work_start(dt)

def add_working_hours(start: datetime, hours: float) -> datetime:
    """
    Add 'hours' working hours to 'start', counting only between WORK_START and WORK_END
    on working days (skips nights/weekends/holidays).
    """
    current = advance_to_work_start_if_needed(start)
    remaining = hours

    while remaining > 1e-9:
        # End of today's work window
        today_end = datetime.combine(current.date(), WORK_END)

        # If we somehow landed past today's end, jump to next start
        if current >= today_end:
            current = next_work_start(current + timedelta(minutes=1))
            continue

        # Hours available today
        available = (today_end - current).total_seconds() / 3600.0

        # Consume what's possible today
        consume = min(remaining, available)
        current += timedelta(hours=consume)
        remaining -= consume

        # If there's still time to add, jump to next working day start
        if remaining > 1e-9:
            current = next_work_start(current + timedelta(minutes=1))

    return current

# --- Lead logic for XYZ (A -> B transfer after 6 working hours if no response) ---

def compute_deadline(received_at: datetime, sla_hours: float = 6.0) -> datetime:
    """Deadline when A's ownership expires, counting only working hours."""
    return add_working_hours(received_at, sla_hours)

def should_transfer_to_B(received_at: datetime,
                         responded_at: datetime | None,
                         sla_hours: float = 6.0) -> tuple[bool, datetime]:
    """
    Returns (transfer, deadline).
    transfer=True if no response by the deadline (i.e., responded_at is None or > deadline).
    """
    deadline = compute_deadline(received_at, sla_hours)
    transfer = responded_at is None or responded_at > deadline
    return transfer, deadline

# ------------------ Demo / Examples ------------------
if __name__ == "__main__":
    # Example from your scenario: A receives lead at 16:00 (4 pm) on a working day.
    rx = datetime(2025, 9, 26, 16, 0)  # Fri, 26 Sep 2025, 16:00
    deadline = compute_deadline(rx, 6)
    print("Received:", rx)
    print("Deadline:", deadline)  # -> Next working day 14:00 (2 pm), skipping off-hours

    # No response: transfer to B
    transfer, dl = should_transfer_to_B(received_at=rx, responded_at=None, sla_hours=6)
    print("Transfer to B?", transfer, "| Deadline:", dl)

    # Responded next day at 13:30 -> no transfer
    resp = datetime(2025, 9, 29, 13, 30)  # Monday 13:30 (if weekend in between)
    transfer2, dl2 = should_transfer_to_B(received_at=rx, responded_at=resp, sla_hours=6)
    print("Responded:", resp, "| Transfer to B?", transfer2, "| Deadline:", dl2)

    # Configure holidays if needed:
    # HOLIDAYS.add(date(2025, 9, 29))