from django.urls import path
from .views import index, records_json, annotations_json

urlpatterns = [
    path('', index, name='index'),
    path('api/records/', records_json, name='records_json'),
    path('api/annotations/', annotations_json, name='annotations_json'),
]
