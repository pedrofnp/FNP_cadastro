/* global bootstrap: false */
(() => {
  'use strict'
  const tooltipTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(tooltipTriggerEl => {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()

window.onload = function() {
  var partnersDiv = document.getElementById("partners");
  partnersDiv.scrollTop = partnersDiv.scrollHeight;
};

// Atualiza municípios ao trocar o estado
     document.getElementById('estado').addEventListener('change', function() {
    var estadoId = this.value;
    var municipioSelect = document.getElementById('municipio');
    
    // Limpa os municípios antigos
    municipioSelect.innerHTML = '<option value="">Todos os Municípios</option>';
    
    if (estadoId) {
        // Requisição AJAX com o formato 'home'
        fetch(`/get-municipios/${estadoId}/`)
            .then(response => response.json())
            .then(data => {
                // Adapte conforme o formato esperado na 'home'
                data['municipios'].forEach(function(municipio) {
                    var option = document.createElement('option');
                    option.value = municipio['id'];
                    option.text = municipio['nome'];
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

      function addEmailField() {
          const emailFieldsDiv = document.getElementById('additional-email-fields');
          const newEmailInputGroup = document.createElement('div');
          newEmailInputGroup.className = 'input-group mt-2';
    
          const newEmailInput = document.createElement('input');
          newEmailInput.type = 'email';
          newEmailInput.name = 'additional_emails';
          newEmailInput.placeholder = 'voce@email.com';
          newEmailInput.className = 'form-control';
    
          const removeButton = document.createElement('button');
          removeButton.className = 'btn btn-danger';
          removeButton.innerHTML = 'X'; // Texto do botão
          removeButton.onclick = function() {
              emailFieldsDiv.removeChild(newEmailInputGroup); // Remove o campo ao clicar
          };
    
          newEmailInputGroup.appendChild(newEmailInput);
          newEmailInputGroup.appendChild(removeButton); // Adiciona o botão de remoção
          emailFieldsDiv.appendChild(newEmailInputGroup);
      }
    
      function addTelephoneField() {
          const telephoneFieldsDiv = document.getElementById('additional-telephone-fields');
          const newTelephoneInputGroup = document.createElement('div');
          newTelephoneInputGroup.className = 'input-group mt-2';
    
          const newTelephoneInput = document.createElement('input');
          newTelephoneInput.type = 'text';
          newTelephoneInput.name = 'additional_telephones';
          newTelephoneInput.placeholder = '(XX) XXXXX-XXXX';
          newTelephoneInput.className = 'form-control';
    
          const removeButton = document.createElement('button');
          removeButton.className = 'btn btn-danger';
          removeButton.innerHTML = 'X'; // Texto do botão
          removeButton.onclick = function() {
              telephoneFieldsDiv.removeChild(newTelephoneInputGroup); // Remove o campo ao clicar
          };
    
          newTelephoneInputGroup.appendChild(newTelephoneInput);
          newTelephoneInputGroup.appendChild(removeButton); // Adiciona o botão de remoção
          telephoneFieldsDiv.appendChild(newTelephoneInputGroup);
      }
