$(document).ready(function() {

    $('.datepicker').attr('autocomplete', 'off');

    $('.datepicker').datepicker({
      changeMonth: true,
      changeYear: true,
      autoSize: true,
      dateFormat: "dd/mm/yy"
    });
});