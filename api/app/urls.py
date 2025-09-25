from django.contrib import admin
from django.urls import path, include
from common.views import BoardingPointViewSet

router = DefaultRouter()

router.register(r'boarding-points', BoardingPointViewSet, basename='boarding-point')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("authentication.urls")),
    path("api/v1/", include("students.urls")),
    path("api/v1/", include("drivers.urls")),
    path("api/v1/", include("polls.urls")),
    
    path("api/v1/", include(router.urls)),
]
