function ajax_select_mission(id_person)
{
   $("#id_title").html('<option value="">Loading...</option>');
   $.ajax({
       type: "GET",
       url: "/scientific_mission/show_missions",
       dataType: "json",
       data: {'person':id_person},
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
