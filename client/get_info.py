#!/usr/bin/python
# -*- coding=utf-8 -*-
import subprocess
import os
import platform

def disk_space():
    disk_dic = {}
    for a in ['/dev/sda','/dev/sdb','/dev/sdc']:
        cmd = "fdisk -l | grep %s: | awk '{print $3}'"%a
        try:
            obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            space = obj.stdout.read()
        except:
            pass
        if not space.strip():
            pass
        else:
            disk_dic[a]=space.strip()
    return disk_dic

def cpu():
    base_cmd = 'cat /proc/cpuinfo'

    raw_data = {
        'cpu_model':"%s | grep 'model name' |head -1 " %base_cmd,
        'cpu_count':"%s | grep 'physical id'| sort| uniq| wc -l" %base_cmd,
        'cpu_core_count':"%s | grep 'cpu cores'| uniq | cut -d: -f2"%base_cmd
    }

    for k, cmd in raw_data.items():
        try:
            cmd_res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE).stdout.read()
            raw_data[k] = cmd_res.strip()
        except ValueError as e:
            print(e)
    data = {
        "cpu_count": raw_data["cpu_count"],
        "cpu_core_count": raw_data["cpu_core_count"]
    }
    cpu_model = raw_data["cpu_model"].split(":")
    if len(cpu_model) >1:
        data["cpu_model"] = cpu_model[1].strip()
    else:
        data["cpu_model"] = -1
    return data



def open_port():
    cmd = "netstat -ntlp | awk '{print $4}' | grep '0.0.0.0'| awk -F: '{print $2}'"
    try:
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        obj = obj.stdout.read().strip().split('\n')
    except:
        pass
    data = ' '.join(obj)
    return data

def mem_total():
    cmd = "grep 'MemTotal' /proc/meminfo | awk '{print $2}'"
    try:
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        obj = int(obj)
    except:
        pass
    return round(obj/1024/1024.00,3)

def os_type():
    return platform.system()

def os_version():
    obj = platform.linux_distribution()
    data = ' '.join(obj)
    return data

def device_model():
    cmd = "dmidecode -t 1 | grep 'Product Name'"
    try:
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        data = obj.split(':')[1].strip()
    except:
        pass
    return data
def device_serial():
    cmd = "dmidecode -t 1 | grep 'Serial Number'"
    try:
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        data = obj.split(':')[1].strip()
    except:
        pass
    return data
def device_manufacturer():
    cmd = "dmidecode -t 1 | grep 'Manufacturer'"
    try:
        obj = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
        data = obj.split(':')[1].strip()
    except:
        pass
    return data

if __name__ == "__main__":
    print "cpu:%s"%cpu()
    print "mem_total:%s"%mem_total()
    print "disk_space:%s"%disk_space()
    print "os_type:%s"%os_type()
    print os_version()
    print "open_port:%s"%open_port()
    print "device_model:%s"%device_model()
    print "device_manufacturer:%s"%device_manufacturer()
    print "device_serial:%s"%device_serial()



