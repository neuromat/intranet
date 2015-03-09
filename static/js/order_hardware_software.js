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