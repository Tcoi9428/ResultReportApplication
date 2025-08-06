from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import ServiceReport, Organization, EquipmentModel, Equipment, Reglament , Personal
from django import forms


class ServiceReportForm(forms.ModelForm):
    class Meta:
        model = ServiceReport
        fields = '__all__'
        widgets = {
            'service_work_description': forms.Textarea(attrs={'rows': 2}),
            'service_used_materials': forms.Textarea(attrs={'rows': 2}),
            'service_defect_description': forms.Textarea(attrs={'rows': 2}),
            'service_recomendation': forms.Textarea(attrs={'rows': 2}),
            'service_employer_fio': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '3'}),
            'service_work_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'service_time_start': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'service_time_end': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(ServiceReportForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.FileInput) and field_name != 'service_employer_fio':
                field.widget.attrs['class'] = 'form-control'
         

def load_equipment(request):
    org_id = request.GET.get('organization_id')
    equipment = Equipment.objects.filter(organization_id=org_id).values('id', 'factory_number', 'garage_number')
    equipment_list = list(equipment)
    return JsonResponse(equipment_list, safe=False)

def submit_report(request):
    if request.method == 'POST':
        form = ServiceReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('report_list')  # <-- предпочтительно использовать именованный URL
    else:
        form = ServiceReportForm()
    return render(request, 'submit_report.html', {'form': form})


def report_list(request):
    reports = ServiceReport.objects.all().order_by('-service_work_date')

    # Фильтры
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    organization_id = request.GET.get('organization')
    model_id = request.GET.get('model')
    equipment_id = request.GET.get('equipment')
    reglament_id = request.GET.get('reglament')

    if date_from:
        reports = reports.filter(service_work_date__gte=date_from)
    if date_to:
        reports = reports.filter(service_work_date__lte=date_to)
    if organization_id:
        reports = reports.filter(service_organization_id=organization_id)
    if model_id:
        reports = reports.filter(equip_model_id=model_id)
    if equipment_id:
        reports = reports.filter(equipment_id=equipment_id)
    if reglament_id:
        reports = reports.filter(service_reglament_work_type_id=reglament_id)

    context = {
        'reports': reports,
        'organizations': Organization.objects.all(),
        'models': EquipmentModel.objects.all(),
        'equipments': Equipment.objects.all(),
        'reglaments': Reglament.objects.all(),
        'selected_filters': {
            'date_from': date_from,
            'date_to': date_to,
            'organization': organization_id,
            'model': model_id,
            'equipment': equipment_id,
            'reglament': reglament_id,
        }
    }
    return render(request, 'report_list.html', context)
