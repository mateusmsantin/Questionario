from rest_framework import serializers
from .models import CustomUser, Profile, Aba, Pergunta, Resposta

# Serializer para criar novos usuários
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Serializer para o Perfil (as 11 perguntas iniciais)
#class ProfileSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Profile
#        fields = '__all__'
#        read_only_fields = ['user']

# Serializer para as Perguntas
class PerguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pergunta
        fields = ['id', 'texto']

# Serializer para as Abas (contendo as perguntas dentro)
class AbaSerializer(serializers.ModelSerializer):
    perguntas = PerguntaSerializer(many=True, read_only=True)

    class Meta:
        model = Aba
        fields = ['id', 'nome', 'ordem', 'perguntas']

# Serializer para salvar a Resposta (peso 1 a 5)
class RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resposta
        fields = ['pergunta', 'peso']

from validate_docbr import CPF
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ['user']

    def validate_cpf(self, value):
        cpf = CPF()
        # Remove pontos e traços antes de validar
        clean_cpf = "".join(filter(str.isdigit, value))
        
        if not cpf.validate(clean_cpf):
            raise serializers.ValidationError("CPF inválido.")
            
        # O unique=True no model já cuida da duplicidade, 
        # mas aqui você pode customizar a mensagem se quiser:
        if Profile.objects.filter(cpf=clean_cpf).exists():
            raise serializers.ValidationError("Este CPF já está cadastrado no sistema.")
            
        return clean_cpf        