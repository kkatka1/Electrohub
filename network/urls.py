from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from .apps import NetworkConfig
from .views import NetworkPointViewSet, ContactViewSet, ProductViewSet, RegisterView

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r"networkpoints", NetworkPointViewSet, basename="networkpoints")
router.register(r"contacts", ContactViewSet, basename="contacts")
router.register(r"products", ProductViewSet, basename="products")

urlpatterns = [
    path("api/", include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls
