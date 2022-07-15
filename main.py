import wmi
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Union
import pandas as pd
import json


app = FastAPI()


class GET:

    global hardware

    hardware = wmi.WMI()

    def get_network_info(self):
        network = []

        for getNetwork in hardware.Win32_NetworkAdapterConfiguration(IPEnabled=1):
            network.append(
                {
                    "MAC": getNetwork.MACAddress,
                    "ip": getNetwork.IPAddress
                }
            )
        return network


    def get_cpu_info(self):
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


    def get_disk_info(self):
        disk = []

        for getDisk in hardware.Win32_DiskDrive():
            disk.append(
                {
                    "Serial": hardware.Win32_PhysicalMedia()[0].SerialNumber.lstrip().rstrip(),
                    "Caption": getDisk.Caption,
                    "Size": str(int(float(getDisk.Size) / 1024 / 1024 / 1024)) + "G"
                }
            )
        return disk


@app.get("/")
async def hello_word():
    return "hello word!"


@app.get("/cpu")
async def get_cpu():
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


@app.get("/cnetwork")
async def get_network():
    GET.get_network_info()


@app.get("/disk")
async def get_disk():
    pass


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


data = [{
        "username": "",
        "password": "",
        "email": "",
        "full_name": ""
        }]


dataframC = pd.DataFrame(data)



@app.post("/user/", response_model=UserIn)
async def create_user(user: UserIn):

    dataframC.loc[0, "username"] = user.username
    dataframC.loc[0, "password"] = user.password
    dataframC.loc[0, "email"] = user.email
    dataframC.loc[0, "full_name"] = user.full_name

    print(dataframC)




    print("檔案已生成")

    return user