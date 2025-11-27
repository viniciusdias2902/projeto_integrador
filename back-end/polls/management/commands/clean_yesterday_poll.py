from django.core.management.base import BaseCommand
from django.utils import timezone
from polls.models import Poll
from datetime import timedelta


class Command(BaseCommand):
    help = "Remove yesterday's poll (runs Tuesday to Friday)"

    def handle(self, *args, **kwargs):
        today = timezone.localtime(timezone.now()).date()
        weekday = today.weekday()
        
        if weekday < 1 or weekday > 4:
            self.stdout.write(
                self.style.WARNING(
                    "This command should only run Tuesday to Friday (weekday 1-4)"
                )
            )
            return

        yesterday = today - timedelta(days=1)
        
        deleted_polls = Poll.objects.filter(date=yesterday)
        count = deleted_polls.count()
        deleted_polls.delete()

        if count > 0:
            self.stdout.write(
                self.style.SUCCESS(f"Deleted poll for date: {yesterday}")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f"No poll found for date: {yesterday}")
            )