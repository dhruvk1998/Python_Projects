from datetime import datetime, time, timedelta, date
from zoneinfo import ZoneInfo

class WorkCalendar:
    def __init__(self,
                 work_start: time = time(9, 0),
                 work_end: time = time(17, 0),
                 working_days: set[int] = {0, 1, 2, 3, 4},
                 holidays: set[date] | None = None,
                 timezone: str = "America/Vancouver"):
        self.work_start = work_start
        self.work_end = work_end
        self.working_days = working_days
        self.holidays = holidays or set()
        self.tz = ZoneInfo(timezone)

    def is_working_day(self, d: date) -> bool:
        return d.weekday() in self.working_days and d not in self.holidays

    def within_working_hours(self, dt: datetime) -> bool:
        local = dt.astimezone(self.tz)
        return (
            self.is_working_day(local.date()) and
            (self.work_start <= local.time() < self.work_end)
        )

    def next_work_start(self, after: datetime) -> datetime:
        local = after.astimezone(self.tz)
        d, t = local.date(), local.time()

        if self.is_working_day(d) and t < self.work_start:
            return datetime.combine(d, self.work_start, tzinfo=self.tz)

        while not self.is_working_day(d) or t >= self.work_end:
            d += timedelta(days=1)
            t = time(0, 0)
            if (d - after.date()).days > 365:
                raise ValueError("No working day found within 1 year.")

        return datetime.combine(d, self.work_start, tzinfo=self.tz)

    def advance_to_work_start_if_needed(self, dt: datetime) -> datetime:
        return dt if self.within_working_hours(dt) else self.next_work_start(dt)

    def add_working_hours(self, start: datetime, hours: float) -> datetime:
        current = self.advance_to_work_start_if_needed(start)
        remaining = hours

        while remaining > 1e-9:
            today_end = datetime.combine(current.date(), self.work_end, tzinfo=self.tz)

            if current >= today_end:
                current = self.next_work_start(current + timedelta(minutes=1))
                continue

            available = (today_end - current).total_seconds() / 3600.0
            consume = min(remaining, available)

            current += timedelta(hours=consume)
            remaining -= consume

            if remaining > 1e-9:
                current = self.next_work_start(current + timedelta(minutes=1))

        return current

    def compute_deadline(self, received_at: datetime, sla_hours: float = 6.0) -> datetime:
        return self.add_working_hours(received_at, sla_hours)

    def should_transfer_to_B(self, received_at: datetime,
                             responded_at: datetime | None,
                             sla_hours: float = 6.0) -> tuple[bool, datetime]:
        deadline = self.compute_deadline(received_at, sla_hours)
        transfer = responded_at is None or responded_at > deadline
        return transfer, deadline


if __name__ == "__main__":
    calendar = WorkCalendar(
        work_start=time(9, 0),
        work_end=time(17, 0),
        holidays={date(2025, 12, 25)},
        timezone="America/Vancouver"
    )

    received = datetime(2025, 9, 26, 16, 0, tzinfo=calendar.tz)
    deadline = calendar.compute_deadline(received, 6)
    print("Received:", received)
    print("Deadline:", deadline)

    transfer, dl = calendar.should_transfer_to_B(received_at=received, responded_at=None, sla_hours=6)
    print("Transfer to B?", transfer, "| Deadline:", dl)

    responded = datetime(2025, 9, 29, 13, 30, tzinfo=calendar.tz)
    transfer2, dl2 = calendar.should_transfer_to_B(received_at=received, responded_at=responded, sla_hours=6)
    print("Responded:", responded, "| Transfer to B?", transfer2, "| Deadline:", dl2)




#Received: 2025-09-26 16:00:00-07:00
#Deadline: 2025-09-29 14:00:00-07:00
#Transfer to B? True | Deadline: 2025-09-29 14:00:00-07:00
#Responded: 2025-09-29 13:30:00-07:00 | Transfer to B? #False | Deadline: 2025-09-29 14:00:00-07:00