document.addEventListener('DOMContentLoaded', async function () {
  let map;
  let marker = null;
  let geojson = [];
  let participacoesAtuais = [];

  const select = document.getElementById('municipio_id');
  const mapaDiv = document.getElementById('mapa');
  const dadosDiv = document.getElementById('dados_municipio');
  const statusDiv = document.getElementById('status_adimplencia');

  const infoNome = document.getElementById('info_nome');
  const infoUF = document.getElementById('info_uf');
  const infoPopulacao = document.getElementById('info_populacao');
  const infoParticipacao = document.getElementById('info_participacao');

  const formEdicao = document.getElementById('form_edicao');
  const formMunicipio = document.getElementById('form_municipio');
  const btnEditar = document.getElementById('btn_editar');
  const btnCancelar = document.getElementById('btn_cancelar');
  const projetoSelect = document.getElementById('projeto_select');
  const listaDiv = document.getElementById('lista_participacao');
  const btnAddProjeto = document.getElementById('btn_add_projeto');

  function renderParticipacoes() {
    listaDiv.innerHTML = '';
    if (participacoesAtuais.length === 0) {
      listaDiv.innerHTML = '<em>Nenhuma categoria adicionada</em>';
      return;
    }
    participacoesAtuais.forEach((p, idx) => {
      const item = document.createElement('div');
      item.classList.add('d-flex', 'align-items-center', 'mb-1');
      item.innerHTML = `
        <span class="me-2">${p}</span>
        <button type="button" 
              class="btn btn-sm btn-outline-danger p-0 px-2 fw-bold" 
              style="line-height:1;" 
              data-index="${idx}">&times;</button>
          `;
      listaDiv.appendChild(item);
    });
  }

  // Inicializa mapa
  map = L.map(mapaDiv).setView([-14.235, -51.9253], 4);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  const normalizar = s => s.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toUpperCase();

  try {
    const res = await fetch('/static/data/vermapa.json');
    geojson = await res.json();
  } catch (err) {
    alert('Erro ao carregar vermapa.json');
    return;
  }

  // Seleção de município
  $('#municipio_id').on('select2:select', async function (e) {
    const nome = e.params.data.id;
    const ponto = geojson.find(m => normalizar(m.municipio) === normalizar(nome));
    if (!ponto) {
      alert('Município não encontrado no arquivo de coordenadas.');
      return;
    }

    if (marker) map.removeLayer(marker);
    map.setView([ponto.lat, ponto.lng], 11);
    marker = L.marker([ponto.lat, ponto.lng]).addTo(map).bindPopup(nome).openPopup();

    dadosDiv.style.display = 'block';
    [infoNome, infoUF, infoPopulacao, infoParticipacao].forEach(el => el.textContent = '');
    formMunicipio.value = nome;
    participacoesAtuais = [];

    try {
      const apiResp = await fetch(`/api/municipio/${encodeURIComponent(nome)}/`);
      const dados = await apiResp.json();

      statusDiv.innerHTML = dados.adimplente
        ? '<span class="text-success fw-bold">Município Adimplente</span>'
        : '<span class="text-danger fw-bold">Município Inadimplente</span>';

      infoNome.textContent = dados.municipio || '';
      infoUF.textContent = dados.uf || '';
      infoPopulacao.textContent = dados.populacao ? dados.populacao.toLocaleString('pt-BR') : '';
      participacoesAtuais = Array.isArray(dados.participacao) ? dados.participacao : [];
      infoParticipacao.textContent = participacoesAtuais.join(', ');
      renderParticipacoes();

    } catch (err) {
      console.warn('Erro na API:', err);
    }
  });

  // Adicionar categoria
  btnAddProjeto.addEventListener('click', () => {
    const projeto = projetoSelect.value;
    if (projeto && !participacoesAtuais.includes(projeto)) {
      participacoesAtuais.push(projeto);
      renderParticipacoes();
      infoParticipacao.textContent = participacoesAtuais.join(', ');
    }
  });

  // Remover categoria
  listaDiv.addEventListener('click', (e) => {
    if (e.target.tagName === 'BUTTON') {
      const idx = parseInt(e.target.dataset.index, 10);
      participacoesAtuais.splice(idx, 1);
      renderParticipacoes();
      infoParticipacao.textContent = participacoesAtuais.join(', ');
    }
  });

  // Botões editar/cancelar
  btnEditar.addEventListener('click', () => {
    document.getElementById('dados_exibicao').style.display = 'none';
    formEdicao.style.display = 'block';
  });

  btnCancelar.addEventListener('click', () => {
    formEdicao.style.display = 'none';
    document.getElementById('dados_exibicao').style.display = 'block';
  });

  // Salvar via AJAX
  formEdicao.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(formEdicao);
    formData.delete('projeto');
    formData.append('participacao', JSON.stringify(participacoesAtuais));
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
      const response = await fetch(formEdicao.action, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrftoken
        }
      });

      const result = await response.json();
      infoParticipacao.textContent = (result.participacao || []).join(', ');
      participacoesAtuais = Array.isArray(result.participacao) ? result.participacao : [];
      renderParticipacoes();
      formEdicao.style.display = 'none';
      document.getElementById('dados_exibicao').style.display = 'block';
      alert('Alterações salvas com sucesso!');
    } catch (error) {
      alert('Erro ao salvar as alterações.');
    }
  });
});

// Inicializa Select2
$(document).ready(function () {
  $('#municipio_id').select2({
    placeholder: "Selecione um município",
    width: 'resolve',
    language: { noResults: () => "Nenhum município encontrado" }
  });
});
