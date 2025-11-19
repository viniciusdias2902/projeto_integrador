from django.test import TestCase
from boarding_points.models import BoardingPoint


class BoardingPointModelTests(TestCase):

    # funcionaldiade 1
    def test_CT_01_create_boarding_point_attributes(self):
        boarding_point = BoardingPoint.objects.create(
            name="Hotel Alvorada", address_reference="Em frente ao IBE", route_order=1
        )

        self.assertEqual(boarding_point.name, "Hotel Alvorada")
        self.assertEqual(boarding_point.address_reference, "Em frente ao IBE")
        self.assertEqual(boarding_point.route_order, 1)

    # Funcionalidade 2
    def test_CT_02_boarding_points_ordering(self):

        ponto_2 = BoardingPoint.objects.create(name="Rodoviária", route_order=2)
        # Cria o ponto 1 depois
        ponto_1 = BoardingPoint.objects.create(name="Machado AutoPeças", route_order=1)

        pontos_do_banco = list(BoardingPoint.objects.all())

        self.assertEqual(pontos_do_banco[0], ponto_1)
        self.assertEqual(pontos_do_banco[0].name, "Machado AutoPeças")

        self.assertEqual(pontos_do_banco[1], ponto_2)
        self.assertEqual(pontos_do_banco[1].name, "Rodoviária")

    # Fucnoalidade 3
    def test_CT_03_str_representation(self):
        point = BoardingPoint.objects.create(name="Praça", route_order=5)
        self.assertEqual(str(point), "5: Praça")
