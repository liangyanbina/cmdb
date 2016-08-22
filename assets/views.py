# -*- coding=utf-8 -*-
from django.shortcuts import render,HttpResponse,redirect
from django.core.exceptions import ObjectDoesNotExist
import models
from django.views.decorators.csrf import csrf_exempt
import json,datetime
from assets import html_form

# Create your views here.
def test(request,obj=None):
    if request.method == "GET":
        asset = models.Asset.objects.all()
        BusinessUnit = models.BusinessUnit.objects.all()
        idc = models.IDC.objects.all()
        status = models.Asset.objects.all()
        return render(request,"test.html",{"BusinessUnit":BusinessUnit,"idc":idc,"status":status})
    else:
        print request.POST.get('BusinessUnit')
        print request.POST.get('idc')
        print request.POST
        return HttpResponse('ok')

def index(request):
    return redirect("/cmdb/main")

def main(request):
    if request.method == "GET":
        asset_list = models.Asset.objects.all()
        BusinessUnit = models.BusinessUnit.objects.all()
        idc = models.IDC.objects.all()
        counts = asset_list.count()
        # return render(request, "main.html",{"asset":assets_list,"header":u"资产列表",'counts':counts,"BusinessUnit":BusinessUnit,"idc":idc,"status":assets_list})
    else:
        BusinessUnit = models.BusinessUnit.objects.all()
        idc = models.IDC.objects.all()
        info = request.POST
        asset_list = models.Asset.objects.all()
        if info.get('status') != "-1":
            asset_list = asset_list.filter(status=info.get('status'))
        if info.get('BusinessUnit') != "-1":
            asset_list = asset_list.filter(business_unit_id=info.get('BusinessUnit'))
        if info.get('asset_ip'):
            asset_list = asset_list.filter(ip__contains=info.get('asset_ip'))
        if info.get('idc') != "-1":
            asset_list = asset_list.filter(idc_id=info.get('idc'))
        if info.get('sn'):
            asset_list = asset_list.filter(sn__contains=info.get('sn'))
        counts = asset_list.count()
    return render(request, "main.html",{"asset":asset_list,"header":u"资产列表",'counts':counts,"BusinessUnit":BusinessUnit,"idc":idc,"status":asset_list})
def server(request):
    if request.method == "GET":
        server_list = models.Server.objects.all()
    else:
        info = request.POST
        server_list = models.Server.objects.all()
        if info.get('ip'):
            server_list = server_list.filter(asset__ip=info.get('ip'))
    return render(request, "server.html",{"server":server_list})

def server_detail(request,obj):
    header = u"服务器详细信息"
    server_obj = models.Server.objects.get(asset__ip=obj)
    server_modelform = html_form.servermoelsform(instance=server_obj)
    if request.method == "POST":
        f1 = html_form.servermoelsform(request.POST,instance=server_obj)
        f1.save()
        return redirect("/cmdb/server")
    return render(request, "server_form.html", {"form":server_modelform, "ass_obj": obj, "header": header})

def idc(request,obj):
    if request.method == "GET":
        if obj == u"":
            idc_list = models.IDC.objects.all()
            return render(request, "idc.html",{"idc_list":idc_list})
        else:
            asset_list =models.Asset.objects.filter(idc__name=obj)
            return render(request, "main.html", {"asset":asset_list, "name":obj})

def yewu(request,obj):
    if request.method =="GET":
        if obj == u"":
            yewu_list = models.BusinessUnit.objects.all()
            for i in yewu_list:
                asset_count = models.Asset.objects.filter(business_unit__name=i).count()
                models.BusinessUnit.objects.filter(name=i).update(asset_count=asset_count)
            return render(request, "yewu.html",{"yewu_list":yewu_list})
        else:
            asset_list = models.Asset.objects.filter(business_unit__name=obj)
            return render(request, "main.html", {"asset": asset_list, "header": obj})
    else:
        return HttpResponse("ok")

def expired(request,obj):
    expired_list = []
    now = datetime.date.today()
    expired_asset = models.Asset.objects.filter(status__lt=2)
    # 当obj=0表示列出已经过保修的设备
    if obj == '0':
        name = '已过保修设备'
        for k in expired_asset:
            date1 = k.expire_date
            if date1:
                nu = (date1 - now).days
                if nu < 0:
                    expired_list.append(k)
    else:
        name = "即过保修设备"
        for k in expired_asset:
             date1 = k.expire_date
             if date1:
                 nu = (date1 - now).days
                 if nu <30 and nu >0:
                     expired_list.append(k)
    return render(request,"expired.html",{'expired_list':expired_list,'name':name})

def asset_detailmodelform(request,obj):
    header =u"资产详细信息"
    ass = models.Asset.objects.get(ip=obj)
    form = html_form.Assetmoelsform(instance=ass)
    if request.method == "POST":
        f = html_form.Assetmoelsform(request.POST,instance=ass)
        f.save()
        return redirect("/cmdb/main")
    return render(request,"modelsform_detail.html",{"form":form,"ass_obj":ass.ip,"header":header })

@csrf_exempt
def asset_add(request):
    if request.method == "POST":
        ip = request.META['REMOTE_ADDR']
        device_serial = request.POST.get('device_serial')
        device_manufacturer = request.POST.get('device_manufacturer')
        obj = models.Asset.objects.get_or_create(ip=ip)
        if device_serial:
            models.Asset.objects.filter(ip=ip).update(sn = device_serial)
        if device_manufacturer:
            obj = models.Manufactory.objects.get_or_create(manufactory=device_manufacturer)
            models.Asset.objects.filter(ip=ip).update(manufactory= obj[0])
    else:
        pass
    return HttpResponse('ok')

@csrf_exempt
def asset_cpu(request):
    if request.method == "POST":
        ip = request.META['REMOTE_ADDR']
        cpu_info = request.POST
        try:
            asset = models.Asset.objects.get(ip=ip)
        except:
            return HttpResponse("no asset")
        try:
            models.CPU.objects.get(asset = asset)
            models.CPU.objects.filter(asset = asset).update(cpu_model=cpu_info.get('cpu_model'),
                                    cpu_count=cpu_info.get('cpu_count'),
                                    cpu_core_count=cpu_info.get('cpu_core_count'),)
            return HttpResponse("cpu asset already update")
        except ObjectDoesNotExist:
            models.CPU.objects.create(asset=asset,cpu_model=cpu_info.get('cpu_model'),
                                      cpu_count=cpu_info.get('cpu_count'),
                                      cpu_core_count=cpu_info.get('cpu_core_count'))
    else:
        pass
    return HttpResponse("ok")

@csrf_exempt
def asset_server(request):
    if request.method == "POST":
        ip = request.META['REMOTE_ADDR']
        post_info = json.loads(request.body)
        disk_total = str(post_info.get('disk_total')).replace('u','')
        try:
            asset = models.Asset.objects.get(ip=ip)
            if models.CPU.objects.filter(asset=asset):
                cpu_obj = models.CPU.objects.get(asset=asset)
        except:
            return HttpResponse("no asset")
        try:
            models.Server.objects.get(asset=asset)
            models.Server.objects.filter(asset=asset).update(asset=asset,
                                                             physical_disk_driver=disk_total,
                                                             ram_capacity=post_info.get('mem_total'),
                                                             os_type=post_info.get('os_type'),
                                                             os_release=post_info.get('os_version'),
                                                             open_port=post_info.get('open_port'),)
            obj = models.Server.objects.filter(asset=asset).values('S_cpu')
            if not obj[0].get("S_cpu") and cpu_obj:
                models.Server.objects.filter(asset=asset).update(S_cpu=cpu_obj)
            if post_info.get("device_model"):
                models.Server.objects.filter(asset=asset).update(model=post_info.get("device_model"))
            return HttpResponse("server asset exits")
        except ObjectDoesNotExist:
            models.Server.objects.create(asset=asset,physical_disk_driver=disk_total,
                                                             ram_capacity=post_info.get('mem_total'),
                                                             os_type=post_info.get('os_type'),
                                                             os_release=post_info.get('os_version'),
                                                             open_port=post_info.get('open_port'),)
            asset_cpu = models.CPU.objects.filter(asset = asset)
            if asset_cpu:
                models.Server.objects.filter(asset=asset).update(S_cpu=cpu_obj)
            if post_info.get("device_model"):
                models.Server.objects.filter(asset=asset).update(model=post_info.get("device_model"))
    else:
        pass
    return HttpResponse("ok")