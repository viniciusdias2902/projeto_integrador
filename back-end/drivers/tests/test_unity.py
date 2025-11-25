from django.test import TestCase
from django.contrib.auth.models import User, Group
from drivers.models import Driver
from common.constants import SHIFT_CHOICES
from drivers.serializers import DriverSerializer, DriverCreateSerializer
from django.apps import apps
from drivers.apps import DriversConfig


class DriverModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="dom", password="password123")

    # Funcionalidade 1
    def test_CT_01_driver_role_is_set_to_driver_on_save(self):
        driver = Driver.objects.create(
            user=self.user,
            name="Sem usuário",
            phone="1234567",
            shift="A",
            dailyPaymentCents=10000,
        )

        self.assertEqual(driver.role, "driver")

    # Funcionalidade 2
    def test_CT_02_driver_user_added_to_group(self):
        driver = Driver.objects.create(
            name="DriverTest",
            user=self.user,
            shift=SHIFT_CHOICES[0][0],
            dailyPaymentCents=13000,
        )

        self.assertTrue(Group.objects.filter(name="drivers").exists())
        group = Group.objects.get(name="drivers")
        self.assertIn(driver.user, group.user_set.all())

    # Funcionalidade 3
    def test_CT_03_create_driver_sucess(self):
        data = {
            "name": "CreateDriverTest",
            "phone": "9876543215",
            "shift": SHIFT_CHOICES[1][0],
            "email": "motorista@exemplo.com",
            "password": "senha123",
            "dailyPaymentCents": 1000,
        }

        serializer = DriverCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        driver = serializer.save()

        self.assertIsInstance(driver.user, User)
        self.assertEqual(driver.user.email, data["email"])
        self.assertTrue(driver.user.check_password(data["password"]))

        self.assertTrue(driver.user.groups.filter(name="drivers").exists())

        self.assertEqual(driver.name, data["name"])
        self.assertEqual(driver.dailyPaymentCents, data["dailyPaymentCents"])

    # Funcionalidade 4
    def test_CT_04_missing_required_fields(self):
        data = {
            "name": "Gabryel",
            "phone": "9876543215",
            "shift": SHIFT_CHOICES[1][0],
        }
        serializer = DriverCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertIn("password", serializer.errors)

    # Funcionalidade 5
    def test_CT_05_get_email_returns_email(self):
        from django.contrib.admin.sites import AdminSite
        from drivers.admin import DriverModelAdmin

        driver = Driver.objects.create(
            user=self.user,
            name="EmailTestDriver",
            phone="1234567890",
            shift="A",
            dailyPaymentCents=15000,
        )
        admin = DriverModelAdmin(Driver, AdminSite())
        email = admin.get_email(driver)
        self.assertEqual(email, self.user.email)

    # Funcionalidade 6
    def test_CT_06_app_config_name(self):
        self.assertEqual(DriversConfig.name, "drivers")
        self.assertEqual(apps.get_app_config("drivers").name, "drivers")

    def test_CT_07_app_config_class(self):
        config = apps.get_app_config("drivers")
        self.assertIsInstance(config, DriversConfig)
