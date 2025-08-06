from django.urls import path
from . import views

urlpatterns = [
    path('ajax/load-equipment/', views.load_equipment, name='ajax_load_equipment'),
    path('', views.submit_report, name='submit_report'),
    path('reports/', views.report_list, name='report_list'),  # <-- Важно!
]
