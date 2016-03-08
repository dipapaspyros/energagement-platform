from django.shortcuts import render

from structure.lists import UNIT_TYPES


unit_icon_classes = {
    'GENERIC_BUILDING': 'fa-building',
    'FACTORY': 'fa-industry',
    'CHARGING_STATION': 'fa-bolt',
}


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
    }

    return render(request, 'designer/overview.html', ctx)


# A detailed view of a specific unit
def details(request, unit_id):
    pass
