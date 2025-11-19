from django.test import TestCase
from django.contrib.auth.models import User
from drivers.models import Driver


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
