$(function() {
    OverviewDesigner = {

        init: function() {
            var container = document.getElementById('designer-overview-map-container');
            this.map = new google.maps.Map(container, {
                center: {lat: 37.980, lng: 23.72},
                zoom: 13
            });

            this.overlay = new google.maps.OverlayView();
            this.overlay.draw = function() {};
            this.overlay.setMap(this.map);
        },

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

            var marker = new google.maps.Marker({
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

        show_create_form: function(unit_type, ll) {
            // show the dialog
            var cf = $('#unit-create-modal');
            cf.html(LOADING_UNIT_TEMPLATE);
            cf.modal('show');

            // populate with the form
            $.ajax({
                url: '/designer/unit-create/' + unit_type + '/',
                method: 'GET',
                data: {
                    lat: ll.lat(),
                    lng: ll.lng()
                },
                success: function(data) {
                    cf.html(data);
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
            var unit_type = $(e.target).data('unit_type');

            var map_offset = $(OverviewDesigner.map.getDiv()).offset();
            var point = new google.maps.Point(
                ui.offset.left - map_offset.left + (ui.helper.width() / 2),
                ui.offset.top - map_offset.top + ui.helper.height()
            );

            var ll = OverviewDesigner.overlay.getProjection().fromContainerPixelToLatLng(point);
            OverviewDesigner.place_marker(unit_type, ll);

            // show the form for the new unit
            OverviewDesigner.show_create_form(unit_type, ll);

        }
    });
});