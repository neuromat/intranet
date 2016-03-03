$(document).ready(function(){
    $("#select_all_event_papers").change(function(){
      $(".checkbox_event_papers").prop('checked', $(this).prop("checked"));
    });
});
