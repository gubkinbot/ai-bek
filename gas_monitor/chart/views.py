import json
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime

from .models import GasRecord, Annotation


from django.http import JsonResponse
from .models import GasRecord

def records_json(request):
    qs = GasRecord.objects.order_by('-datetime')[:]
    data = []
    for rec in reversed(qs):
        # если datetime = None — пропустим или вернём пустую строку
        dt = rec.datetime.isoformat() if rec.datetime else ''
        data.append({
            'datetime':      rec.datetime,
            'gas_rate_fact': rec.gas_rate_fact,
            'gas_rate_plan': rec.gas_rate_plan,
            'gas_rate_v1':   rec.gas_rate_v1,
            'gas_rate_v2':   rec.gas_rate_v2,
            'gas_rate_v3':   rec.gas_rate_v3,
        })
    return JsonResponse(data, safe=False)

def index(request):
    return render(request, 'chart/index.html')


@csrf_exempt
def annotations_json(request):
    if request.method == 'GET':
        qs = Annotation.objects.all().order_by('timestamp')
        data = [
            {
                'timestamp': ann.timestamp.isoformat(),
                'text':      ann.text,
                'author':    ann.author
            }
            for ann in qs
        ]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            text = payload.get('text','').strip()
            author = payload.get('author','').strip() or 'Anonymous'
            ts_str = payload.get('timestamp','')
            if not text or not ts_str:
                return HttpResponseBadRequest('text and timestamp required')

            timestamp = parse_datetime(ts_str)
            if timestamp is None:
                return HttpResponseBadRequest('invalid timestamp format')

            ann = Annotation.objects.create(
                text=text, author=author, timestamp=timestamp
            )

            return JsonResponse({
                'timestamp': ann.timestamp.isoformat(),
                'text':      ann.text,
                'author':    ann.author
            }, status=201)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('invalid JSON')

    return HttpResponseBadRequest('only GET and POST allowed')
