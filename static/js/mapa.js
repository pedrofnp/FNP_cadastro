document.addEventListener('DOMContentLoaded', async function () {
  let map;
  let marker = null;
  let geojson = [];

  const select = document.getElementById('municipio_id');
  const mapaDiv = document.getElementById('mapa');
  const dadosDiv = document.getElementById('dados_municipio');
  const statusDiv = document.getElementById('status_adimplencia');

  if (!select || !mapaDiv || !dadosDiv || !statusDiv) {
    console.error("Algum elemento necessário não foi encontrado no DOM.");
    return;
  }

  console.log("Select encontrado com sucesso:", select.outerHTML);

  // Inicializa o mapa centralizado no Brasil
  map = L.map(mapaDiv).setView([-14.235, -51.9253], 4);

  // Camada base do OpenStreetMap
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  // Função para normalizar nomes de municípios (sem acento, tudo maiúsculo)
  const normalizar = s => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase();

  // Carrega o arquivo de coordenadas locais
  try {
    const res = await fetch('/static/data/vermapa.json');
    geojson = await res.json();
    console.log('GeoJSON carregado:', geojson.length, 'itens');
  } catch (err) {
    alert('Erro ao carregar vermapa.json');
    console.error(err);
    return;
  }

  // Evento para captura da seleção do usuário via Select2
  $('#municipio_id').on('select2:select', async function (e) {
    const nome = e.params.data.id;
    console.log('Município selecionado:', nome);

    const ponto = geojson.find(m => normalizar(m.municipio) === normalizar(nome));
    if (!ponto || !ponto.lat || !ponto.lng) {
      alert('Município não encontrado no arquivo de coordenadas.');
      return;
    }

    // Limpa marcador anterior se houver
    if (marker) map.removeLayer(marker);

    // Move o mapa e adiciona marcador novo
    map.setView([ponto.lat, ponto.lng], 11);
    marker = L.marker([ponto.lat, ponto.lng]).addTo(map).bindPopup(nome).openPopup();

    // Zera dados exibidos enquanto carrega
    dadosDiv.innerHTML = 'Carregando dados...';
    statusDiv.innerHTML = '';

    // Tenta buscar na API
    try {
      const apiResp = await fetch(`/api/municipio/${encodeURIComponent(nome)}/`);
      if (!apiResp.ok) throw new Error('Não encontrado');

      const dados = await apiResp.json();
      statusDiv.innerHTML = dados.adimplente
        ? '<span class="text-success">Município Adimplente</span>'
        : '<span class="text-danger">Município Inadimplente</span>';

      dadosDiv.innerHTML = `
        <b>Município:</b> ${dados.municipio}<br>
        <b>UF:</b> ${dados.uf}<br>
        <b>População:</b> ${dados.populacao.toLocaleString('pt-BR')}
      `;
    } catch (err) {
      console.warn('Erro na API, tentando fallback:', err);
      try {
        const fallbackRes = await fetch('/static/data/db_sqmunicipio.json');
        const fallbackData = await fallbackRes.json();
        const dados = fallbackData.find(m => normalizar(m.municipio) === normalizar(nome));

        if (dados) {
          dadosDiv.innerHTML = `
            <b>Município:</b> ${dados.municipio}<br>
            <b>UF:</b> ${dados.uf}<br>
            <b>População:</b> ${dados.populacao.toLocaleString('pt-BR')}
          `;
        } else {
          dadosDiv.innerHTML = 'Município não encontrado na base local.';
        }
      } catch (e) {
        dadosDiv.innerHTML = 'Erro ao buscar informações locais.';
        console.error(e);
      }
    }
  });
});
