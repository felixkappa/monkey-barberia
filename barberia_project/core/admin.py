from django.contrib import admin
from .models import InformacionGeneral

@admin.register(InformacionGeneral)
class InformacionGeneralAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha_actualizacion')