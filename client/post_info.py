#!/usr/bin/python
# -*- coding=utf-8 -*-
import get_info
import requests,json
server_ip = "192.168.2.200"
agent_ip = ""
#获取CPU
cpu = get_info.cpu()

#获取总内存
mem_total =  get_info.mem_total()

#硬盘总大小

disk_total = get_info.disk_space()

#系统信息
os_type = get_info.os_type()
os_version = get_info.os_version()

#服务器开放端口
open_port = get_info.open_port()

#服务器型号
device_model = get_info.device_model()

#生产厂商
device_manufacturer = get_info.device_manufacturer()

#SN序列号
device_serial = get_info.device_serial()


def html(url,data):
    headers = { "Content-Type":"application/x-www-form-urlencoded",
                    "Accept-Encoding":"gzip, deflate",
                    "Connection": "close",
                    "User-Agent":"iso 9.0"
                    }
    try:
        html = requests.post(url,data=data,headers=headers)
    except:
        pass
    return html
#add asset
url = "http://%s:8000/api/asset_add"%server_ip
data = {'device_serial':device_serial,"device_manufacturer":device_manufacturer}
html(url,data)

#add cpu
url = "http://%s:8000/api/asset_cpu"%server_ip
html(url,cpu)


#add_server
server_data = {"ip":agent_ip,"mem_total":mem_total,
               "disk_total":disk_total,"os_type":os_type,
               "os_version":os_version,"open_port":open_port,"device_model":device_model}

url = "http://%s:8000/api/asset_server"%server_ip
json=json.dumps(server_data)
html(url,json)
