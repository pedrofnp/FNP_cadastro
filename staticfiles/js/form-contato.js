// Atualiza municípios ao trocar o estado
document.getElementById('estado').addEventListener('change', function() {
    var estadoId = this.value;
    var municipioSelect = document.getElementById('municipio');

    municipioSelect.innerHTML = '<option value="">Todos os Municípios</option>';

    if (estadoId) {
        fetch(`/get-municipios/${estadoId}/?format=dash`)
            .then(response => response.json())
            .then(data => {
                data.forEach(function(municipio) {
                    var option = document.createElement('option');
                    option.value = municipio.id;
                    option.text = municipio.nome;
                    municipioSelect.add(option);
                });
            })
            .catch(error => console.error('Erro ao buscar municípios:', error));
    }
});

// Inicializa select2 em interesses
$(document).ready(function() {
    $('#id_interesses').select2({
        placeholder: 'Selecione seus interesses',
        allowClear: true,
        width: '100%'
    }).next('.select2').find('.select2-selection').addClass('form-control');
});

// Inicializa select2 com múltipla seleção
$('#multiple-select-custom-field').select2({
    theme: "bootstrap-5",
    width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
    placeholder: $(this).data('placeholder'),
    closeOnSelect: false,
    tags: true
});
