from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken
from admins.models import Admin


class AdminAPITestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username="superadmin",
            email="superadmin@example.com",
            password="superpass123",
        )

        self.regular_user = User.objects.create_user(
            username="regularuser", password="regularpass123"
        )

        self.admin_user = User.objects.create_superuser(
            username="admin@example.com",
            email="admin@example.com",
            password="adminpass123",
        )
        self.admin = Admin.objects.create(
            user=self.admin_user,
            name="Existing Admin",
            phone="9876543210",
        )

        self.admin_data = {
            "name": "New Admin User",
            "phone": "1234567890",
            "email": "newadmin@example.com",
            "password": "NewAdminPass123",
        }

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_superuser(self):
        token = self.get_jwt_token(self.superuser)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def authenticate_regular_user(self):
        token = self.get_jwt_token(self.regular_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_admin_as_superuser(self):
        self.authenticate_superuser()
        url = reverse("admins-create-list")
        response = self.client.post(url, self.admin_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Admin.objects.filter(name="New Admin User").exists())

        new_admin = Admin.objects.get(name="New Admin User")
        self.assertEqual(new_admin.role, "admin")
        self.assertTrue(new_admin.user.is_superuser)
        self.assertTrue(new_admin.user.is_staff)
        self.assertTrue(new_admin.user.groups.filter(name="admins").exists())

    def test_create_admin_as_regular_user_forbidden(self):
        self.authenticate_regular_user()
        url = reverse("admins-create-list")
        response = self.client.post(url, self.admin_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Admin.objects.filter(name="New Admin User").exists())

    def test_list_admins(self):
        self.authenticate_superuser()
        url = reverse("admins-create-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_admin(self):
        self.authenticate_superuser()
        url = reverse("admins-retrieve-update-destroy", args=[self.admin.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Existing Admin")
        self.assertEqual(response.data["role"], "admin")

    def test_update_admin(self):
        self.authenticate_superuser()
        url = reverse("admins-retrieve-update-destroy", args=[self.admin.id])
        data = {
            "name": "Updated Admin Name",
            "phone": "1112223334",
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.name, "Updated Admin Name")
        self.assertEqual(self.admin.phone, "1112223334")

    def test_delete_admin(self):
        self.authenticate_superuser()
        url = reverse("admins-retrieve-update-destroy", args=[self.admin.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Admin.objects.filter(id=self.admin.id).exists())
