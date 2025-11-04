from django.db import models
from django.contrib.auth.models import User, Group
from common.models import Person


class Admin(Person):
    def save(self, *args, **kwargs):
        if not self.role:
            self.role = "admin"

        super().save(*args, **kwargs)

        if self.user:
            group, _ = Group.objects.get_or_create(name="admins")
            self.user.groups.add(group)

            if not self.user.is_superuser:
                self.user.is_superuser = True
                self.user.is_staff = True
                self.user.save()

    def __str__(self):
        return f"Admin: {self.name}"
