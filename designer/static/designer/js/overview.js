$(function() {
    OverviewDesigner = {
        units: [],

        /* Create the map, add an overlay & load all units */
        init: function() {
            var container = document.getElementById('designer-overview-map-container');
            this.map = new google.maps.Map(container, {
                center: {lat: 37.980, lng: 23.72},
                zoom: 13
            });

            this.overlay = new google.maps.OverlayView();
            this.overlay.draw = function() {};
            this.overlay.setMap(this.map);

            //load existing units
            this.load_units();
        },

        /* Given an existing unit add its corresponding marker */
        place_existing_marker: function(unit) {
            var point = new google.maps.LatLng(unit.location.lat, unit.location.lng);
            return this.place_marker(unit.unit_type, point);
        },

        /* Given a unit type & an overlay add a new marker */
        place_marker: function(unit_type, ll) {
            var that = this;
            var icon_path;

            if (unit_type == 'GENERIC_BUILDING') {
                icon_path = fontawesome.markers.BUILDING;
            }
            else if (unit_type == 'FACTORY') {
                icon_path = fontawesome.markers.INDUSTRY;
            }
            else if (unit_type == 'CHARGING_STATION') {
                icon_path = fontawesome.markers.BOLT;
            }
            else {
                icon_path = fontawesome.markers.QUESTION;
            }

            return new google.maps.Marker({
                position: ll,
                map: that.map,
                icon: {
                    path: icon_path,
                    scale: 0.5,
                    strokeWeight: 0.2,
                    strokeColor: '#777',
                    strokeOpacity: 1,
                    fillColor: '#777',
                    fillOpacity: 1,
                },
                clickable: true,
                draggable: true
            });
        },

        /* Get all units, save them & add their markers */
        load_units: function() {
            // get list of user's units
            var that = this;
            $.ajax({
                url: '/designer/api/units/all/',
                method: 'GET',
                success: function(units) {
                    that.units = units;

                    // add units to map
                    for (var i=0; i<units.length; i++) {
                        that.units[i].marker = that.place_existing_marker(units[i]);
                    }

                    // move the map to the correct point/zoom level
                    that.map.fitBounds(that.get_all_markers().reduce(function(bounds, marker) {
                        return bounds.extend(marker.getPosition());
                    }, new google.maps.LatLngBounds()));
                }
            });
        },

        /* Returns a list with all markers */
        get_all_markers: function() {
            var markers = [];
            for (var i=0; i<this.units.length; i++) {
                markers.push(this.units[i].marker);
            }

            return markers;
        },

        /* Show the correct create form for a new unit */
        show_create_form: function(unit_type, ll) {
            // show the dialog
            var cf = $('#unit-create-modal');
            cf.html(LOADING_UNIT_TEMPLATE);
            cf.modal('show');

            // populate with the form
            var that = this;
            $.ajax({
                url: '/designer/unit-create/' + unit_type + '/',
                method: 'GET',
                data: {
                    lat: ll.lat(),
                    lng: ll.lng()
                },
                success: function(data) {
                    cf.html(data)
                }
            });
        }
    };

    // initialize the designer
    OverviewDesigner.init();

    // add new units in the map
    $(".add-unit").draggable({
        helper: 'clone',
        stop: function(e, ui) {
            var od = OverviewDesigner;
            var unit_type = $(e.target).data('unit_type');

            var map_offset = $(od.map.getDiv()).offset();
            var point = new google.maps.Point(
                ui.offset.left - map_offset.left + (ui.helper.width() / 2),
                ui.offset.top - map_offset.top + ui.helper.height()
            );

            var ll = od.overlay.getProjection().fromContainerPixelToLatLng(point);
            od.orphan_marker = od.place_marker(unit_type, ll);

            // show the form for the new unit
            od.show_create_form(unit_type, ll);
        }
    });

    function async_form_submit(form, on_success, on_error) {
        var submit = form.find('input[type="submit"]')
        submit.attr('disabled', 'disabled');
        submit.addClass('disabled');

        // get method & form data
        var data;
        var url = form.attr('action');
        var method = form.attr('method');
        if (method == 'GET') {
            data = form.serialize();
            url += '?' + data;
        } else {
            data = new FormData(form[0]);
        }

        // make the request
        $.ajax({
            url   : url,
            type  : method,
            data  : data, // data to be submitted
            async: true,
            cache: false,
            contentType: false,
            processData: false,
            success: function(data, textStatus, request){
                submit.attr('disabled', undefined);
                submit.removeClass('disabled');

                on_success(data, textStatus, request)
            },
            error: function(xhr, status, error) {
                on_error(xhr, status, error)
            }
        });
    }

    // asynchronous unit create view
    $(document).on('submit', '#unit-create-modal form', function(e) {
        var form = $(this);
        var cf = $('#unit-create-modal');

        // define the callbacks
        var on_success = function(unit, textStatus, request) {
            cf.modal('hide');

            // add the unit to the designer & attach the marker
            unit.marker = OverviewDesigner.orphan_marker;
            OverviewDesigner.units.push(unit);
            OverviewDesigner.orphan_marker = undefined;
        };

        var on_error = function(xhr, status, error) {
            cf.html(xhr.responseText);
        };

        // submit the form
        async_form_submit(form, on_success, on_error);

        e.preventDefault();
        return false;
    });
});