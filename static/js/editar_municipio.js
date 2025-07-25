// static/js/editar_municipio.js

$(document).ready(function () {
  $('#municipio_id').select2({
    placeholder: "Selecione um município",
    width: 'resolve',
    language: {
      noResults: function () {
        return "Nenhum município encontrado";
      }
    }
  });
});
