from django.test import TestCase
from rest_framework.test import APIRequestFactory
from boarding_points.models import BoardingPoint
from boarding_points.views import BoardingPointViewSet
from boarding_points.serializers import BoardingPointSerializer


class BoardingPointModelTests(TestCase):

    # Funcionalidade 1
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

    # Funcionalidade 4
    def test_CT_04_meta_ordering(self):
        ponto_1 = BoardingPoint.objects.create(name="Ponto A", route_order=3)
        ponto_2 = BoardingPoint.objects.create(name="Ponto B", route_order=1)
        ponto_3 = BoardingPoint.objects.create(name="Ponto C", route_order=2)

        pontos = BoardingPoint.objects.all()

        self.assertEqual(list(pontos), [ponto_2, ponto_3, ponto_1])

    # Funcionalidade 5
    def test_CT_05_delete_boarding_point_reorders(self):
        ponto_1 = BoardingPoint.objects.create(name="Ponto 1", route_order=1)
        ponto_2 = BoardingPoint.objects.create(name="Ponto 2", route_order=2)
        ponto_3 = BoardingPoint.objects.create(name="Ponto 3", route_order=3)

        ponto_2.delete()

        pontos = BoardingPoint.objects.all()

        self.assertEqual(pontos[0].route_order, 1)
        self.assertEqual(pontos[0].name, "Ponto 1")

        self.assertEqual(pontos[1].route_order, 2)
        self.assertEqual(pontos[1].name, "Ponto 3")

    # Funcionalidade 5
    def test_CT_06_create_boarding_point_adjusts_order(self):
        ponto_1 = BoardingPoint.objects.create(name="Ponto 1", route_order=0)
        ponto_2 = BoardingPoint.objects.create(name="Ponto 2", route_order=0)

        ponto_1.refresh_from_db()
        ponto_2.refresh_from_db()

        self.assertEqual(ponto_1.route_order, 1)
        self.assertEqual(ponto_2.route_order, 0)

    # Funcionalidade 5
    def test_CT_07_create_boarding_point_at_end(self):
        ponto_1 = BoardingPoint.objects.create(name="Garagem", route_order=0)
        ponto_2 = BoardingPoint.objects.create(name="Hotel Alvorada", route_order=1)

        ponto_3 = BoardingPoint.objects.create(
            name="Farmácia Santa Luzia", route_order=2
        )
        ponto_3.refresh_from_db()

        self.assertEqual(ponto_1.route_order, 0)
        self.assertEqual(ponto_2.route_order, 1)
        self.assertEqual(ponto_3.route_order, 2)

    def test_CT_08_insert_middle(self):
        ponto_1 = BoardingPoint.objects.create(name="Ponto A", route_order=0)
        ponto_2 = BoardingPoint.objects.create(name="Ponto B", route_order=1)

        novo_ponto = BoardingPoint.objects.create(name="Ponto C", route_order=1)
        ponto_1.refresh_from_db()
        ponto_2.refresh_from_db()
        novo_ponto.refresh_from_db()

        assert ponto_1.route_order == 0
        assert novo_ponto.route_order == 1
        assert ponto_2.route_order == 2


class BoardingPointViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = BoardingPointViewSet()
        self.view.serializer_class = BoardingPointSerializer
        self.view.queryset = BoardingPoint.objects.all()

    def test_CT_09_serializer_class(self):
        self.assertEqual(self.view.serializer_class, BoardingPointSerializer)

    def test_CT_10_queryset(self):
        self.assertEqual(self.view.queryset.model, BoardingPoint)
