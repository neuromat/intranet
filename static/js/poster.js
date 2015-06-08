function ajax_select_seminar(id_speaker)
{
   $("#id_title").html('<option value="">Loading...</option>');
   $.ajax({
       type: "GET",
       url: "/activity/seminar_show_titles",
       dataType: "json",
       data: {'speaker':id_speaker},
       success: function(retorno) {
           $("#id_title").empty();
           $("#id_title").append('<option value="">--------</option>');

           $.each(retorno, function(i, item){
               $("#id_title").append('<option value="'+item.pk+'">'+item.valor+'</option>');
           });
       },
       error: function(erro) {
           alert('Error: No request return.');
       }
   });
}
