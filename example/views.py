from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import TagProblema, Instituicao, RecursoAjuda, User
from .serializers import *

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class InstituicaoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InstituicaoSerializer
    def get_queryset(self):
        # Retorna instituições que atendem os problemas do usuário logado
        return Instituicao.objects.filter(tags__in=self.request.user.problemas.all()).distinct()

class RecursoAjudaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecursoAjudaSerializer
    def get_queryset(self):
        return RecursoAjuda.objects.filter(tag__in=self.request.user.problemas.all())