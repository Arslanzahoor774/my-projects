import tkinter as tk
from tkinter import scrolledtext
import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def show_system_info():
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)

    result_text.insert(tk.END, "="*40 + " System Information " + "="*40 + "\n")
    uname = platform.uname()
    result_text.insert(tk.END, f"System: {uname.system}\n")
    result_text.insert(tk.END, f"Node Name: {uname.node}\n")
    result_text.insert(tk.END, f"Release: {uname.release}\n")
    result_text.insert(tk.END, f"Version: {uname.version}\n")
    result_text.insert(tk.END, f"Machine: {uname.machine}\n")
    result_text.insert(tk.END, f"Processor: {uname.processor}\n")
    result_text.insert(tk.END, f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n")
    result_text.insert(tk.END, f"Ip-Address: {socket.gethostbyname(socket.gethostname())}\n")
    result_text.insert(tk.END, f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n")

    result_text.insert(tk.END, "="*40 + " Boot Time " + "="*40 + "\n")
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    result_text.insert(tk.END, f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")

    result_text.insert(tk.END, "="*40 + " CPU Info " + "="*40 + "\n")
    result_text.insert(tk.END, f"Physical cores: {psutil.cpu_count(logical=False)}\n")
    result_text.insert(tk.END, f"Total cores: {psutil.cpu_count(logical=True)}\n")
    cpufreq = psutil.cpu_freq()
    result_text.insert(tk.END, f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
    result_text.insert(tk.END, f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
    result_text.insert(tk.END, f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
    result_text.insert(tk.END, "CPU Usage Per Core:\n")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        result_text.insert(tk.END, f"Core {i}: {percentage}%\n")
    result_text.insert(tk.END, f"Total CPU Usage: {psutil.cpu_percent()}%\n")

    result_text.insert(tk.END, "="*40 + " Memory Information " + "="*40 + "\n")
    svmem = psutil.virtual_memory()
    result_text.insert(tk.END, f"Total: {get_size(svmem.total)}\n")
    result_text.insert(tk.END, f"Available: {get_size(svmem.available)}\n")
    result_text.insert(tk.END, f"Used: {get_size(svmem.used)}\n")
    result_text.insert(tk.END, f"Percentage: {svmem.percent}%\n")

    result_text.insert(tk.END, "="*20 + " SWAP " + "="*20 + "\n")
    swap = psutil.swap_memory()
    result_text.insert(tk.END, f"Total: {get_size(swap.total)}\n")
    result_text.insert(tk.END, f"Free: {get_size(swap.free)}\n")
    result_text.insert(tk.END, f"Used: {get_size(swap.used)}\n")
    result_text.insert(tk.END, f"Percentage: {swap.percent}%\n")

    result_text.insert(tk.END, "="*40 + " Disk Information " + "="*40 + "\n")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        result_text.insert(tk.END, f"=== Device: {partition.device} ===\n")
        result_text.insert(tk.END, f"  Mountpoint: {partition.mountpoint}\n")
        result_text.insert(tk.END, f"  File system type: {partition.fstype}\n")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        result_text.insert(tk.END, f"  Total Size: {get_size(partition_usage.total)}\n")
        result_text.insert(tk.END, f"  Used: {get_size(partition_usage.used)}\n")
        result_text.insert(tk.END, f"  Free: {get_size(partition_usage.free)}\n")
        result_text.insert(tk.END, f"  Percentage: {partition_usage.percent}%\n")

    disk_io = psutil.disk_io_counters()
    result_text.insert(tk.END, f"Total read: {get_size(disk_io.read_bytes)}\n")
    result_text.insert(tk.END, f"Total write: {get_size(disk_io.write_bytes)}\n")

    result_text.insert(tk.END, "="*40 + " Network Information " + "="*40 + "\n")
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            result_text.insert(tk.END, f"=== Interface: {interface_name} ===\n")
            if str(address.family) == 'AddressFamily.AF_INET':
                result_text.insert(tk.END, f"  IP Address: {address.address}\n")
                result_text.insert(tk.END, f"  Netmask: {address.netmask}\n")
                result_text.insert(tk.END, f"  Broadcast IP: {address.broadcast}\n")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                result_text.insert(tk.END, f"  MAC Address: {address.address}\n")
                result_text.insert(tk.END, f"  Netmask: {address.netmask}\n")
                result_text.insert(tk.END, f"  Broadcast MAC: {address.broadcast}\n")

    result_text.config(state=tk.DISABLED)

# Create the main window
window = tk.Tk()
window.title("System Information")
window.geometry("800x600")

# Create a scrolled text widget to display the results
result_text = scrolledtext.ScrolledText(window, width=100, height=30, wrap=tk.WORD)
result_text.pack(padx=10, pady=10)

# Create a button to trigger the system information retrieval
button = tk.Button(window, text="Show System Information", command=show_system_info)
button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()