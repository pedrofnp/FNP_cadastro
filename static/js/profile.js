 document.getElementById('estado').addEventListener('change', function() {
            var estadoId = this.value;
            var municipioSelect = document.getElementById('municipio');
            
            // Limpa os municípios antigos
            municipioSelect.innerHTML = '<option value="">Selecione um Município</option>';
            
            if (estadoId) {
                // Faz uma requisição AJAX para buscar os municípios do estado selecionado
                fetch(`/get-municipios/${estadoId}/?format=dash`)
                    .then(response => response.json())
                    .then(data => {
                        // Preenche o campo de municípios com os dados recebidos
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
              $(document).ready(function() {
                  $('#id_interesses').select2({
                      placeholder: 'Selecione seus interesses',
                      allowClear: true,
                      width: '100%'  // Forçar o tamanho da caixa para se ajustar ao container
                  }).next('.select2').find('.select2-selection').addClass('form-control');
              });
