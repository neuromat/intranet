function ajax_filter_institutes(university_id)
{
   $("#id_institute").html('<option value="">Loading...</option>');
   $.ajax({
       type: "GET",
       url: "/member/show_institute",
       dataType: "json",
       data: {'university':university_id},
       success: function(retorno) {
           $("#id_institute").empty();
           $("#id_institute").append('<option value="">--------</option>');
           $.each(retorno, function(i, item){
               $("#id_institute").append('<option value="'+item.pk+'">'+item.valor+'</option>');
           });
       },
       error: function(erro) {
           alert('Erro: Sem retorno de requisição.');
       }
   });
}