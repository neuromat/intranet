$(document).ready(function(){ 
    $("#select_all_periodicals").change(function(){
      $(".checkbox_periodicals").prop('checked', $(this).prop("checked"));
    });
});