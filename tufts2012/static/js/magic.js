var pLine; /* The current polyline on the map. This could have an empty path */
var polygonArray = Array(); /* The array of all the polygon objects */
var polygonMode; /* True if you are currently drawing a polygon */
var polygonListen = false; /* True if polygon mode is active */
var polyMarker; /* The first marker for the polygon */
var infowin;    /* The one infowindow allowed on the map */
var map; /* The map object */
var polyResults = false; /* True if results are being displayed */
var plineOptions = {strokeColor:"#0B0B61",strokeOpacity:0.7};
var pgonOptions = $.extend(plineOptions,{fillColor:"#0B0B61",fillOpacity:0.4});

function initialize() {
    polygonMode = false;
    infowin = new google.maps.InfoWindow();
    var mapOptions = {
        center: new google.maps.LatLng(42.406, -71.119),
        zoom: 3,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("gmap"),
            mapOptions);
    pline = new google.maps.Polyline(plineOptions);
    pline.setMap(map);
    polyMarker = new google.maps.Marker({ map:map,
        title: "", icon: "static/img/pin.gif"});
    google.maps.event.addDomListener(window, 'resize', resizeGmap);
    return map;
}

function placeMarker(lat, lon, name, place, map) {
    var latlng = new google.maps.LatLng(lat, lon);
    var marker = new google.maps.Marker({position: latlng,
                                         map:map,
                                         title: name+ " - " + place});
    marker.setMap(map);
    google.maps.event.addListener(marker, 'click', function(r) {
        infowin.content = name + " - " + place;
        infowin.open(map, marker);
    });
}

function polygonButtonListeners() {
    $('#polygon-on').click(polygonModeToggle);
    $('#polygon-clear').click(polygonModeOff);
}

function polygonModeToggle() {
    if (polygonListen) {
        $('#polygon-on').removeClass('depressed');
        polygonListen = false;
    } else {
        $("#polygon-on").addClass('depressed');
        polygonListen = true;
    }
}

function searchLocationListener(url) {
    $('#search-loc-form').submit(function(e) {
        var params="?location="+$("#search-location").val();
        e.preventDefault();
        $.getJSON(url+params, $('#search-loc-form').serialize(),
            function(data) {
                var latlng = new google.maps.LatLng(data['lat'], data['lon']);
                map.panTo(latlng);
                map.setZoom(8);
            });
        return false;
    });
}

function polygonModeOff() {
        pline.setPath([]);
        polyMarker.setMap(null);
        polyResults = false;
        resizeGmap();
        polygonMode = false;
        destroySlimscroll();
        for(var i=0; i<polygonArray.length; i++)
            polygonArray[i].setMap(null);
        $('#polygon-results').empty();
        $('#polygon-clear').removeClass('depressed');
        polygonModeToggle();
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
    var res = $('#polygon-results');
    if (!$('#poly-'+person['id'], res).get(0)) {
        res.append("<li id='poly-"+person['id']+"'>"+
                "<span class='bold'>"+person['name']+"</span> - "+person['loc']);
    }
}

function polygonListeners(get_url, map) {
    google.maps.event.addListener(map, 'click', function(e) {
        if (polygonListen == false)
            return 
        if ($('#polygon-clear').hasClass('depressed'))
            $('#polygon-clear').addClass('depressed');
        var path = pline.getPath();
        path.push(e.latLng);
        if(!polygonMode) {
            polyMarker.setPosition(e.latLng);
            polyMarker.setMap(map);
            polygonMode = true;
            google.maps.event.addListener(polyMarker, 'click', function(ev) {
                if(pline.getPath()['b'].length > 2) {
                    var paths = pline.getPath();
                    var pgon = new google.maps.Polygon(
                        $.extend({paths: paths}, pgonOptions));
                    pline.setPath([]);
                    pgon.setMap(map);
                    polygonArray.push(pgon);
                    polyMarker.setMap(null);
                    polygonMode = false;
                    var params = ""
                    $.each(paths['b'], function (i, v) {
                        params += v.lat() + "," + v.lng() + ",,";
                    });
                    params = params.substring(0, params.length-2) + '/';
                    $.getJSON(get_url+params, {}, function(data) {
                        $.each(data, function(i, person) {
                            if (i==0) {
                                polyResults = true;
                                resizeGmap();
                            }
                            addPolygonMember(person);
                            slimScrollSetup();
                        });
                    });
                }
            });
        }
    });
}
function destroySlimscroll() {
    $(".slimScrollDiv").replaceWith($("#polygon-results"));
    $("#polygon-results").css("height","auto");
}
function slimScrollSetup() {
    $("#polygon-results").slimScroll({height:"350px",alwaysVisible: true});
}

function resizeGmap() {
    /* Checks if the results div exists, and resizes the map if it does. 
     * Triggered when polyResults are found or the window is resized.
     */
    var resW = 220;
    if (!polyResults) resW=0;
    var wrapW = $("#wrapper").width();
    $("#gmap").css("width",wrapW - resW);
    google.maps.event.trigger(map, 'resize');
}

function autocompleteInit(get_url, map) {
    $('#search-box').autocomplete({
        source: get_url,
        minLength: 3,
        focus: function(e, v) {
            $('#search-box').val(v.item.label);
            return false;
        },
        select: function(e,i) {
            var latlng = new google.maps.LatLng(i.item.lat, i.item.lon);
            map.panTo(latlng);
            map.setZoom(5);
            infowin.close();
            infowin.content = i.item['label'] + " - " + i.item['name'];
            infowin.setPosition(latlng);
            infowin.open(map);
            return false;
        }
    });
}
