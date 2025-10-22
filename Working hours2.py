from datetime import datetime, time, timedelta, date
from zoneinfo import ZoneInfo


class WorkCalendar:
    """
    A configurable business-hours calendar that can compute working-hour additions,
    next work start times, and SLA-based deadlines (e.g., for LeadSquared lead transfer).
    """

    def __init__(
        self,
        work_start: time = time(9, 0),
        work_end: time = time(17, 0),
        working_days: set[int] = {0, 1, 2, 3, 4},  # Monday–Friday
        holidays: set[date] | None = None,
        timezone: str = "America/Vancouver",       # ✅ Correct timezone
    ):
        self.work_start = work_start
        self.work_end = work_end
        self.working_days = working_days
        self.holidays = holidays or set()
        self.tz = ZoneInfo(timezone)

    # ------------------------------------------------------------------
    # --- Basic utilities
    # ------------------------------------------------------------------

    def is_working_day(self, d: date) -> bool:
        """Return True if 'd' is a working day (not weekend or holiday)."""
        return d.weekday() in self.working_days and d not in self.holidays

    def within_working_hours(self, dt: datetime) -> bool:
        """Check if datetime is within working hours."""
        local = dt.astimezone(self.tz)
        return (
            self.is_working_day(local.date())
            and (self.work_start <= local.time() < self.work_end)
        )

    # ------------------------------------------------------------------
    # --- Core helpers
    # ------------------------------------------------------------------

    def next_work_start(self, after: datetime) -> datetime:
        """
        Return the next datetime at work_start on a valid working day at or after 'after'.
        Always returns a timezone-aware datetime.
        """
        local = after.astimezone(self.tz)
        d, t = local.date(), local.time()

        # Case 1: same day but before work start
        if self.is_working_day(d) and t < self.work_start:
            return datetime.combine(d, self.work_start, tzinfo=self.tz)

        # Move to next working day if it's after hours or non-working
        while not self.is_working_day(d) or t >= self.work_end:
            d += timedelta(days=1)
            t = time(0, 0)  # reset midnight
            # Safety guard to prevent infinite loop
            if (d - after.date()).days > 365:
                raise ValueError("No working day found within 1 year.")

        return datetime.combine(d, self.work_start, tzinfo=self.tz)

    def advance_to_work_start_if_needed(self, dt: datetime) -> datetime:
        """If dt is outside working hours, jump to the next valid work start."""
        return dt if self.within_working_hours(dt) else self.next_work_start(dt)

    # ------------------------------------------------------------------
    # --- Main computation
    # ------------------------------------------------------------------

    def add_working_hours(self, start: datetime, hours: float) -> datetime:
        """
        Add 'hours' working hours to 'start', counting only between work_start/work_end
        on working days (skips nights/weekends/holidays).
        """
        current = self.advance_to_work_start_if_needed(start)
        remaining = hours

        while remaining > 1e-9:
            today_end = datetime.combine(current.date(), self.work_end, tzinfo=self.tz)

            # If we reached/passed today's end, jump to next start
            if current >= today_end:
                current = self.next_work_start(current + timedelta(minutes=1))
                continue

            # Available working hours left today
            available = (today_end - current).total_seconds() / 3600.0
            consume = min(remaining, available)

            current += timedelta(hours=consume)
            remaining -= consume

            # Jump to next work day if still more to add
            if remaining > 1e-9:
                current = self.next_work_start(current + timedelta(minutes=1))

        return current

    # ------------------------------------------------------------------
    # --- SLA / Lead Escalation logic
    # ------------------------------------------------------------------

    def compute_deadline(self, received_at: datetime, sla_hours: float = 6.0) -> datetime:
        """Compute the SLA deadline, counting only business hours."""
        return self.add_working_hours(received_at, sla_hours)

    def should_transfer_to_B(
        self,
        received_at: datetime,
        responded_at: datetime | None,
        sla_hours: float = 6.0,
    ) -> tuple[bool, datetime]:
        """
        Returns (transfer, deadline)
        transfer=True if no response by the deadline.
        """
        deadline = self.compute_deadline(received_at, sla_hours)
        transfer = responded_at is None or responded_at > deadline
        return transfer, deadline


# ----------------------------------------------------------------------
# --- Example Usage / Demo
# ----------------------------------------------------------------------
if __name__ == "__main__":
    calendar = WorkCalendar(
        work_start=time(9, 0),
        work_end=time(17, 0),
        holidays={date(2025, 12, 25)},
        timezone="America/Vancouver",
    )

    # Example: A receives lead at 16:00 on Friday
    received = datetime(2025, 9, 26, 16, 0, tzinfo=calendar.tz)
    deadline = calendar.compute_deadline(received, 6)
    print("Received:", received)
    print("Deadline:", deadline)  # → Monday 14:00

    # No response → Transfer
    transfer, dl = calendar.should_transfer_to_B(received_at=received, responded_at=None, sla_hours=6)
    print("Transfer to B?", transfer, "| Deadline:", dl)

    # Responded next Monday 13:30 → No transfer
    responded = datetime(2025, 9, 29, 13, 30, tzinfo=calendar.tz)
    transfer2, dl2 = calendar.should_transfer_to_B(received_at=received, responded_at=responded, sla_hours=6)
    print("Responded:", responded, "| Transfer to B?", transfer2, "| Deadline:", dl2)




#Received: 2025-09-26 16:00:00-07:00
#Deadline: 2025-09-29 14:00:00-07:00
#Transfer to B? True | Deadline: 2025-09-29 14:00:00-07:00
#Responded: 2025-09-29 13:30:00-07:00 | Transfer to B? #False | Deadline: 2025-09-29 14:00:00-07:00