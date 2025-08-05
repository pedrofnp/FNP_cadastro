# base/adimplencia.py
import requests

URL_ADIMPLENTES = 'https://script.google.com/a/macros/fnp.org.br/s/AKfycbzy2CEUcJQHzktIFUz1Bq9ATrrHERopLEhvJe4m1a0Os2iS2K125KDNHGOOXLd9qhFp4A/exec'

# Cache local para não fazer várias requisições
_adimplentes_cache = None

def carregar_adimplentes():
    global _adimplentes_cache
    if _adimplentes_cache is None:
        try:
            response = requests.get(URL_ADIMPLENTES, timeout=5)
            response.raise_for_status()
            dados = response.json()
            _adimplentes_cache = {
                f"{item['municipio']} - {item['uf']}": True
                for item in dados if item.get('municipio') and item.get('uf')
            }
        except Exception as e:
            print(f"[ERRO] Falha ao carregar lista de adimplentes: {e}")
            _adimplentes_cache = {}
    return _adimplentes_cache

def verificar_adimplente(nome_municipio_completo):
    """
    Exemplo do nome esperado: 'Rio de Janeiro - RJ'
    """
    adimplentes = carregar_adimplentes()
    return adimplentes.get(nome_municipio_completo, False)
