from django.test import TestCase
from django.contrib.auth.models import User, Group
from drivers.models import Driver
from common.constants import SHIFT_CHOICES


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
