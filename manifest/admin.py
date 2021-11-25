from django.contrib import admin
from manifest.models import Skydiver, GiftCertificate, SkydivingService, BalanceOperation, CertificateBalanceOperation

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

@admin.register(CertificateBalanceOperation)
class CertificateBalanceOperationAdmin(admin.ModelAdmin):
    pass