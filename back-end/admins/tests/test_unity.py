from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated

from admins.models import Admin
from admins.admin import AdminModelAdmin
from admins.views import AdminListCreateView, AdminRetrieveUpdateDestroyView
from admins.serializers import AdminSerializer, AdminCreateSerializer


# Funcionalidades 1 e 2
class AdminModelTests(TestCase):

    def test_CT_01_admin_role_automatically_set(self):
        user = User.objects.create_user("testrole", "role@test.com", "pass123")
        admin = Admin.objects.create(user=user, name="Test Role", phone="123")

        self.assertEqual(admin.role, "admin")

    def test_CT_02_admin_permissions_and_groups_set(self):
        user = User.objects.create_user("testgroup", "group@test.com", "pass123")
        Group.objects.create(name="admins")

        Admin.objects.create(user=user, name="Test Group", phone="123")

        self.assertTrue(user.groups.filter(name="admins").exists())
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_CT_03_str_method(self):
        user = User.objects.create_user("strtest", "str@test.com", "pass123")
        admin = Admin.objects.create(user=user, name="Admin Teste Str", phone="123")

        self.assertEqual(str(admin), "Admin: Admin Teste Str")


# Funcionalidade 4
class AdminCreateSerializerTests(TestCase):

    def test_CT_06_create_method_logic(self):
        data = {
            "name": "TesteAdmin",
            "phone": "12345678910",
            "email": "mariarita@teste.com",
            "password": "senha123",
        }
        # mcock grupos
        Group.objects.create(name="admins")

        serializer = AdminCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        admin = serializer.save()

        self.assertIsInstance(admin, Admin)
        self.assertEqual(admin.name, "TesteAdmin")
        self.assertEqual(admin.phone, "12345678910")

        user = admin.user
        self.assertEqual(user.username, "mariarita@teste.com")
        self.assertEqual(user.email, "mariarita@teste.com")
        self.assertTrue(user.check_password("senha123"))

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.groups.filter(name="admins").exists())


# Funcionalidades 3 e 5
class AdminViewTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_CT_04_get_serializer_class_get_method(self):
        view = AdminListCreateView()
        view.request = self.factory.get("/")
        self.assertEqual(view.get_serializer_class(), AdminSerializer)

    def test_CT_05_get_serializer_class_post_method(self):
        view = AdminListCreateView()
        view.request = self.factory.post("/")
        self.assertEqual(view.get_serializer_class(), AdminCreateSerializer)

    def test_CT_07_to_09_retrieve_view_configuration(self):
        view = AdminRetrieveUpdateDestroyView()

        self.assertEqual(view.queryset.model, Admin)

        self.assertEqual(view.serializer_class, AdminSerializer)

        perm_classes = view.permission_classes
        self.assertTrue(
            any(issubclass(p, IsAuthenticated) for p in perm_classes)
            or IsAuthenticated in perm_classes
        )


# Funcionalidade 6
class AdminSiteTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.superuser = User.objects.create_superuser("super", "s@s.com", "pass")
        self.admin_model_admin = AdminModelAdmin(model=Admin, admin_site=None)
        Group.objects.create(name="admins")

    def test_CT_10_save_model_integration(self):
        request = self.factory.get("/")
        request.user = self.superuser

        user = User.objects.create_user("novo@teste.com", "novo@teste.com", "senha123")
        # admin ainda não salvo
        admin = Admin(user=user, name="Admin Teste", phone="123456789")

        self.admin_model_admin.save_model(request, admin, form=None, change=False)

        self.assertTrue(user.groups.filter(name="admins").exists())
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
