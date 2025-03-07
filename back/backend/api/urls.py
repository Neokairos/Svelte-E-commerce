from django.urls import path,include
from rest_framework.routers import DefaultRouter

from .views import (
    LoginAPIView,
    LogoutAPIView,
    RegistrationAPIView,
    UserRetrieveUpdateAPIView,
    ProductViewSet
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'products',ProductViewSet)

urlpatterns = [
    path('register', RegistrationAPIView.as_view(), name='register_user'),
    path('login', LoginAPIView.as_view(), name='login_user'),
    path('logout', LogoutAPIView.as_view(), name="logout_user"),
    path('user', UserRetrieveUpdateAPIView.as_view(), name='user'),  # kwargs={'id': None},
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
urlpatterns += router.urls
