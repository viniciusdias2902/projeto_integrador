from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        person = (
            getattr(user, "student", None)
            or getattr(user, "driver", None)
            or getattr(user, "admin", None)
        )

        token["role"] = getattr(person, "role", "unknown")

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # ✅ CORREÇÃO: Adicionar busca por admin
        person = (
            getattr(self.user, "student", None)
            or getattr(self.user, "driver", None)
            or getattr(self.user, "admin", None)
        )

        data["role"] = getattr(person, "role", "unknown")
        return data
