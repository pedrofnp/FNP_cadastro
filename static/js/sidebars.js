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