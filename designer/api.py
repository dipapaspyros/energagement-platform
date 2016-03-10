from django.http import JsonResponse

from structure.models import Unit


def unit_list(request):
    return JsonResponse([u.to_dict() for u in Unit.objects.filter(user=request.user)], safe=False)
