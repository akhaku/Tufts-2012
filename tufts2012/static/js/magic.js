var pLine;
var polygonMode;
var plineOptions = {strokeColor:"#0B0B61",strokeOpacity:0.7};
var pgonOptions = $.extend(plineOptions,{fillColor:"#0B0B61",fillOpacity:0.4});

function initialize() {
    polygonMode = false;
    var mapOptions = {
        center: new google.maps.LatLng(42.406, -71.119),
        zoom: 3,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("gmap"),
            mapOptions);
    pline = new google.maps.Polyline(plineOptions);
    pline.setMap(map);
    return map;
}

function placeMarker(lat, lon, name, place, map) {
    var latlng = new google.maps.LatLng(lat, lon);
    var marker = new google.maps.Marker({position: latlng,
                                         map:map,
                                         title: name+ " - " + place});
    marker.setMap(map);
}

function locationFormListeners(post_url, map) {
    $('#location-form').submit(function(e) {
        e.preventDefault();
        $.post(post_url, $('form#location-form').serialize(),
            function(data) {
                $('#add-location-div').html(data);
                var lat = $('#added-lat',data).html();
                var lon = $('#added-lon',data).html();
                var name = $('#added-name',data).html();
                var loc = $('#added-loc',data).html();
                placeMarker(lat, lon, name, loc, map);
                $("#added-div").remove();
                locationFormListeners(post_url, map);
            });
    });
}

function addPolygonMember(person) {
    var res = $('#polygon-results-div');
    if ($('#poly-'+person['id'], res).get(0)) {
        res.append("<li id=poly'"+person['id']+"'>"+
                person['name']+" - "+person['loc']);
    }
}

function polygonListeners(get_url, map) {
    google.maps.event.addListener(map, 'click', function(e) {
        var path = pline.getPath();
        path.push(e.latLng);
        if(!polygonMode) {
            var marker = new google.maps.Marker({position: e.latLng,
                map:map, title: "", icon: "static/img/pin.gif"});
            marker.setMap(map);
            polygonMode = true;
            google.maps.event.addListener(marker, 'click', function(ev) {
                if(pline.getPath()['b'].length > 2) {
                    var paths = pline.getPath();
                    var pgon = new google.maps.Polygon(
                        $.extend({paths: paths}, pgonOptions));
                    pgon.setMap(map);
                    polygonMode = false;
                    pline = new google.maps.Polyline(plineOptions);
                    pline.setMap(map);
                    var params = ""
                    $.each(paths['b'], function (i, v) {
                        params += v.lat() + "," + v.lng() + ",,";
                    });
                    params = params.substring(0, params.length-2) + '/';
                    $.getJSON(get_url+params, {}, function(data) {
                        $.each(data, function(i, person) {
                            addPolygonMember(person);
                        });
                    });
                }
            });
        }
    });
}
