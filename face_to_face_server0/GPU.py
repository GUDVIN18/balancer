from pynvml import *
from time import time, sleep


while True:
    nvmlInit()
    handle = nvmlDeviceGetHandleByIndex(0)
    util = nvmlDeviceGetUtilizationRates(handle)
    print(f"GPU Utilization: {util.gpu}%")
    nvmlShutdown()
    sleep(1)