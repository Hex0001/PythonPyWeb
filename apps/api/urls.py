from django.urls import path, include
from .views import AuthorAPIView
from .views import AuthorGenericAPIView
from .views import AuthorViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

app_name = 'api'

router = DefaultRouter()
router.register(r'authors_viewset', AuthorViewSet, basename='authors-viewset')

urlpatterns = [
    path('authors/', AuthorAPIView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorAPIView.as_view(), name='author-detail'),
    path('authors_generic/', AuthorGenericAPIView.as_view(), name='author-generic-list'),
    path('authors_generic/<int:pk>/', AuthorGenericAPIView.as_view(), name='author-generic-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление токена
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Проверка токена
    path('', include(router.urls)),
]
