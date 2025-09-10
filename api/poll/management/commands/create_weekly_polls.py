from django.core.management.base import BaseCommand
from ...models import Poll
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Create polls for next week (Monday to Friday)"

    def handle(self, *args, **kwargs):
        today = date.today()
        next_monday = today + timedelta(days=2)

        created_polls = []

        for i in range(5):
            poll_date = next_monday + timedelta(days=i)
            poll, created = Poll.objects.get_or_create(
                date=poll_date, defaults={"status": "open"}
            )
            if created:
                created_polls.append(str(poll_date))

        if created_polls:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created polls for next week: {', '.join(created_polls)}"
                )
            )
        else:
            self.stdout.write("Polls for next week already exist.")
