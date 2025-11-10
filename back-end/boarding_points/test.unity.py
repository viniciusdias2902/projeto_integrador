from django.test import TestCase


class BoardingPointTests(TestCase):
    def test_create_boarding_point(self):
        boarding_point = BoardingPoint.objects.create(
            name="Hotel Alvorada", address_reference="Em frente ao IBE", route_order=1
        )
        self.assertEqual(boarding_point.name, "Rodoviária")
        self.assertEqual(boarding_point.address_reference, "Em frente ao IBE")
        self.assertEqual(boarding_point.route_order, 1)
