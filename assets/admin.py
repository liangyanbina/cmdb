# -*- coding=utf-8 -*-
from django.contrib import admin
from assets import models
from django import forms
# Register your models here.

# class ServerInline(admin.TabularInline):
#     model = models.Server
def set_status_0(modeladmin,request,queryset):
    queryset.update(status = 0)
set_status_0.short_description = '设置选中状态为"正常"'

def set_status_1(modeladmin,request,queryset):
    queryset.update(status = 1)
set_status_1.short_description = '设置选中状态为"维护"'

def set_status_2(modeladmin,request,queryset):
    queryset.update(status = 2)
set_status_2.short_description = '设置选中状态为"停用"'

def set_status_3(modeladmin,request,queryset):
    queryset.update(status = 3)
set_status_3.short_description = '设置选中状态为"报废"'

def set_status_4(modeladmin,request,queryset):
    queryset.update(status = 4)
set_status_4.short_description = '设置选中状态为"未知"'


class ServerInline(admin.StackedInline):
    model = models.Server
    exclude = ('memo','open_port','create_date',)
    readonly_fields = ['create_date']

class CPUInline(admin.StackedInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']


class Assetadmin(admin.ModelAdmin):
    list_display = ('ip','asset_type','name','sn','manufactory','trade_date','expire_date','business_unit','idc','status','update_date','created_by','memo')
    search_fields = ('ip','name','manufactory__manufactory','idc__name')
    list_per_page = 10
    # list_filter = ('create_date',)
    inlines = (ServerInline,)
    ordering = ('create_date',)
    actions = [set_status_0,set_status_1,set_status_2,set_status_3,set_status_4]

class serveradmin(admin.ModelAdmin):
    list_display = ('asset','created_by','model','S_cpu','ram_capacity','physical_disk_driver','os_type','os_release','open_port')
    list_per_page = 10
class Manufactoryadmin(admin.ModelAdmin):
    list_display = ('manufactory','support_num',"memo")
    list_per_page = 10
class IDCadmin(admin.ModelAdmin):
    list_display = ('name','bandwidth',"linkman",'phone','address','network','operator','memo')
    list_per_page = 10
class CPUadmin(admin.ModelAdmin):
    list_display = ('asset','cpu_model','cpu_count','cpu_core_count','memo')
    list_per_page = 10
class userprofileadmin(admin.ModelAdmin):
    list_display = ('user','name','Department',)
    list_per_page = 10

class diskadmin(admin.ModelAdmin):
    list_display = ('asset','slot','manufactory','model','capacity','iface_type','create_date','memo',)
    fields = ['asset','model','iface_type','slot','capacity','manufactory']
    list_per_page = 10
admin.site.register(models.Asset,Assetadmin)
admin.site.register(models.Server,serveradmin)
admin.site.register(models.NetworkDevice)
admin.site.register(models.CPU,CPUadmin)
admin.site.register(models.Disk,diskadmin)
admin.site.register(models.Manufactory,Manufactoryadmin)
admin.site.register(models.BusinessUnit)
admin.site.register(models.IDC,IDCadmin)
admin.site.register(models.UserProfile,userprofileadmin)