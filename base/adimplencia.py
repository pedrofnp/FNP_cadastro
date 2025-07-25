# base/adimplencia.py
def verificar_adimplente(nome_municipio):
    adimplentes = [
        "Brasília", "São Paulo", "Rio de Janeiro", "Curitiba"  # ← temporário, simula planilha
    ]
    return nome_municipio in adimplentes
