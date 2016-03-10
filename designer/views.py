from django.http import HttpResponse, JsonResponse
from django.middleware import csrf
from django.shortcuts import render
from django.utils.safestring import mark_safe

from energagement.settings import GEOCODING_API_KEY
from structure.forms import UnitForm
from structure.lists import UNIT_TYPES, get_tupple_label
from googlemaps import Client as GoogleMaps
from django.template import loader, Context

from structure.models import Unit

gmaps = GoogleMaps(GEOCODING_API_KEY)

unit_icon_classes = {
    'GENERIC_BUILDING': 'fa-building',
    'FACTORY': 'fa-industry',
    'CHARGING_STATION': 'fa-bolt',
}

LOADING_UNIT_TEMPLATE = mark_safe(loader.get_template('designer/unit/form-create-loading.html').
                                  render(Context({})).replace('\n', '').replace("'", "\\'"))


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
        'units': Unit.objects.filter(user=request.user),
        'LOADING_UNIT_TEMPLATE': LOADING_UNIT_TEMPLATE,
    }

    return render(request, 'designer/overview.html', ctx)


# render the correct form based on the unit type
def unit_create_form(request, unit_type):
    if request.method != 'GET':
        return HttpResponse('Only GET method is accepted', status=400)

    try:
        unit_type_label = [ut[1] for ut in UNIT_TYPES if ut[0] == unit_type][0]
    except IndexError:
        return HttpResponse('Invalid `unit_type`', status=400)

    initial = {'unit_type': unit_type}

    if 'lat' in request.GET and 'lng' in request.GET:
        initial['lat'] = float(request.GET.get('lat'))
        initial['lng'] = float(request.GET.get('lng'))

        # use Google Geocoding API to get the address
        rg = gmaps.reverse_geocode((initial['lat'], initial['lng']), language='el')
        if rg:
            initial['address'] = rg[0]['formatted_address']

    form = UnitForm(initial=initial, unit_type=unit_type)

    return render(request, 'designer/unit/form-create-contents.html', {
        'unit_type': unit_type,
        'unit_type_label': unit_type_label,
        'form': form,
    })


# process the unit create form
def unit_create(request):
    if request.method != 'POST':
        return HttpResponse('Only POST method is accepted', status=400)

    try:
        unit_type = request.POST.get('unit_type')
        unit_type_label = get_tupple_label(UNIT_TYPES, unit_type)
    except IndexError:
        return HttpResponse('Invalid `unit_type`', status=400)

    form = UnitForm(request.POST, unit_type=unit_type)
    if form.is_valid():
        # save the new unit & return empty response
        unit = form.save(commit=False)
        unit.user = request.user
        unit.save()

        return JsonResponse(unit.to_dict(), safe=False)
    else:
        # return form with errors
        c = Context({
            'unit_type': unit_type,
            'unit_type_label': unit_type_label,
            'form': form,
            'csrf_token': csrf.get_token(request),
        })

        response = mark_safe(loader.get_template('designer/unit/form-create-contents.html').render(c))
        return HttpResponse(response, status=400)


# A detailed view of a specific unit
def details(request, unit_id):
    pass
