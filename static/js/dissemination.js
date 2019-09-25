$(document).ready(function () {

    // ### Hide internal class field ###
    $("#id_class_internal_field").hide();

    // ### Type field ###
    let $id_type = $('#id_type');

    // ### Hide or show internal class field ###
    $id_type.each(function() {
        if($(this).val() == 'i'){
           $("#id_class_internal_field").show();
       } else {
           $("#id_class_internal_field").hide();
       }
    });

    $id_type.on('change', (function () {
       if($(this).val() == 'i'){
           $("#id_class_internal_field").show();
       } else {
           $("#id_class_internal_field").hide();
       }
    }));

    $('.report-date-mask').mask("99/99/9999");
});

