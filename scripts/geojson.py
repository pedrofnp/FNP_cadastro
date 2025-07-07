import json
import os
from django.conf import settings

# Caminho para o arquivo GeoJSON original
geojson_path = os.path.join(settings.BASE_DIR, 'static\\geojson\\grandes_regioes_json.geojson')

# Carregar o arquivo GeoJSON original
with open(geojson_path, 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Extrair apenas os campos necessários
dados_simplificados = [
    {
        "NOME1": feature["properties"]["NOME1"],
        "SIGLA": feature["properties"]["SIGLA"]
    }
    for feature in geojson_data["features"]
]

# Caminho para salvar o arquivo JSON simplificado
output_path = os.path.join(settings.BASE_DIR, 'static\\geojson\\dados_regioes_simplificado.json')

# Salvar como um arquivo JSON simplificado
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(dados_simplificados, f, ensure_ascii=False, indent=2)

print("Arquivo JSON simplificado criado com sucesso:", output_path)
