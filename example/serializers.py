from rest_framework import serializers
from .models import User, TagProblema, Instituicao, RecursoAjuda

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'problemas')

    def create(self, validated_data):
        probs = validated_data.pop('problemas', [])
        user = User.objects.create_user(**validated_data)
        user.problemas.set(probs)
        return user

class TagProblemaSerializer(serializers.ModelSerializer):
    class Meta: model = TagProblema; fields = '__all__'

class InstituicaoSerializer(serializers.ModelSerializer):
    class Meta: model = Instituicao; fields = '__all__'

class RecursoAjudaSerializer(serializers.ModelSerializer):
    tag_nome = serializers.ReadOnlyField(source='tag.nome')
    class Meta: model = RecursoAjuda; fields = '__all__'