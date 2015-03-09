$(document).ready(function () {
    if (!id_category_0.checked && !id_category_1.checked){
        $("#id_institution").parents('.row').hide();
        $("#id_department").parents('.row').hide();
    }

    $("#id_category_0").click(function () {
        $("#id_institution").parents('.row').show();
        $("#id_department").parents('.row').show();
    });
    $("#id_category_1").click(function () {
        $("#id_institution").parents('.row').hide();
        $("#id_department").parents('.row').hide();
    });

    $("#id_type_1").click(function () {
        $("#id_inbound_date").parents('.row').hide();
        $("#id_inbound_date_preference").parents('.row').hide();
    });
    $("#id_type_0").click(function () {
        $("#id_inbound_date").parents('.row').show();
        $("#id_inbound_date_preference").parents('.row').show();
    });

    if (id_category_1.checked){
        $("#id_institution").parents('.row').hide();
        $("#id_department").parents('.row').hide();
    }

    if (id_type_1.checked){
        $("#id_inbound_date").parents('.row').hide();
        $("#id_inbound_date_preference").parents('.row').hide();
    }
});

function ajax_filter_departments(institution_id)
{
   $("#id_department").html('<option value="">Loading...</option>');
   $.ajax({
       type: "GET",
       url: "/order/show_department",
       dataType: "json",
       data: {'institution':institution_id},
       success: function(retorno) {
           $("#id_department").empty();
           $("#id_department").append('<option value="">--------</option>');
           $.each(retorno, function(i, item){
               $("#id_department").append('<option value="'+item.pk+'">'+item.valor+'</option>');
           });
       },
       error: function(error) {
           alert('Error: No request return.');
       }
   });
}

function ajax_select_additional_options(id_order_type)
{
   $("#id_status").html('<option value="">Carregando...</option>');
   $("#id_category").html('<option value="">Carregando...</option>');
   $("#id_origin").html('<option value="">Carregando...</option>');
   $.ajax({
       type: "GET",
       url: "/order/additional_options",
       dataType: "json",
       data: {'order_type':id_order_type},
       success: function(retorno) {
           $("#id_status").empty();
           $("#id_category").empty();
           $("#id_origin").empty();
           $("#id_status").append('<option value="">--------</option>');
           $("#id_category").append('<option value="">--------</option>');
           $("#id_origin").append('<option value="">--------</option>');

           $.each(retorno[0], function(i, item){
               $("#id_status").append('<option value="'+ item.value+'">'+item.display+'</option>');
           });

           $.each(retorno[1], function(i, item){
               $("#id_category").append('<option value="'+ item.value+'">'+item.display+'</option>');
           });
           if ($("#id_order_type").val() == 'h') {
               $("#id_category").prop( "disabled", false );
           } else{
               $("#id_category").prop( "disabled", true );
           }

           $.each(retorno[2], function(i, item){
               $("#id_origin").append('<option value="'+ item.value+'">'+item.display+'</option>');
           });
           if ($("#id_order_type").val() == 'h' || $("#id_order_type").val() == 's') {
               $("#id_origin").prop( "disabled", false );
           } else{
               $("#id_origin").prop( "disabled", true );
           }

       },
       error: function(erro) {
           alert('Erro: Sem retorno de requisição.');
       }
   });
}

