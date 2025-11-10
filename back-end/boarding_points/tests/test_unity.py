from django.test import TestCase
from boarding_points.models import BoardingPoint


class BoardingPointTests(TestCase):
    def test_create_boarding_point(self):
        boarding_point = BoardingPoint.objects.create(
            name="Hotel Alvorada", address_reference="Em frente ao IBE", route_order=1
        )
        self.assertEqual(boarding_point.name, "Hotel Alvorada")
        self.assertEqual(boarding_point.address_reference, "Em frente ao IBE")
        self.assertEqual(boarding_point.route_order, 1)

    def test_boarding_points_ordering(self):
        boarding_points1 = BoardingPoint.objects.create(
            name="Rodoviária", route_order=2
        )
        boarding_points2 = BoardingPoint.objects.create(
            name="Machado AutoPeças", route_order=1
        )

        boarding_points = list(BoardingPoint.objects.all())
        self.assertEqual(boarding_points[0], boarding_points2)
        self.assertEqual(boarding_points[1], boarding_points1)
