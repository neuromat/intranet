$(document).ready(function () {
    if (!id_category_0.checked && !id_category_1.checked){
        $("#id_university").parents('.row').hide();
        $("#id_institute").parents('.row').hide();
        $("#id_department").parents('.row').hide();
    }
    $("#id_category_0").click(function () {
        $("#id_university").parents('.row').show();
        $("#id_institute").parents('.row').show();
        $("#id_department").parents('.row').show();
    });
    $("#id_category_1").click(function () {
        $("#id_university").parents('.row').hide();
        $("#id_institute").parents('.row').hide();
        $("#id_department").parents('.row').hide();
    });
    if (id_category_1.checked){
        $("#id_university").parents('.row').hide();
        $("#id_institute").parents('.row').hide();
        $("#id_department").parents('.row').hide();
    }
});

function ajax_filter_institutes(university_id)
{
   $("#id_institute").html('<option value="">Loading...</option>');
   $.ajax({
       type: "GET",
       url: "/order/show_institute",
       dataType: "json",
       data: {'university':university_id},
       success: function(retorno) {
           $("#id_institute").empty();
           $("#id_institute").append('<option value="">--------</option>');
           $.each(retorno, function(i, item){
               $("#id_institute").append('<option value="'+item.pk+'">'+item.valor+'</option>');
           });
       },
       error: function(error) {
           alert('Error: No request return.');
       }
   });
}

function ajax_filter_departments(institute_id)
{
   $("#id_department").html('<option value="">Loading...</option>');
   $.ajax({
       type: "GET",
       url: "/order/show_department",
       dataType: "json",
       data: {'institute':institute_id},
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