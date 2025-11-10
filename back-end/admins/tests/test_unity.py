from django.test import TestCase
from admins.models import Admin
from django.contrib.auth.models import User


class AdminsTest(TestCase):
    def test_admin_role_automatically_set(self):
        admin = Admin.objects.create(
            user=User.objects.create_user(
                username="testrole@example.com", password="testpass123"
            ),
            name="Test Role Admin",
            phone="5555555555",
        )

        self.assertEqual(admin.role, "admin")

    def test_admin_added_to_admins_group(self):
        user = User.objects.create_user(
            username="testgroup@example.com", password="testpass123"
        )
        admin = Admin.objects.create(
            user=user,
            name="Test Group Admin",
            phone="6666666666",
        )

        self.assertTrue(user.groups.filter(name="admins").exists())
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_str_method(self):
        user = User.objects.create_user(username="mrlsn", password="senha123")
        admin = Admin.objects.create(
            user=user, name="Admin Teste Str", phone="40028022"
        )
        self.assertEqual(str(admin), "Admin: Admin Teste Str")
