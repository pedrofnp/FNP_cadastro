// base.js

// 1. Botão de toggle da sidebar
document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.querySelector('.sidebar-fixed');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function () {
      sidebar.classList.toggle('show');
    });
  }

  // 2. Atualiza municípios quando o estado é alterado
  const estadoSelect = document.getElementById('estado');
  const municipioSelect = document.getElementById('municipio');

  if (estadoSelect && municipioSelect) {
    estadoSelect.addEventListener('change', function () {
      const estadoId = this.value;
      municipioSelect.innerHTML = '<option value="">Selecione um Município</option>';

      if (estadoId) {
        fetch(`/get-municipios/${estadoId}/?format=dash`)
          .then(response => response.json())
          .then(data => {
            data.forEach(function (municipio) {
              const option = document.createElement('option');
              option.value = municipio.id;
              option.text = municipio.nome;
              municipioSelect.appendChild(option);
            });
          })
          .catch(error => console.error('Erro ao buscar municípios:', error));
      }
    });
  }

  // 3. Ativa Select2 para o campo de interesses, se existir
  const interessesSelect = document.getElementById('id_interesses');
  if (interessesSelect && typeof $ !== 'undefined') {
    $(interessesSelect).select2({
      placeholder: 'Selecione seus interesses',
      allowClear: true,
      width: '100%'
    }).next('.select2').find('.select2-selection').addClass('form-control');
  }
});
