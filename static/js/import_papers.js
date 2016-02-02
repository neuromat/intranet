$(document).ready(function(){ 
    $("#selectall").change(function(){
      $(".checkbox1").prop('checked', $(this).prop("checked"));
      });
});