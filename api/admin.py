from django.contrib import admin
from .models import *


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'price']
    search_fields = ['full_name', 'position']


@admin.register(MainService)
class MainServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name']


@admin.register(InstrumentalService)
class InstrumentalServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'service_price']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_id', 'service_name']
    search_fields = ['service_name', 'service_price']
    exclude = ['is_checked']


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'pass_data', 'inspaction', 'staff', 'created_date', 'room']
    search_fields = ['full_name', 'pass_data', 'inspaction', 'created_date']
    exclude = ['discount']


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = ['patient', 'result', 'service', 'created_date']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_personal', 'room_price']


@admin.register(PatientService)
class PatientServiceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'service']

