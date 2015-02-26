$(document).ready(function () {
    $("#id_type_1").click(function () {
        $("#id_inbound_date").parents('.row').hide();
        $("#id_inbound_date_preference").parents('.row').hide();
    });
    $("#id_type_0").click(function () {
        $("#id_inbound_date").parents('.row').show();
        $("#id_inbound_date_preference").parents('.row').show();
    });
    if (id_type_1.checked){
        $("#id_inbound_date").parents('.row').hide();
        $("#id_inbound_date_preference").parents('.row').hide();
    }
});

function ajax_select_categories(id_order_type)
{
   $("#id_category").html('<option value="">Carregando...</option>');
   $.ajax({
       type: "GET",
       url: "/order/categories",
       dataType: "json",
       data: {'order_type':id_order_type},
       success: function(retorno) {
           $("#id_category").empty();
           $("#id_category").append('<option value="">--------</option>');
           $.each(retorno, function(i, item){
               $("#id_category").append('<option value="'+ item.value+'">'+item.display+'</option>');
           });
           if (retorno.length == 0){
            $("#id_category").hide();
           }else{
            $("#id_category").show();
           }

       },
       error: function(erro) {
           alert('Erro: Sem retorno de requisição.');
       }
   });
}