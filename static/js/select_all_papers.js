$(document).ready(function(){
    $("#select_all_papers").change(function(){
      $(".checkbox_ris_paper").prop('checked', $(this).prop("checked"));
    });
});