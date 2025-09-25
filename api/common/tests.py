from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BoardingPoint

class BoardingPointAPITests(APITestCase):
    def setUp(self):
       
        self.admin_user = User.objects.create_superuser(
            username="admin", password="adminpass"
        )
        self.student_user = User.objects.create_user(
            username="aluno_comum", password="alunopass"
        )
        self.boarding_point = BoardingPoint.objects.create(
            name="Ponto Teste Existente", route_order=1
        )

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate_as_admin(self):
        token = self.get_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    
    def authenticate_as_student(self):
        token = self.get_jwt_token(self.student_user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_admin_can_create_boarding_point(self):
       
        self.authenticate_as_admin()
        url = reverse("boarding-point-list")
        payload = {
            "name": "Ponto Novo Criado por Admin",
            "route_order": 2
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(BoardingPoint.objects.filter(name="Ponto Novo Criado por Admin").exists())
