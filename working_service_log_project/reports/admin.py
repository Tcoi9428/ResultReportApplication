from django.contrib import admin
from .models import ServiceReport , EquipmentModel, Equipment, Organization ,Reglament ,Personal

admin.site.register(ServiceReport)
admin.site.register(EquipmentModel)
admin.site.register(Equipment)
admin.site.register(Organization)
admin.site.register(Reglament)
admin.site.register(Personal)