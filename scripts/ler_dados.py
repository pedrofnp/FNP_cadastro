import pandas as pd
from base.models import Estado, Municipio, Partido, Interesse, Cargo # Substitua "myapp" pelo nome do seu app

def carregar_xls():
    # Carregar o arquivo XLS
    xls_file = r'C:\Users\phillippi.alkmin\Desktop\contatos\scripts\data\muns.xlsx'
    
    # Ler o arquivo usando pandas (assumindo que o arquivo tenha colunas 'estado' e 'municipio')
    df = pd.read_excel(xls_file)

    # Iterar sobre o DataFrame e adicionar os dados ao banco de dados
    for index, row in df.iterrows():
        estado_nome = row['UF']
        municipio_nome = row['NOME DO MUNICÍPIO']
        pop = row['pop']
        capitais = row['capitais']
        nome_met = row['NOME_CATMETROPOL']
        met = row['met']
        regiao = row['Regiao']

        
        # Verifica se o estado já existe no banco
        estado, created = Estado.objects.get_or_create(nome=estado_nome)
        if created:
            print(f"Estado criado: {estado_nome}")
        else:
            print(f"Estado já existia: {estado_nome}")
        
        # Cria o município com o estado associado
        Municipio.objects.get_or_create(nome=municipio_nome, estado=estado, regiao_metropolitana = met, capital = capitais,
                                        mais_de_80_mil_hab = pop, nome_metropolitana = nome_met, nome_regiao = regiao )

    print("Dados carregados com sucesso!")


def carregar_xlsx():
    # Carregar o arquivo XLS
    xls_file = r'C:\Users\phillippi.alkmin\Desktop\contatos\scripts\data\partidos.xlsx'
    
    # Ler o arquivo usando pandas (assumindo que o arquivo tenha colunas 'estado' e 'municipio')
    df = pd.read_excel(xls_file)

    # Iterar sobre o DataFrame e adicionar os dados ao banco de dados
    for index, row in df.iterrows():
        partido_nome = row['partidos']
        
        # Verifica se o estado já existe no banco
        partido, created = Partido.objects.get_or_create(nome=partido_nome)
        if created:
            print(f"Estado criado: {partido_nome}")
        else:
            print(f"Estado já existia: {partido_nome}")

    print("Dados carregados com sucesso!")

def ler_interesses(lista):
    interests = lista

    for interest in interests:
        Interesse.objects.get_or_create(nome=interest)

def ler_cargos(lista):
    cargos = lista

    for cargo in cargos:
        Cargo.objects.get_or_create(nome=cargo) 