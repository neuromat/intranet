$(document).ready(function () {

    var $status = $('#id_status');
    var $id_type = $('#id_type');
    var $periodical = $('#id_periodical');
    var $event = $('#id_event');
    var $published = $('#id_status_3');
    var $accepted = $('#id_status_2');
    var $submitted = $('#id_status_1');
    var $draft = $('#id_status_0');

    //This file should looking for control-group class if django-suit is used.
    if ($(".control-group")[0]){
        var $class = ('.control-group');
    } else {
        var $class = ('.form-row');
    }


    // ### Hide/show "Where will be published?" field ###
    if ($accepted.is(':checked') || $published.is(':checked')){
        $id_type.parents($class).show();
    } else {
        $id_type.parents($class).hide();
    }

    $status.click(function(){
       if ($accepted.is(':checked') || $published.is(':checked')) {
          $id_type.parents($class).show();
       } else {
          $id_type.parents($class).hide();
       }
    });


    // ### Hide/show event/periodical fields ###
    $id_type.each(function() {
        if($(this).val() == 'p' && ($published.is(':checked') || $accepted.is(':checked'))){
            $periodical.parents($class).show();
        } else if($(this).val() == 'e' && ($published.is(':checked') || $accepted.is(':checked'))){
            $event.parents($class).show();
        } else{
            $periodical.parents($class).hide();
            $event.parents($class).hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'p' && ($published.is(':checked') || $accepted.is(':checked'))){
            $periodical.parents($class).show();
            $event.prop('selectedIndex',0);
            $event.parents($class).hide();
        } else if($(this).val() == 'e' && ($published.is(':checked') || $accepted.is(':checked'))){
            $periodical.prop('selectedIndex',0);
            $periodical.parents($class).hide();
            $event.parents($class).show();
        } else{
            $periodical.parents($class).hide();
            $event.parents($class).hide();
        }
    });


    // ### Hide/show draft inline ###
    if ($draft.is(':checked')) {
        $('[id^="draft"]').parents('.inline-group').show();
    } else {
        $('[id^="draft"]').parents('.inline-group').hide();
    }

    $status.click(function(){
       if ($draft.is(':checked')) {
          $('[id^="draft"]').parents('.inline-group').show();
       } else {
          $('[id^="draft"]').parents('.inline-group').hide();
       }
    });


    // ### Hide/show submitted inline ###
    if ($submitted.is(':checked')) {
        $('[id^="submitted"]').parents('.inline-group').show();
    } else {
        $('[id^="submitted"]').parents('.inline-group').hide();
    }

    $status.click(function(){
       if ($submitted.is(':checked')) {
          $('[id^="submitted"]').parents('.inline-group').show();
       } else {
          $('[id^="submitted"]').parents('.inline-group').hide();
       }
    });


    // ### Hide/show accepted inline ###
    if ($accepted.is(':checked')) {
        $('[id^="accepted"]').parents('.inline-group').show();
    } else {
        $('[id^="accepted"]').parents('.inline-group').hide();
    }

    $status.click(function(){
       if ($accepted.is(':checked')) {
          $('[id^="accepted"]').parents('.inline-group').show();
       } else {
          $('[id^="accepted"]').parents('.inline-group').hide();
       }
    });


    // ### Hide/show published in periodical inline ###
    $periodical.each(function() {
        if($(this).length && ($id_type.val() == 'p' && $published.is(':checked'))){
            $('[id^="publishedinperiodical"]').parents('.inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('.inline-group').hide();
        }
    });

    $periodical.change(function(){
        if($(this).val() != ''  && ($id_type.val() == 'p' && $published.is(':checked'))){
            $('[id^="publishedinperiodical"]').parents('.inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('.inline-group').hide();
        }
    });


    // ### Hide/show published inline ###
    $event.each(function() {
        if($(this).val() != '' && ($id_type.val() == 'e' && $published.is(':checked'))){
            $('[id^="published-"]').parents('.inline-group').show();
        } else{
            $('[id^="published-"]').parents('.inline-group').hide();
        }
    });

    $event.change(function(){
        if($(this).val() != ''  && ($id_type.val() == 'e' && $published.is(':checked'))){
            $('[id^="published-"]').parents('.inline-group').show();
        } else{
            $('[id^="published-"]').parents('.inline-group').hide();
        }
    });


    // ### Hide/show published or published in periodical inline ###
    $id_type.change(function(){
        if($(this).val() == 'p' && $periodical.val() != '' && $published.is(':checked')){
            $('[id^="publishedinperiodical"]').parents('.inline-group').show();
        } else if($(this).val() == 'e' && $event.val() != '' && $published.is(':checked')){
            $('[id^="published-"]').parents('.inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('.inline-group').hide();
            $('[id^="published-"]').parents('.inline-group').hide();
        }
    });


    // ### Hide/show some fields according to the status ###
    $status.click(function(){
       if ($published.is(':checked') && ($id_type.val() == 'p' && $periodical.val() != '')) {
           $('[id^="publishedinperiodical"]').parents('.inline-group').show();
           $periodical.parents($class).show();
       } else if($accepted.is(':checked') && ($id_type.val() == 'p' && $periodical.val() != '')){
           $('[id^="publishedinperiodical"]').parents('.inline-group').hide();
           $periodical.parents($class).show();
       } else if($published.is(':checked') && $id_type.val() == 'p'){
           $periodical.parents($class).show();
       } else {
           $('[id^="publishedinperiodical"]').parents('.inline-group').hide();
           $periodical.parents($class).hide();
       }
    });

    $status.click(function(){
       if ($published.is(':checked') && $id_type.val() == 'e' && $event.val() != '') {
           $('[id^="published-"]').parents('.inline-group').show();
           $event.parents($class).show();
       } else if($accepted.is(':checked') && ($id_type.val() == 'e' && $event.val() != '')){
           $('[id^="published-"]').parents('.inline-group').hide();
           $event.parents($class).show();
       } else if($published.is(':checked') && $id_type.val() == 'e'){
           $event.parents($class).show();
       } else {
           $('[id^="published-"]').parents('.inline-group').hide();
           $event.parents($class).hide();
       }
    });


    // ### Hide/show some fields in accordance with the values entered ###
    if ($accepted.is(':checked') && $id_type.val() == 'p') {
        $('[id^="accepted"]').parents('.inline-group').show();
        $periodical.parents($class).show();
        $id_type.parents($class).show();
        $event.parents($class).hide();
    } else if ($accepted.is(':checked') && $id_type.val() == 'e') {
        $('[id^="accepted"]').parents('.inline-group').show();
        $periodical.parents($class).hide();
        $id_type.parents($class).show();
        $event.parents($class).show();
    }

    if ($published.is(':checked') && $id_type.val() == 'e' && $event.val() != '') {
        $('[id^="published-"]').parents('.inline-group').show();
        $periodical.parents($class).hide();
        $id_type.parents($class).show();
        $event.parents($class).show();
    } else if ($published.is(':checked') && $id_type.val() == 'e' && $event.val() == '') {
        $('[id^="published-"]').parents('.inline-group').hide();
        $periodical.parents($class).hide();
        $id_type.parents($class).show();
        $event.parents($class).show();
    }

    if ($published.is(':checked') && $id_type.val() == 'p' && $periodical.val() != '') {
        $('[id^="publishedinperiodical"]').parents('.inline-group').show();
        $periodical.parents($class).show();
        $id_type.parents($class).show();
        $event.parents($class).hide();
    } else if ($published.is(':checked') && $id_type.val() == 'p' && $periodical.val() == '') {
        $('[id^="publishedinperiodical"]').parents('.inline-group').hide();
        $periodical.parents($class).show();
        $id_type.parents($class).show();
        $event.parents($class).hide();
    }

});