import os
import sys
import socket
import win32com
import json
import wmi
import win32com


global hardware
hardware = wmi.WMI()


def get_network_info():
    network = []

    for getNetwork in hardware.Win32_NetworkAdapterConfiguration(IPEnabled=1):
        network.append(
            {
                "MAC": getNetwork.MACAddress,
                "ip": getNetwork.IPAddress
            }
        )
    return network


def get_cpu_info():
    cpu = []
    getCpuInfo = hardware.Win32_Processor()

    for getCpu in getCpuInfo:
        cpu.append(
            {
                "Name": getCpu.Name,
                "Serial Number": getCpu.ProcessorId,
                "CoreNum": getCpu.NumberOfCores,
                "numOfLogicalProcessors": getCpu.NumberOfLogicalProcessors,
                "cpuPercent": getCpu.loadPercentage
            }
        )
    return cpu


def get_disk_info():
    disk = []

    for getDisk in hardware.Win32_DiskDrive():
        disk.append(
            {
                "Serial": hardware.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(),
                "Caption": getDisk.Caption,
                "Size": str(int(float(getDisk.Size)/1024/1024/1024))+"G"
            }
        )
    return disk


print(get_network_info())
print(get_cpu_info())
print(get_disk_info())