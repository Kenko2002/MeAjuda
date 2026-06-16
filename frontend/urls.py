from django.urls import path
from .views import login_view, logout_view, home_view, profile_view, comunidades_view, comunidade_detalhe_view

urlpatterns = [
    path("login/", login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('perfil/', profile_view, name='perfil'),
    path('comunidades/', comunidades_view, name='comunidades'),
    path('comunidades/<int:pk>/', comunidade_detalhe_view, name='comunidade_detalhe'),
    path('', home_view, name='home'),
]