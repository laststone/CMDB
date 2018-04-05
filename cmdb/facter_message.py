#!/usr/bin/env python
# coding=utf-8  
import salt.client


def get_all_host_facter_message():

    ###salt调用  
    local = salt.client.LocalClient()
    
    ###获取grains，disk信息  
    grains = local.cmd('*', 'grains.items')
    diskusage = local.cmd('*', 'disk.usage')
    
    #最终要返回的json字典
    all_host_facter_message={}
    
    #for循环遍历每台minion获取其主机信息
    for i in grains.keys():
        #获取salt客户端的ID
        salt_id=grains[i]['id']
        #获取直接能获取到的信息
        name=grains[i]['fqdn']
        sn=grains[i]['serialnumber']
        os=grains[i]['os'] + ' ' + grains[i]['osrelease']
        mem=str(grains[i]['mem_total'] / 1024 + 1)+'GB'
        cpu=grains[i]['cpu_model']
        idc=''
        role=''
        status=''
        admin=''
        memo=''
        #获取内/外网IP(需优化)
        if len(grains[i]['ip4_interfaces']) >= 2:
            public_ip=grains[i]['ip4_interfaces'].values()[1][0]
            if len(grains[i]['ip4_interfaces'].values()[1]) >=2:
                private_ip=grains[i]['ip4_interfaces'].values()[1][1]
            else:
                private_ip='None'
        #获取MAC地址(需优化)
        mac=grains[i]['hwaddr_interfaces'].values()[1]
        #获取磁盘总容量
        if "/" not in diskusage[i]:
            disk_used = " "
            disk_capacity = " "
        else:
            disk_used = float(diskusage[i]["/"]["1K-blocks"])/1048576
            disk_capacity = diskusage[i]["/"]["capacity"]
        if "/data" not in diskusage[i]:
            disk_data_used = " "
            disk_data_capacity = " "
        else:
            disk_data_used = float(diskusage[i]["/data"]["1K-blocks"])/1048576
            disk_data_capacity = diskusage[i]["/data"]["capacity"]
        if "/data1" not in diskusage[i]:
            disk_data1_used = " "
            disk_data1_capacity = " "
        else:
            disk_data1_used = float(diskusage[i]["/data"]["1K-blocks"])/1048576
            disk_data1_capacity = diskusage[i]["/data"]["capacity"]
        #计算总磁盘容量
        disk=0
        for v in diskusage[i].values():
            disk=disk+int(v['1K-blocks'])
        disk=str(round(disk/1024./1024.,2))+'GB'
    
        #构造json数据返回,即 {salt_id:{name:xx,sn:yy,os:zz,...}}
        data={}
        data['name']=name
        data['sn']=sn
        data['public_ip']=public_ip
        data['private_ip']=private_ip
        data['mac']=mac
        data['os']=os
        data['mem']=mem
        data['cpu']=cpu
        data['disk']=disk
        data['idc']=''
        data['role']=''
        data['status']=''
        data['admin']=''
        data['memo']=''
    
        #测试构造data字典是否成功
        #for k,v in data.items():
        #    print k,'===',v
    
        #将该minion的数据存入data字典,并将该字典作为一个元素存入all_host_facter_message这个大字典
        all_host_facter_message[salt_id]=data
    
    #测试最终要返回的数据是否正确  
    #for k,v in all_host_facter_message.items():
    #     print k,'===',v

    #最后返回构造的大字典数据
    return all_host_facter_message

