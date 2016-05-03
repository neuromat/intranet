function load_origin_cities(id_origin_country)
{
    var $id_origin_city = $('#id_origin_city');

    $id_origin_city.html('<option value="">Loading...</option>');
    $.ajax({
       type: "GET",
       url: "/scientific_mission/load_origin_cities",
       dataType: "json",
       data: {'origin_country':id_origin_country},
       success: function(result) {
           $id_origin_city.empty();
           $id_origin_city.append('<option value="">--------</option>');

           $.each(result, function(i, item){
               $id_origin_city.append('<option value="'+item.pk+'">'+item.name+'</option>');
           });
       },
       error: function() {
           alert('Error: No request return.');
       }
    });
}


function load_destination_cities(id_destination_country)
{
    var $id_destination_city = $('#id_destination_city');

    $id_destination_city.html('<option value="">Loading...</option>');
    $.ajax({
       type: "GET",
       url: "/scientific_mission/load_destination_cities",
       dataType: "json",
       data: {'destination_country':id_destination_country},
       success: function(result) {
           $id_destination_city.empty();
           $id_destination_city.append('<option value="">--------</option>');

           $.each(result, function(i, item){
               $id_destination_city.append('<option value="'+item.pk+'">'+item.name+'</option>');
           });
       },
       error: function() {
           alert('Error: No request return.');
       }
    });
}
