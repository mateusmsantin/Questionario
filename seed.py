import os
import django

# Configuração para o script reconhecer o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from questionario.models import Aba, Pergunta

def populate():
    print("Iniciando a população de dados...")

    dados = {
        "1. Dimensão Ambiental": [
            "Como você avalia a qualidade da água da Lagoa Mirim?",
            "Qual a importância da preservação da mata ciliar para a região?",
            "Como você vê o impacto da pesca predatória no ecossistema?"
        ],
        "2. Dimensão Social": [
            "Qual o nível de engajamento das comunidades locais no projeto?",
            "O projeto respeita as tradições das populações ribeirinhas?",
            "Como você avalia o acesso à informação sobre as ações da lagoa?"
        ],
        "3. Dimensão Econômica": [
            "Qual o impacto do projeto na geração de renda local?",
            "Como você avalia o potencial turístico sustentável da região?",
            "O incentivo ao comércio local é satisfatório?"
        ],
        "4. Gestão e Governança": [
            "A comunicação entre governo e sociedade civil é eficiente?",
            "Como você avalia a transparência no uso dos recursos?",
            "A fiscalização ambiental na lagoa é rigorosa o suficiente?"
        ],
        "5. Infraestrutura": [
            "As vias de acesso à lagoa estão em boas condições?",
            "Como você avalia a sinalização e pontos de apoio aos visitantes?",
            "A infraestrutura para pesquisa científica é adequada?"
        ],
        "6. Educação e Pesquisa": [
            "O projeto promove educação ambiental nas escolas da região?",
            "Há incentivo para pesquisas acadêmicas sobre a biodiversidade?",
            "Como você avalia o conhecimento da população sobre a Lagoa Mirim?"
        ],
        "7. Perspectivas Futuras": [
            "Qual sua expectativa para a sustentabilidade da lagoa nos próximos 10 anos?",
            "O projeto está preparado para enfrentar mudanças climáticas?",
            "Você indicaria o projeto para parcerias com outras instituições?"
        ]
    }

    for i, (nome_aba, perguntas) in enumerate(dados.items(), 1):
        aba, created = Aba.objects.get_or_create(nome=nome_aba, ordem=i)
        if created:
            print(f"Aba criada: {nome_aba}")
        
        for texto_pergunta in perguntas:
            Pergunta.objects.get_or_create(aba=aba, texto=texto_pergunta)
            print(f"  Pergunta adicionada à {nome_aba}")

    print("População concluída com sucesso!")

if __name__ == '__main__':
    populate()