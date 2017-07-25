proj4.defs("EPSG:31370", "+proj=lcc +lat_1=51.16666723333333 +lat_2=49.8333339 +lat_0=90 +lon_0=4.367486666666666 +x_0=150000.013 +y_0=5400088.438 +ellps=intl +towgs84=-106.869,52.2978,-103.724,0.3366,-0.457,1.8422,-1.2747 +units=m +no_defs");

var layers = [];
var outputs = [];

// Add the routes as layers.
$.each(routes, function (key, value) {
    $("#layers").append('<option value="' + key + '">' + value + '</option>');
});

// Make correct layer visible when changing route select.
$("#layers").change(function () {
    var i;

    if (this.value === "all") {
        for (i = 0; i < outputs.length; i++) {
            layers[i].setVisible(false);
            outputs[i].setVisible(true);
        }
    } else {
        for (i = 0; i < outputs.length; i++) {
            layers[i].setVisible(false);

            if (i === parseInt(this.value)) {
                outputs[i].setVisible(true);
            } else {
                outputs[i].setVisible(false);
            }
        }
    }

    $("#bm").prop("checked", false);
    $("#out").prop("checked", true);
    overlay.setPosition(undefined);
    closer.blur();
    select.getFeatures().clear();
});

// Make correct layer visible when changing type checkbox.
$(".type-checkbox").change(function () {
    var i;
    var kind = $(this).attr("value");
    var layer = $("#layers").val();

    if (layer === "all") {
        if (kind === "route") {
            for (i = 0; i < outputs.length; i++) {
                layers[i].setVisible($(this).is(":checked"));
            }
        } else if (kind === "output") {
            for (i = 0; i < outputs.length; i++) {
                outputs[i].setVisible($(this).is(":checked"));
            }
        }
    } else {
        var index = parseInt(layer);
        if (kind === "route") {
            layers[index].setVisible($(this).is(":checked"))
        } else if (kind === "output") {
            outputs[index].setVisible($(this).is(":checked"))
        }
    }

    overlay.setPosition(undefined);
    closer.blur();
    select.getFeatures().clear();
});

/**
 * Elements that make up the popup.
 */
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');

/**
 * Create an overlay to anchor the popup to the map.
 */
var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
    element: container,
    autoPan: true,
    autoPanAnimation: {
        duration: 250
    }
}));

/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
closer.onclick = function () {
    overlay.setPosition(undefined);
    closer.blur();
    select.getFeatures().clear();
    return false;
};

// OpenStreetMap base layers.
var baselayers = {
    "opencycle": new ol.layer.Tile({
        source: new ol.source.XYZ({
            url: "https://{a-c}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey=05cd428b293d4da1a7d2db69d11bc83e",
            attributions: [ol.source.OSM.ATTRIBUTION, "Maps &copy; <a href=\"http://www.thunderforest.com/\">Thunderforest</a>"]
        })
    }),
    "osmbe": new ol.layer.Tile({
        source: new ol.source.OSM({
            url: "https://tile.osm.be/osmbe/{z}/{x}/{y}.png",
            attributions: [ol.source.OSM.ATTRIBUTION, "Tiles courtesy of <a href=\"https://geo6.be/\">GEO-6</a>"]
        })
    }),
    "osmbe-fr": new ol.layer.Tile({
        source: new ol.source.OSM({
            url: "https://tile.osm.be/osmbe-fr/{z}/{x}/{y}.png",
            attributions: [ol.source.OSM.ATTRIBUTION, "Tiles courtesy of <a href=\"https://geo6.be/\">GEO-6</a>"]
        })
    }),
    "osmbe-nl": new ol.layer.Tile({
        source: new ol.source.OSM({
            url: "https://tile.osm.be/osmbe-nl/{z}/{x}/{y}.png",
            attributions: [ol.source.OSM.ATTRIBUTION, "Tiles courtesy of <a href=\"https://geo6.be/\">GEO-6</a>"]
        })
    }),
    "osmbe-de": new ol.layer.Tile({
        source: new ol.source.OSM({
            url: "https://tile.osm.be/osmbe-de/{z}/{x}/{y}.png",
            attributions: [ol.source.OSM.ATTRIBUTION, "Tiles courtesy of <a href=\"https://geo6.be/\">GEO-6</a>"]
        })
    })
};

var attribution = new ol.control.Attribution({
    collapsible: false
});

var map = new ol.Map({
    layers: [
        baselayers[$("#baselayers").val()]
    ],
    overlays: [overlay],
    controls: ol.control.defaults({attribution: false}).extend([attribution]),
    target: "map",
    view: new ol.View({
        center: ol.proj.transform([4.36657, 50.84072], "EPSG:4326", "EPSG:3857"),
        zoom: 12
    })
});

/**
 * Returns a list of sorted keys in an object.
 *
 * @param obj Object to get keys from.
 * @returns {Array.<*>} Sorted array of keys.
 */
var keysSorted = function (obj) {
    var keys = [];

    for (var key in obj) {
        if (obj.hasOwnProperty(key)) {
            keys.push(key);
        }
    }

    return keys.sort();
};

var downloadRoute = function (routenumber)
{
    var xmlHttp = new XMLHttpRequest();

    var url = "http://localhost:8111/import?url=http://api.openstreetmap.org/api/0.6/relation/" + routenumber+"/full";
    xmlHttp.open("GET", url, true); // true for asynchronous 
    xmlHttp.send(null);
};

/**
 * Generate the content for the overlay based on the feature's properties.
 *
 * @param properties Properties of the feature.
 * @returns {string} HTML code for the overlay content.
 */
var overlayContent = function (properties) {
    var info = "";
    info += "<strong>Route " + properties.ref + "</strong>";

    if (properties.hasOwnProperty("error_type")) {
        if (properties.error_type === "missing") {
            info += "<p class='warning'>This route is missing!</p>"
        } else if (properties.error_type === "difference") {
            info += "<p class='warning'>This route has geometrical issues!</p>";
            info += "<hr>";

            if (properties.difference_type === "missing") {
                info += "<p class='warning'>The selected segments are missing.</p>";
            } else if (properties.difference_type === "wrong") {
                info += "<p class='warning'>The selected segments shouldn't be here.</p>";
            }
        } else if (properties.error_type === "tagging") {
            info += "<p class='warning'>This route has tag issues!</p>";
        }
    } else {
        info += "<p>No issues with this route.</p>";
    }

    info += "<hr>";

    var keys = keysSorted(properties);
    for (var i = 0; i < keys.length; i++) {
        var property = keys[i];
        if (properties.hasOwnProperty(property) && property !== "error_type" && property !== "difference_type" && property !== "tagging_errors" && property !== "geometry") {
            info += "<p><strong>" + property + "</strong>: " + properties[property] + "</p>";
        }
    }
    
    if ("@id" in properties){
    info+="<button onclick='downloadRoute("+ properties["@id"].split('/')[1] + ")'>Open route in JOSM</button></p>"
    }

    if (properties.hasOwnProperty("tagging_errors")) {
        info += "<hr>";
        var issues = properties["tagging_errors"].split(";");

        for (i = 0; i < issues.length; i++) {
            info += "<p class='warning'>" + issues[i] + "</p>";
        }
    }
    



    return info;

};


var openBoundingBoxInJosm = function (routenumber)
{
   var boundaries=ol.proj.transformExtent(map.getView().calculateExtent(map.getSize()), map.getView().getProjection(), "EPSG:4326")
    var left_bound = boundaries[0];
    var bottom_bound = boundaries[1];
    var right_bound = boundaries[2];
    var top_bound = boundaries[3];

    var xmlHttp = new XMLHttpRequest();
    var url = "http://127.0.0.1:8111/load_and_zoom?left=" + left_bound + "&right=" + right_bound + "&top=" + top_bound + "&bottom=" + bottom_bound;
    xmlHttp.open("GET", url, true); // true for asynchronous 
    xmlHttp.send(null);



};

var select = new ol.interaction.Select({
    condition: ol.events.condition.click
});

map.addInteraction(select);

// Show overlay when selecting a feature or hide it when deselecting.
select.on('select', function (e) {
    if (e.selected.length > 0) {
        content.innerHTML = overlayContent(e.selected[0].getProperties());
        overlay.setPosition(e.mapBrowserEvent.coordinate);
    } else {
        overlay.setPosition(undefined);
        closer.blur();
    }
});

if (window.location.hash !== "") {
    // Try to restore center, zoom-level and rotation from the URL.
    var hash = window.location.hash.replace("#map=", "");
    var parts = hash.split("/");
    if (parts.length === 3) {
        zoom = parseInt(parts[0], 10);
        center = [
            parseFloat(parts[2]),
            parseFloat(parts[1])
        ];
        map.getView().setCenter(ol.proj.fromLonLat(center));
        map.getView().setZoom(zoom);
    }
}

// Update the base layer when changing the select.
document.getElementById("baselayers").onchange = function () {
    map.getLayers().setAt(0, baselayers[this.value]);
};

var shouldUpdate = true;
var view = map.getView();
var updatePermalink = function () {
    if (!shouldUpdate) {
        // do not update the URL when the view was changed in the "popstate" handler
        shouldUpdate = true;
        return;
    }

    var center = view.getCenter(), ll = ol.proj.toLonLat(center);
    var hash = "#map=" +
        view.getZoom() + "/" +
        Math.round(ll[1] * 100000) / 100000 + "/" +
        Math.round(ll[0] * 100000) / 100000;
    var state = {
        zoom: view.getZoom(),
        center: view.getCenter(),
        rotation: view.getRotation()
    };
    window.history.pushState(state, "map", hash);
};

map.on("moveend", updatePermalink);

// Restore the view state when navigating through the history, see
// https://developer.mozilla.org/en-US/docs/Web/API/WindowEventHandlers/onpopstate
window.addEventListener("popstate", function (event) {
    if (event.state === null) {
        return;
    }
    map.getView().setCenter(ol.proj.fromLonLat(event.state.center));
    map.getView().setZoom(event.state.zoom);
    shouldUpdate = false;
});

/**
 * Loads a route layer from the given file location and places it in the layers array at given index.
 *
 * @param file File location of the GeoJSON.
 * @param index Index of the layer.
 */
var loadLayers = function (file, index) {
    var vectorSource, vectorLayer;
    $.getJSON(file, function (json) {
        vectorSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(json, {
                dataProjection: "EPSG:4326",
                featureProjection: "EPSG:3857"
            })

        });
        vectorLayer = new ol.layer.Vector({
            source: vectorSource,
            style: function (feature) {
                var properties = feature.getProperties();
                var color = ol.color.asArray(properties.colour || "#000000");

                color[3] = 0.8;

                var stroke = new ol.style.Stroke({
                    color: color,
                    width: 10
                });
                return [
                    new ol.style.Style({
                        stroke: stroke
                    })
                ];
            }
        });
        map.addLayer(vectorLayer);
        vectorLayer.setVisible(false);

        layers[index] = vectorLayer;
    });
};

/**
 * Gets the colour based on the kind of errors in the feature.
 *
 * @param properties Properties of the feature.
 * @returns {*} OpenLayers color.
 */
var getColor = function (properties) {
    if ('error_type' in properties) {
        switch (properties.error_type) {
            case 'missing':
                return ol.color.asArray("#f40500");
            case 'difference':
            case 'tagging':
                return ol.color.asArray("#ffa000");
        }
    } else {
        return ol.color.asArray("#13cd00");
    }
};

/**
 * Gets the line dash based on the kind of errors in the feature.
 *
 * @param properties Properties of the feature.
 * @returns {*} Array of numbers representing dashed property.
 */
var getLineDash = function (properties) {
    if ('error_type' in properties && properties.error_type === "difference" && properties.difference_type === "wrong") {
        return [25, 25];
    } else {
        return undefined;
    }
};

/**
 * Loads a output layer from the given file location and places it in the outputs array at given index.
 *
 * @param file File location of the GeoJSON.
 * @param index Index of the layer.
 */
var loadOutput = function (file, index) {
    var vectorSource, vectorLayer;
    $.getJSON(file, function (json) {
        vectorSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(json, {
                dataProjection: "EPSG:4326",
                featureProjection: "EPSG:3857"
            })

        });
        vectorLayer = new ol.layer.Vector({
            source: vectorSource,
            style: function (feature) {
                var properties = feature.getProperties();
                var color = getColor(properties);

                color[3] = 0.8;

                var stroke = new ol.style.Stroke({
                    color: color,
                    width: 10,
                    lineDash: getLineDash(properties)
                });
                return [
                    new ol.style.Style({
                        stroke: stroke
                    })
                ];
            }
        });
        map.addLayer(vectorLayer);
        vectorLayer.setVisible(true);

        outputs[index] = vectorLayer;
    });
};

// Load the routes
$.each(routes, function (key, value) {
    loadLayers(routes_src + value + ".geojson", key);
});

// Load the outputs
$.each(routes, function (key, value) {
    loadOutput(output_src + value + ".geojson", key);
});
