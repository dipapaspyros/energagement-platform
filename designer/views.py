from django.shortcuts import render
from django.utils.safestring import mark_safe

from energagement.settings import GEOCODING_API_KEY
from structure.forms import UnitForm
from structure.lists import UNIT_TYPES
from googlemaps import Client as GoogleMaps
from django.template import loader, Context

gmaps = GoogleMaps(GEOCODING_API_KEY)

unit_icon_classes = {
    'GENERIC_BUILDING': 'fa-building',
    'FACTORY': 'fa-industry',
    'CHARGING_STATION': 'fa-bolt',
}

LOADING_UNIT_TEMPLATE = mark_safe(loader.get_template('designer/unit/form-create-loading.html').render(Context({}))\
    .replace('\n', '').replace("'", "\\'"))


def get_unit_types_info():
    return [{
        'unit_type': ut[0],
        'label': ut[1],
        'icon_class': unit_icon_classes[ut[0]],
    } for ut in UNIT_TYPES]


# A map view with a list of different units
def overview(request):
    ctx = {
        'unit_types': get_unit_types_info(),
        'LOADING_UNIT_TEMPLATE': LOADING_UNIT_TEMPLATE,
    }

    return render(request, 'designer/overview.html', ctx)


def unit_create_form(request, unit_type):
    unit_type_label = [ut[1] for ut in UNIT_TYPES if ut[0] == unit_type][0]
    initial = {}

    if 'lat' in request.GET and 'lng' in request.GET:
        initial['lat'] = float(request.GET.get('lat'))
        initial['lng'] = float(request.GET.get('lng'))

        # use Google Geocoding API to get the address
        rg = gmaps.reverse_geocode((initial['lat'], initial['lng']))
        if rg:
            initial['address'] = rg[0]['formatted_address']

    form = UnitForm(unit_type=unit_type, initial=initial)

    return render(request, 'designer/unit/form-create-contents.html', {
        'unit_type': unit_type,
        'unit_type_label': unit_type_label,
        'form': form,
    })


# A detailed view of a specific unit
def details(request, unit_id):
    pass
