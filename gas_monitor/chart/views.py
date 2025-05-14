import json
from django.shortcuts import render
from django.http import JsonResponse

from .models import GasRecord, Annotation


def records_json(request):
    # получаем последние, например, 100 записей
    qs = GasRecord.objects.all().order_by('-datetime')[:100]
    data = []
    for rec in reversed(qs):
        data.append({
            'datetime': rec.datetime.isoformat(),
            'gas_rate_fact': rec.gas_rate_fact,
            'gas_rate_plan': rec.gas_rate_plan,
        })
    return JsonResponse(data, safe=False)


def index(request):
    return render(request, 'chart/index.html')


def annotations_json(request):
    qs = Annotation.objects.all()
    data = [
        {
            'timestamp': ann.timestamp.isoformat(),
            'text': ann.text
        }
        for ann in qs
    ]
    return JsonResponse(data, safe=False)
