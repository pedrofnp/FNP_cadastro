import json
import os
import requests
import time

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(BASE_DIR, 'db_sqmunicipio.json')
output_path = os.path.join(BASE_DIR, 'vermapa.json')

# Lê o arquivo com os municípios
with open(input_path, 'r', encoding='utf-8') as f:
    municipios_data = json.load(f)

resultado = []

for m in municipios_data:
    nome = m['municipio']
    uf = m['uf']
    print(f'Consultando: {nome}/{uf}...')

    url = f'https://nominatim.openstreetmap.org/search?city={nome}&state={uf}&country=Brazil&format=json&limit=1'
    headers = {'User-Agent': 'GeoCoderBot/1.0'}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data:
            lat = float(data[0]['lat'])
            lng = float(data[0]['lon'])
            resultado.append({
                "municipio": nome,
                "uf": uf,
                "lat": lat,
                "lng": lng
            })
            print(f"✓ Coordenadas: {lat}, {lng}")
        else:
            print(f"✗ Não encontrado: {nome}/{uf}")
    except Exception as e:
        print(f"Erro em {nome}/{uf}: {e}")

    time.sleep(1)  # Respeita o rate limit da API

# Salva o arquivo final
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print(f"\n✔️ Arquivo salvo em: {output_path}")
