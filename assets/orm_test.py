#!/usr/bin/python
# -*- coding=utf-8 -*-

import datetime
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cmdb.settings'
import django
django.setup()
from django.core.exceptions import ObjectDoesNotExist
from assets import models

# idc = models.Asset.objects.all()
# idc = models.Asset.objects.filter(Extranet_ip="4.4.4.4")
# print idc

# s = models.Server.objects.get(asset__ip = "122.49.38.150")
# print s
# s.model = 'R120'
# s.save()

# p = models.Server.objects.filter(asset__ip = "122.49.38.167").update(model='R500')

# c = models.CPU.objects.filter(asset__ip = "122.49.38.169").update(cpu_model = "I5-5200")

# 添加服务器：
# p = models.Asset.objects.get(ip = "127.0.0.1")
# print type(p)
#
# s = models.Server.objects.filter(asset = p).update(model='IBM X3650')
# print s
#

#判断IP地址是否存在进行添加
# ip = "192.168.2.204"
# try:
#     obj = models.Asset.objects.get(ip=ip)
#     print obj
# except ObjectDoesNotExist:
#     obj = models.Asset.objects.create(ip=ip)
#     print obj
ip = '192.168.100.144'
# cpu_obj = models.CPU.objects.filter(asset = ip)
# obj = models.Server.objects.filter(asset=ip).values('S_cpu')
# models.Asset.objects.filter(ip=ip).update(sn="0002")
# obj = models.Asset.objects.select_related().get(ip=ip)
# print obj.server
# obj = models.Asset.objects.all().count()
# print obj

# name = u"公共服务"
# expired_asset = models.Asset.objects.filter(status__lt=2).values('ip','name',
#                                                                  'asset_type','sn','trade_date',
#                                                                  'business_unit','expire_date','status')
# print expired_asset
# now = datetime.date.today()
# for k in expired_asset:
#     date1 = k.get('expire_date')
#     if date1:
#         nu = (date1 - now).days
#         print nu
obj = models.Asset.objects.all()
q = obj.filter(status=0)
print q.filter(idc=u'北京办公区')

