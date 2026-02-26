from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser, Profile, Aba, Resposta
from .serializers import UserRegistrationSerializer, ProfileSerializer, AbaSerializer, RespostaSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Resposta

# 1. Cadastro de Usuário
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

# 2. Gerenciamento do Perfil (GET para ver se existe, POST para criar)
class ProfileView(APIView):
    # Força o Django a usar JWT para esta view
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Exception:
            return Response({"detail": "Não encontrado"}, status=404)

    def post(self, request):
        # Tenta atualizar se já existir, ou cria se não existir
        profile, created = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 3. Listar as 7 Abas e suas Perguntas
#class AbaListView(generics.ListAPIView):
#    queryset = Aba.objects.all().order_by('ordem')
#    serializer_class = AbaSerializer
#    permission_classes = [permissions.IsAuthenticated]
    #permission_classes = [permissions.AllowAny]



class AbaListView(APIView):
    def get(self, request):
        # Verifica se o usuário logado já tem alguma resposta salva
        ja_respondeu = Resposta.objects.filter(user=request.user).exists()
        
        if ja_respondeu:
            # Retorna um sinalizador para o frontend
            return Response({"ja_respondido": True}, status=200)
            
        # Caso contrário, retorna as abas normalmente
        abas = Aba.objects.all()
        serializer = AbaSerializer(abas, many=True)
        return Response(serializer.data)


# 4. Salvar múltiplas respostas de uma vez
class SubmitRespostasView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Espera uma lista de respostas: [{"pergunta": 1, "peso": 5}, ...]
        serializer = RespostaSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"detail": "Respostas salvas com sucesso!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

@api_view(['POST'])
@permission_classes([AllowAny])
def login_or_register(request):
    """
    Se o usuário existir, faz login.
    Se não existir, cria usuário com senha padrão e retorna token.
    """
    email = request.data.get('email')
    password = request.data.get('password')  # opcional, podemos ignorar para primeiro acesso

    if not email:
        return Response({"detail": "E-mail é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

    user, created = CustomUser.objects.get_or_create(email=email, defaults={'password': '12345678'})
    if created:
        # Se foi criado, define senha
        user.set_password(password or '12345678')
        user.save()

    # Gera token JWT
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'created': created  # diz se é usuário novo
    })    