// JS da página filters.html


$(document).ready(function () {
  $('select[name="cargo"]').select2({ width: 'resolve', placeholder: "Cargo" });
  $('select[name="estado"]').select2({ width: 'resolve', placeholder: "Estado" });
  $('select[name="municipio"]').select2({ width: 'resolve', placeholder: "Município" });
  $('select[name="regiao"]').select2({ width: 'resolve', placeholder: "Região" });
  $('select[name="capital"]').select2({ width: 'resolve', placeholder: "Capital" });
  $('select[name="tipo_municipio"]').select2({ width: 'resolve', placeholder: "Tipo de Município" });
  $('select[name="regiao_metropolitana"]').select2({ width: 'resolve', placeholder: "Região Metropolitana" });
});
