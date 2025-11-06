from django.contrib import admin
from .models import CarBrand, CarModel, CarElement, PriceConfig, ServiceType, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'e_mail', 'address', 'time_w']
    search_fields = ['name', 'phone', 'e_mail', 'address', 'time_w']

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name', 'tinting', 'protect']
    list_filter = ['brand']
    search_fields = ['name', 'brand__name', 'tinting', 'protect']

@admin.register(CarElement)
class CarElementAdmin(admin.ModelAdmin):
    list_display = ['name', 'element_type', 'code']
    list_filter = ['element_type']
    search_fields = ['name', 'code']

class PriceConfigInline(admin.TabularInline):
    model = PriceConfig
    extra = 1
    fields = ['element', 'service_type', 'price']

@admin.register(PriceConfig)
class PriceConfigAdmin(admin.ModelAdmin):
    list_display = ['car_model', 'element', 'service_type', 'price']
    list_filter = ['car_model__brand', 'service_type', 'element__element_type']
    search_fields = ['car_model__name', 'element__name']
    list_editable = ['price']

@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']