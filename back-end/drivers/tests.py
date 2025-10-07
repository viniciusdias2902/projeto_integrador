from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Driver


class DriverAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="driveruser", password="driverpass123"
        )
        self.group, _ = Group.objects.get_or_create(name="drivers")
        self.user.groups.add(self.group)

        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

        self.driver_data = {
            "name": "Travis Bickle",
            "phone": "1234567890",
            "shift": "A",
            "email": "travis.bickle@example.com",
            "password": "InsertCoin123",
        }

        self.driver = Driver.objects.create(
            user=self.user,
            name="Existing Driver",
            phone="0987654321",
            shift="N",
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_admin(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_driver(self):
        self.authenticate_admin()
        url = reverse("drivers-create-list")
        response = self.client.post(url, self.driver_data, format="json")
        print("STATUS:", response.status_code)
        print("RESPONSE:", response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Driver.objects.filter(name="Travis Bickle").exists())

    def test_list_driver_authenticated(self):
        self.authenticate_admin()
        url = reverse("drivers-create-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_driver(self):
        self.authenticate_admin()
        url = reverse("drivers-retrieve-update-destroy", args=[self.driver.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Existing Driver")

    def test_update_driver(self):
        self.authenticate_admin()
        url = reverse("drivers-retrieve-update-destroy", args=[self.driver.id])
        data = {
            "name": "Updated Name",
            "phone": "8765321098",
            "shift": "M",
            "email": "update@example.com",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.driver.refresh_from_db()
        self.assertEqual(self.driver.name, "Updated Name")

    def test_delete_driver(self):
        self.authenticate_admin()
        url = reverse("drivers-retrieve-update-destroy", args=[self.driver.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Driver.objects.filter(id=self.driver.id).exists())
