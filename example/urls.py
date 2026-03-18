from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from example.views import InstituicaoViewSet, RecursoAjudaViewSet, RegisterView

router = DefaultRouter()
router.register(r'instituicoes', InstituicaoViewSet, basename='instituicoes')
router.register(r'recursos', RecursoAjudaViewSet, basename='recursos')

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Auth & Login
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API
    path('api/', include(router.urls)),
    
    # Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]