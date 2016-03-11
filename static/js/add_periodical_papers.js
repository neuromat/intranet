$(document).ready(function(){
    $("#select_all_periodical_papers").change(function(){
      $(".checkbox_periodical_papers").prop('checked', $(this).prop("checked"));
    });
});