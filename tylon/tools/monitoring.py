# tylon/tools/monitoring.py
import psutil
from langchain.tools import tool
import os
import sys

@tool
def get_system_info():
    """Get information about the current system."""
    info = {
        "os": os.name,
        "platform": sys.platform,
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "battery": None,
    }
    
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        if battery:
            info["battery"] = {
                "percent": battery.percent,
                "power_plugged": battery.power_plugged,
                "secsleft": battery.secsleft if battery.secsleft != -1 else None
            }
    
    return info