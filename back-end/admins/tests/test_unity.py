from django.test import TestCase
from admins.models import Admin
from django.contrib.auth.models import User
from admins.views import AdminListCreateView, AdminRetrieveUpdateDestroyView
from admins.serializers import AdminSerializer, AdminCreateSerializer


class AdminsTest(TestCase):
    def test_ct01_admin_role_automatically_set(self):
        admin = Admin.objects.create(
            user=User.objects.create_user(
                username="testrole@example.com", password="testpass123"
            ),
            name="Test Role Admin",
            phone="5555555555",
        )

        self.assertEqual(admin.role, "admin")

    def test_ct02_admin_added_to_admins_group(self):
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

    def test_ct03_str_method(self):
        user = User.objects.create_user(username="mrlsn", password="senha123")
        admin = Admin.objects.create(
            user=user, name="Admin Teste Str", phone="40028022"
        )
        self.assertEqual(str(admin), "Admin: Admin Teste Str")

    def test_ct04_get_serializer_class_get(self):
        view = AdminListCreateView()
        view.request = type("Request", (object,), {"method": "GET"})()
        self.assertEqual(view.get_serializer_class(), AdminSerializer)

    def test_ct05_create_method(self):
        data = {
            "name": "TesteAdmin",
            "phone": "12345678910",
            "email": "admin@teste.com",
            "password": "senha123",
        }

        serializer = AdminCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        admin = serializer.save()

        self.assertIsInstance(admin, Admin)
        self.assertEqual(admin.name, "TesteAdmin")
        self.assertEqual(admin.phone, "12345678910")

        user = admin.user
        self.assertEqual(user.username, "admin@teste.com")
        self.assertEqual(user.email, "admin@teste.com")
        self.assertTrue(user.check_password("senha123"))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

        self.assertTrue(user.groups.filter(name="admins").exists())

    def test_ct06_view_uses_admin_queryset(self):
        view = AdminRetrieveUpdateDestroyView()
        self.assertEqual(view.queryset.model, Admin)
        self.assertEqual(self.view.serializer_class, AdminSerializer)

        permissions = [permissions.__name__ for permissions in view.permission_classes]
        self.assertIn("IsAuthenticated", permissions)
        self.assertIn("IsAdminUser", permissions)
