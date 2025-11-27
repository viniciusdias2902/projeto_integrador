from django.core.management.base import BaseCommand
from django.utils import timezone
from polls.models import Poll
from datetime import timedelta


class Command(BaseCommand):
    help = "Create polls for next week (Monday to Friday) and remove old polls"

    def handle(self, *args, **kwargs):
        today = timezone.localtime(timezone.now()).date()
        
        if today.weekday() != 5:
            self.stdout.write(
                self.style.WARNING("This command should only run on Saturdays")
            )
            return

        next_monday = today + timedelta(days=2)
        
        Poll.objects.filter(date__lt=next_monday).delete()
        
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
                    f"Created polls for dates: {', '.join(created_polls)}"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS("All polls for next week already exist")
            )