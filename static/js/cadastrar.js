// JS para cadastrar.html

$(document).ready(function () {
  $('select[name="estado"]').select2({
    placeholder: "Selecione um estado",
    width: 'resolve',
    language: {
      noResults: function () {
        return "Nenhum estado encontrado";
      }
    }
  });

  $('select[name="municipio"]').select2({
    placeholder: "Selecione um município",
    width: 'resolve',
    language: {
      noResults: function () {
        return "Nenhum município encontrado";
      }
    }
  });
});
