import os
import requests
import pandas as pd
from django.core.files.base import ContentFile
from base.models import Contato # Substitua `myapp` pelo nome do seu app
from django.conf import settings


def carregar_xls():
    # Caminho do arquivo Excel
    excel_path = os.path.join(settings.BASE_DIR, 'scripts\\data\\meus_dados.xlsx')  # Atualize com o caminho real do Excel
    
    # Carrega o Excel
    df = pd.read_excel(excel_path)
    
    # Itera sobre cada linha do DataFrame e cria o Prefeito no banco de dados
    for index, row in df.iterrows():
        nome = row['nome']  # Nome da coluna com o nome do prefeito
        estado_id = row['ID_Estado']
        municipio_id= row['ID_Municipio']  # Nome da coluna com o município
        partido_id = row['ID_Partidos']
        foto_url = row['foto_caminho']  # Coluna com o URL da foto
        # Cria a instância do Prefeito
        prefeito = Contato(nome=nome, estado_id=estado_id, municipio_id=municipio_id, partido_id = partido_id, cargo_id = 1, 
                       foto_url=foto_url)

        # Baixa e salva a foto se o URL estiver disponível
        #if pd.notna(foto_url):  # Verifica se o URL não é NaN
        #    response = requests.get(foto_url)
        #    if response.status_code == 200:
        #        # Extrai o nome do arquivo da URL e armazena a imagem
        #        foto_nome = os.path.basename(foto_url)
        #        prefeito.foto.save(foto_nome, ContentFile(response.content), save=True)

        prefeito.save()  # Salva o prefeito no banco de dados
