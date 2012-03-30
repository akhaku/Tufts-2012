function initialize() {
    var myOptions = {
        center: new google.maps.LatLng(42.406, -71.119),
        zoom: 3,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("gmap"),
            myOptions);
    return map;
}

function placeMarker(lat, lon, name, place, map) {
    var latlng = new google.maps.LatLng(lat, lon);
    var marker = new google.maps.Marker({position: latlng,
                                         map:map,
                                         title: name+ " - " + place});
    marker.setMap(map);
}
