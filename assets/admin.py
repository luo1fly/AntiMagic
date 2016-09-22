from django.contrib import admin
from assets import models
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
# Register your models here.


class ServerInline(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)
    readonly_fields = ['create_date']


class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']


class NICInline(admin.TabularInline):
    model = models.NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']


class RAMInline(admin.TabularInline):
    model = models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']


class DiskInline(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_type', 'sn', 'name', 'vendor', 'management_ip', 'idc', 'business_unit')
    inlines = [ServerInline, CPUInline, RAMInline, DiskInline, NICInline]
    search_fields = ['sn', ]
    list_filter = ['idc', 'vendor', 'business_unit', 'asset_type']


class NicAdmin(admin.ModelAdmin):
    list_display = ('name', 'mac', 'ip', 'net_mask', 'bonding')
    search_fields = ('mac', 'ip')


class EventLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'colored_event_type', 'asset', 'component', 'detail', 'date', 'user')
    search_fields = ('asset',)
    list_filter = ('event_type', 'component', 'date', 'user')


class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = (
        'sn', 'asset_type', 'vendor', 'model', 'cpu_model', 'cpu_count', 'cpu_core_count',
        'ram_size', 'os_distribution', 'os_release', 'date', 'approved', 'approved_by', 'approved_date'
    )
    actions = ['approve_selected_objects']

    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

    approve_selected_objects.short_description = "批准入库"


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.IDC)
admin.site.register(models.BusinessUnit)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.NIC, NicAdmin)
admin.site.register(models.RAM)
admin.site.register(models.Manufactory)
admin.site.register(models.Tag)
admin.site.register(models.Software)
admin.site.register(models.EventLog, EventLogAdmin)
admin.site.register(models.NewAssetApprovalZone, NewAssetApprovalZoneAdmin)
