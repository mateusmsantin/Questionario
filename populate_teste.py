# populate_test_data.py
import random
from faker import Faker
from questionario.models import CustomUser, Profile, Aba, Pergunta, Resposta

fake = Faker('pt_BR')

NUM_USERS = 100
NUM_RESPONSES = 100

# Limpa dados antigos (opcional)
# CustomUser.objects.filter(email__contains='teste_user_').delete()

# Cria ou pega uma aba e pergunta existentes
aba, _ = Aba.objects.get_or_create(nome="Ambiental")
perguntas = list(Pergunta.objects.filter(aba=aba))
if not perguntas:
    # Se não houver pergunta, cria uma
    perguntas.append(Pergunta.objects.create(aba=aba, texto="A lagoa é importante?"))

# Criação de usuários e profiles
users = []
for i in range(NUM_USERS):
    email = f"teste_user_{i}@teste.com"
    password = "123456"
    user = CustomUser.objects.create(email=email)
    user.set_password(password)
    user.save()
    
    profile = Profile.objects.create(
        user=user,
        nome_completo=fake.name(),
        email_contato=fake.email(),
        telefone=fake.phone_number(),
        cpf=fake.cpf(),
        faixa_etaria=random.choice(['A18','19_30','31_40','41_50','51_60','60+']),
        genero=random.choice(['MC','HC','MT','HT','NB','PNR','OUT']),
        raca=random.choice(['IND','AFR','BRA','PAR','ASI','PNR','OUT']),
        nome_organizacao=fake.company(),
        localidade_organizacao=fake.city(),
        tipo_organizacao=random.choice(['SOC','IND','GOV','EDU','PRI','OUT']),
        participou_projeto=random.choice([True, False])
    )
    users.append(user)

print("Populando respostas...")

# Pega TODAS as perguntas existentes no banco
todas_perguntas = list(Pergunta.objects.all())

if not todas_perguntas:
    print("Erro: Nenhuma pergunta encontrada no banco.")
else:
    for user in users:
        for pergunta in todas_perguntas:
            # Cria uma resposta para cada pergunta para cada usuário
            Resposta.objects.create(
                user=user,
                pergunta=pergunta,
                peso=random.randint(1, 5)
            )

print(f"{NUM_USERS} usuários criados com Profiles.")
print(f"Respostas populadas para todas as perguntas.")