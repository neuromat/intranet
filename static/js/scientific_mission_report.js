$(document).ready(function () {

    let ua = navigator.userAgent.toLowerCase();
    let isNotAndroid = ua.indexOf("android") <= -1; //&& ua.indexOf("mobile");

    if (isNotAndroid) {
        $("#id_start_date").mask("99/99/9999");
        $("#id_end_date").mask("99/99/9999");
    }

    $('.report-date-mask').mask("99/99/9999");


});