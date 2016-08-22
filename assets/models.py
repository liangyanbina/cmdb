# -*- coding=utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Asset(models.Model):
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(u'设备类型',choices=asset_type_choices,max_length=64, default='server')
    name = models.CharField(u'服务名称',max_length=64,null=True,blank=True)
    ip = models.GenericIPAddressField(u'管理地址',max_length=64,unique=True)
    sn = models.CharField(u'资产SN号',max_length=64, unique=True,blank=True,null=True)
    manufactory = models.ForeignKey('Manufactory',verbose_name=u'制造商',null=True, blank=True)
    # model = models.ForeignKey('ProductModel', verbose_name=u'型号')

    trade_date = models.DateField(u'购买时间',null=True, blank=True)
    expire_date = models.DateField(u'过保修期',null=True, blank=True)
    # price = models.FloatField(u'价格',null=True, blank=True)
    business_unit = models.ForeignKey('BusinessUnit', verbose_name=u'所属业务线',null=True, blank=True)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房',null=True, blank=True)
    created_by_choices = (
        ('auto','Auto'),
        ('manual','Manual'),
    )
    created_by = models.CharField(choices=created_by_choices,max_length=32,default='auto')
    asset_status_choices = (
        ('0', u'正常'),
        ('1', u'维护中'),
        ('2', u'停用'),
        ('3', u'报废'),
        ('4', u'未知'),
    )
    status = models.CharField(u'设备状态',choices=asset_status_choices,max_length=8,default=4)
    #Configuration = models.OneToOneField('Configuration',verbose_name='配置管理',blank=True,null=True)

    memo = models.CharField(u'备注',max_length=128, null=True, blank=True)
    create_date = models.DateTimeField(u'创建时间',blank=True, auto_now_add=True)
    update_date = models.DateTimeField(u'更新时间',blank=True, auto_now=True)
    class Meta:
        verbose_name = '资产表'
        verbose_name_plural = "资产表"
    def __unicode__(self):
        return self.ip

class Server(models.Model):
    asset = models.OneToOneField('Asset',verbose_name=u'资产信息')
    created_by_choices = (
        ('auto','Auto'),
        ('manual','Manual'),
    )

    created_by = models.CharField(choices=created_by_choices,max_length=32,default='auto') #auto: auto created,   manual:created manually
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',blank=True,null=True) #for vitural server
    model = models.CharField(u'型号',max_length=128,blank=True,null=True)
    #CPU
    S_cpu = models.ForeignKey('CPU',verbose_name=u'CPU型号',null=True,blank=True)
    #disk
    raid_type = models.CharField(u'raid类型',max_length=256, blank=True,null=True)
    physical_disk_driver = models.CharField(u'硬盘大小(GB)',max_length=128,blank=True,null=True)
    #raid_adaptor = models.ManyToManyField('RaidAdaptor', verbose_name=u'Raid卡',blank=True,null=True)
    #memory
    ram_capacity = models.CharField(u'内存(GB)',blank=True,null=True,max_length=64)

    os_type  = models.CharField(u'操作系统类型',max_length=64, blank=True,null=True)
    # os_distribution =models.CharField(u'发型版本',max_length=64, blank=True,null=True)
    os_release  = models.CharField(u'操作系统版本',max_length=64, blank=True,null=True)

    open_port = models.CharField(u'开放的端口',max_length=128,blank=True,null=True)

    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

    def __unicode__(self):
        return '%s IP:%s' %(self.model,self.asset.ip)

class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    vlan_ip = models.GenericIPAddressField(u'VlanIP',blank=True,null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP',blank=True,null=True)
    sn = models.CharField(u'SN号',max_length=128,unique=True)
    #manufactory = models.CharField(verbose_name=u'制造商',max_length=128,null=True, blank=True)
    model = models.CharField(u'型号',max_length=128,null=True, blank=True )
    port_num = models.SmallIntegerField(u'端口个数',null=True, blank=True )
    device_detail = models.TextField(u'设置详细配置',null=True, blank=True )
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    def __unicode__(self):
        return 'name:%s IP:%s'%(self.asset.name,self.asset.Extranet_ip)
    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"

class CPU(models.Model):

    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPU型号', max_length=128,blank=True)
    cpu_count = models.SmallIntegerField(u'物理cpu个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注', null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"
    def __unicode__(self):
        return '%s*%s'%(self.cpu_model,self.cpu_count)

class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    slot = models.CharField(u'插槽位',max_length=64)
    manufactory = models.CharField(u'制造商', max_length=64,blank=True,null=True)
    model = models.CharField(u'磁盘型号', max_length=128,blank=True,null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64,choices=disk_iface_choice,default='SAS')
    memo = models.TextField(u'备注', blank=True,null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)

    auto_create_fields = ['sn','slot','manufactory','model','capacity','iface_type']
    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"
    def __unicode__(self):
        return '%s:slot:%s capacity:%s' % (self.asset.name,self.slot,self.capacity)


class Manufactory(models.Model):
    name = models.CharField(u'厂商名称',max_length=64,blank=True,null=True)
    manufactory = models.CharField(u'厂商',max_length=64, unique=True)
    support_num = models.CharField(u'支持电话',max_length=30,blank=True,null=True)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)
    def __unicode__(self):
        return self.manufactory
    class Meta:
        verbose_name = '设备厂商'
        verbose_name_plural = "设备厂商"

class BusinessUnit(models.Model):
    # parent_unit = models.ForeignKey('self',related_name='parent_level',blank=True,null=True)
    name = models.CharField(u'业务线',max_length=64, unique=True)
    #contact = models.ForeignKey('UserProfile',default=None)
    asset_count = models.IntegerField(u'资产数量',default=0)
    memo = models.CharField(u'备注',max_length=64, blank=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = "业务线"

class IDC(models.Model):
    name = models.CharField(u'机房名称',max_length=64,unique=True)

    bandwidth = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name=u'机房带宽')
    operator = models.CharField(max_length=32, blank=True, default='', null=True, verbose_name=u"运营商")
    linkman = models.CharField(max_length=16, blank=True, null=True, default='', verbose_name=u'联系人')
    phone = models.CharField(max_length=32, blank=True, null=True, default='', verbose_name=u'联系电话')
    address = models.CharField(max_length=128, blank=True, null=True, default='', verbose_name=u"机房地址")
    network = models.TextField(blank=True, null=True, default='', verbose_name=u"IP地址段")
    date_added = models.DateField(auto_now=True, null=True)
    memo = models.CharField(u'备注',max_length=128,blank=True,null=True)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = '机房'
        verbose_name_plural = "机房"


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(u"姓名",max_length=32)
    Department = models.CharField(u"部门",max_length=32)
    def __unicode__(self):
        return '%s-%s'%(self.name,self.user.username)
    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = "用户信息"
