from drivers.models import Driver
from django.test import TestCase
from django.contrib.auth.models import User, Group


class DriverModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="dom", password="password123")

    def test_ct01_driver_role_is_set_to_driver_on_save(self):
        driver = Driver.objects.create(
            user=self.user,
            name="Sem usuário",
            phone="1234567",
            shift="A",
            dailyPaymentCents=10000,
        )
        self.assertEqual(driver.role, "driver")
