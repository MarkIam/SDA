from django.contrib import admin
from manifest.models import Skydiver, GiftCertificate, SkydivingService, BalanceOperation, SkydiveDiscipline, SkydiverRequest, PlaneType, Plane, PlaneLift, RequestService

@admin.register(Skydiver)
class SkydiverAdmin(admin.ModelAdmin):
    list_filter = ('last_name', 'first_name')    
    list_filter = ('last_name', 'phone_number')
    
@admin.register(GiftCertificate)
class GiftCertificateAdmin(admin.ModelAdmin):
    pass

@admin.register(SkydivingService)
class SkydivingServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(BalanceOperation)
class BalanceOperationAdmin(admin.ModelAdmin):
    pass

@admin.register(SkydiveDiscipline)
class SkydiveDisciplineAdmin(admin.ModelAdmin):
    pass

class RequestServiceInline(admin.TabularInline):
    model = RequestService
    
@admin.register(SkydiverRequest)
class SkydiverRequestAdmin(admin.ModelAdmin):
    inlines = [
       RequestServiceInline
   ]

@admin.register(PlaneType)
class PlaneTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    pass

@admin.register(PlaneLift)
class PlaneLiftAdmin(admin.ModelAdmin):
    pass