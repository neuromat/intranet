$(document).ready(function () {

    var $status = $('#id_status');
    var $id_type = $('#id_type');
    var $periodical = $('#id_periodical');
    var $event = $('#id_event');
    var $published = $('#id_status_3');
    var $accepted = $('#id_status_2');
    var $submitted = $('#id_status_1');
    var $draft = $('#id_status_0');


    // ### Hide/show "Where will be published?" field ###
    if ($accepted.checked || $published.checked){
        $id_type.parents('.row').show();
    } else {
        $id_type.parents('.row').hide();
    }

    $status.click(function(){
       if ($accepted.is(':checked') || $published.is(':checked')) {
          $id_type.parents('.row').show();
       } else {
          $id_type.parents('.row').hide();
       }
    });


    // ### Hide/show event/periodical fields ###
    $id_type.each(function() {
        if($(this).val() == 'p' && ($published.is(':checked') || $accepted.is(':checked'))){
            $periodical.parents('.row').show();
        } else if($(this).val() == 'e' && ($published.is(':checked') || $accepted.is(':checked'))){
            $event.parents('.row').show();
        } else{
            $periodical.parents('.row').hide();
            $event.parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'p' && ($published.is(':checked') || $accepted.is(':checked'))){
            $periodical.parents('.row').show();
            $event.parents('.row').hide();
        } else if($(this).val() == 'e' && ($published.is(':checked') || $accepted.is(':checked'))){
            $periodical.parents('.row').hide();
            $event.parents('.row').show();
        } else{
            $periodical.parents('.row').hide();
            $event.parents('.row').hide();
        }
    });


    // ### Hide/show draft inline ###
    if ($draft.checked){
        $('[id^="draft"]').parents('._inline-group').show();
    } else {
        $('[id^="draft"]').parents('._inline-group').hide();
    }

    $status.click(function(){
       if ($draft.is(':checked')) {
          $('[id^="draft"]').parents('._inline-group').show();
       } else {
          $('[id^="draft"]').parents('._inline-group').hide();
       }
    });


    // ### Hide/show submitted inline ###
    if ($submitted.checked){
        $('[id^="submitted"]').parents('._inline-group').show();
    } else {
        $('[id^="submitted"]').parents('._inline-group').hide();
    }

    $status.click(function(){
       if ($submitted.is(':checked')) {
          $('[id^="submitted"]').parents('._inline-group').show();
       } else {
          $('[id^="submitted"]').parents('._inline-group').hide();
       }
    });


    // ### Hide/show accepted inline ###
    if ($accepted.checked){
        $('[id^="accepted"]').parents('._inline-group').show();
    } else {
        $('[id^="accepted"]').parents('._inline-group').hide();
    }

    $status.click(function(){
       if ($accepted.is(':checked')) {
          $('[id^="accepted"]').parents('._inline-group').show();
       } else {
          $('[id^="accepted"]').parents('._inline-group').hide();
       }
    });


    // ### Hide/show published in periodical inline ###
    $periodical.each(function() {
        if($(this).length && ($id_type.val() == 'p' && $published.is(':checked'))){
            $('[id^="publishedinperiodical"]').parents('._inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
        }
    });

    $periodical.change(function(){
        if($(this).val() != ''  && ($id_type.val() == 'p' && $published.is(':checked'))){
            $('[id^="publishedinperiodical"]').parents('._inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
        }
    });


    // ### Hide/show published inline ###
    $event.each(function() {
        if($(this).length && ($id_type.val() == 'e' && $published.is(':checked'))){
            $('[id^="published-"]').parents('._inline-group').show();
        } else{
            $('[id^="published-"]').parents('._inline-group').hide();
        }
    });

    $event.change(function(){
        if($(this).val() != ''  && ($id_type.val() == 'e' && $published.is(':checked'))){
            $('[id^="published-"]').parents('._inline-group').show();
        } else{
            $('[id^="published-"]').parents('._inline-group').hide();
        }
    });


    // ### Hide/show published or published in periodical inline ###
    $id_type.change(function(){
        if($(this).val() == 'p' && $periodical.val() != '' && $published.is(':checked')){
            $('[id^="publishedinperiodical"]').parents('._inline-group').show();
        } else if($(this).val() == 'e' && $event.val() != '' && $published.is(':checked')){
            $('[id^="published-"]').parents('._inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="published-"]').parents('._inline-group').hide();
        }
    });

    $status.click(function(){
       if ($published.is(':checked') && ($id_type.val() == 'p' && $periodical.val() != '')) {
           $('[id^="publishedinperiodical"]').parents('._inline-group').show();
           $periodical.parents('.row').show();
       } else if($accepted.is(':checked') && ($id_type.val() == 'p' && $periodical.val() != '')){
           $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
           $periodical.parents('.row').show();
       } else if($published.is(':checked') && $id_type.val() == 'p'){
           $periodical.parents('.row').show();
       } else {
           $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
           $periodical.parents('.row').hide();
       }
    });

    $status.click(function(){
       if ($published.is(':checked') && $id_type.val() == 'e' && $event.val() != '') {
           $('[id^="published-"]').parents('._inline-group').show();
           $event.parents('.row').show();
       } else if($accepted.is(':checked') && ($id_type.val() == 'e' && $event.val() != '')){
           $('[id^="published-"]').parents('._inline-group').hide();
           $event.parents('.row').show();
       } else if($published.is(':checked') && $id_type.val() == 'e'){
           $event.parents('.row').show();
       } else {
           $('[id^="published-"]').parents('._inline-group').hide();
           $event.parents('.row').hide();
       }
    });

});