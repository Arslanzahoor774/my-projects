# import platform
# import os
# import psutil

# def get_system_information():
#     system_info = {
#         'System': platform.system(),
#         'Node Name': platform.node(),
#         'Release': platform.release(),
#         'Version': platform.version(),
#         'Machine': platform.machine(),
#         'Processor': platform.processor(),
#         'CPU Cores': psutil.cpu_count(logical=False),
#         'Logical CPUs': psutil.cpu_count(logical=True),
#         'RAM (MB)': round(psutil.virtual_memory().total / (1024 ** 2)),
#         'Disk Space (GB)': round(psutil.disk_usage('/').total / (1024 ** 3)),
#     }

#     return system_info

# def write_to_file(data, filename='system_info.txt'):
#     with open(filename, 'w') as file:
#         for key, value in data.items():
#             file.write(f'{key}: {value}\n')

# if __name__ == "__main__":
#     system_info = get_system_information()
#     write_to_file(system_info)
#     print("System information written to system_info.txt.")
#BREAK
# import platform
# import psutil

# def get_system_information():
#     system_info = {}

#     # Basic Information
#     system_info['System'] = platform.system()
#     system_info['Node Name'] = platform.node()
#     system_info['Platform'] = platform.platform()
#     system_info['Processor'] = platform.processor()

#     # Memory Information
#     memory = psutil.virtual_memory()
#     system_info['Total Memory'] = f"{memory.total / (1024 ** 3):.2f} GB"
#     system_info['Available Memory'] = f"{memory.available / (1024 ** 3):.2f} GB"

#     # Disk Information
#     try:
#         partitions = psutil.disk_partitions()
#         for partition in partitions:
#             usage = psutil.disk_usage(partition.mountpoint)
#             system_info[f'{partition.device} Total Disk Space'] = f"{usage.total / (1024 ** 3):.2f} GB"
#             system_info[f'{partition.device} Used Disk Space'] = f"{usage.used / (1024 ** 3):.2f} GB"
#     except PermissionError as e:
#         print(f"Error getting disk usage: {e}")

#     return system_info

# def format_system_information(system_info):
#     formatted_info = "System Information:\n\n"
#     for key, value in system_info.items():
#         formatted_info += f"{key}: {value}\n"

#     return formatted_info

# if __name__ == "__main__":
#     system_info = get_system_information()
#     formatted_info = format_system_information(system_info)

#     with open("system_information.txt", "w") as file:
#         file.write(formatted_info)

#     print("System information has been saved to 'system_information.txt'.")
#BREAK
# import psutil

# def get_system_info():
#   """
#   Gathers basic system information using psutil library.
#   """
#   system_info = {
#     "OS": psutil.platform(),
#     "CPU": psutil.cpu_count(),
#     "RAM": psutil.virtual_memory().total / 1024**3,
#     "Disk": psutil.disk_usage('/')[0] / 1024**3,
#   }
#   return system_info

# def format_info(info):
#   """
#   Formats the system information as a string.
#   """
#   output = ""
#   for key, value in info.items():
#     output += f"{key}: {value}\n"
#   return output

# def main():
#   info = get_system_info()
#   formatted_info = format_info(info)
#   print(formatted_info)

# if __name__ == "__main__":
#   main()
#AGAIN BREAK

# import psutil
# import platform
# from datetime import datetime
# import cpuinfo
# import socket
# import uuid
# import re


# def get_size(bytes, suffix="B"):
#     """
#     Scale bytes to its proper format
#     e.g:
#         1253656 => '1.20MB'
#         1253656678 => '1.17GB'
#     """
#     factor = 1024
#     for unit in ["", "K", "M", "G", "T", "P"]:
#         if bytes < factor:
#             return f"{bytes:.2f}{unit}{suffix}"
#         bytes /= factor

# def System_information():
#     print("="*40, "System Information", "="*40)
#     uname = platform.uname()
#     print(f"System: {uname.system}")
#     print(f"Node Name: {uname.node}")
#     print(f"Release: {uname.release}")
#     print(f"Version: {uname.version}")
#     print(f"Machine: {uname.machine}")
#     print(f"Processor: {uname.processor}")
#     print(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}")
#     print(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}")
#     print(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")


#     # Boot Time
#     print("="*40, "Boot Time", "="*40)
#     boot_time_timestamp = psutil.boot_time()
#     bt = datetime.fromtimestamp(boot_time_timestamp)
#     print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")


#     # print CPU information
#     print("="*40, "CPU Info", "="*40)
#     # number of cores
#     print("Physical cores:", psutil.cpu_count(logical=False))
#     print("Total cores:", psutil.cpu_count(logical=True))
#     # CPU frequencies
#     cpufreq = psutil.cpu_freq()
#     print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
#     print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
#     print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
#     # CPU usage
#     print("CPU Usage Per Core:")
#     for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
#         print(f"Core {i}: {percentage}%")
#     print(f"Total CPU Usage: {psutil.cpu_percent()}%")


#     # Memory Information
#     print("="*40, "Memory Information", "="*40)
#     # get the memory details
#     svmem = psutil.virtual_memory()
#     print(f"Total: {get_size(svmem.total)}")
#     print(f"Available: {get_size(svmem.available)}")
#     print(f"Used: {get_size(svmem.used)}")
#     print(f"Percentage: {svmem.percent}%")



#     print("="*20, "SWAP", "="*20)
#     # get the swap memory details (if exists)
#     swap = psutil.swap_memory()
#     print(f"Total: {get_size(swap.total)}")
#     print(f"Free: {get_size(swap.free)}")
#     print(f"Used: {get_size(swap.used)}")
#     print(f"Percentage: {swap.percent}%")



#     # Disk Information
#     print("="*40, "Disk Information", "="*40)
#     print("Partitions and Usage:")
#     # get all disk partitions
#     partitions = psutil.disk_partitions()
#     for partition in partitions:
#         print(f"=== Device: {partition.device} ===")
#         print(f"  Mountpoint: {partition.mountpoint}")
#         print(f"  File system type: {partition.fstype}")
#         try:
#             partition_usage = psutil.disk_usage(partition.mountpoint)
#         except PermissionError:
#             # this can be catched due to the disk that
#             # isn't ready
#             continue
#         print(f"  Total Size: {get_size(partition_usage.total)}")
#         print(f"  Used: {get_size(partition_usage.used)}")
#         print(f"  Free: {get_size(partition_usage.free)}")
#         print(f"  Percentage: {partition_usage.percent}%")
#     # get IO statistics since boot
#     disk_io = psutil.disk_io_counters()
#     print(f"Total read: {get_size(disk_io.read_bytes)}")
#     print(f"Total write: {get_size(disk_io.write_bytes)}")

#     ## Network information
#     print("="*40, "Network Information", "="*40)
#     ## get all network interfaces (virtual and physical)
#     if_addrs = psutil.net_if_addrs()
#     for interface_name, interface_addresses in if_addrs.items():
#         for address in interface_addresses:
#             print(f"=== Interface: {interface_name} ===")
#             if str(address.family) == 'AddressFamily.AF_INET':
#                 print(f"  IP Address: {address.address}")
#                 print(f"  Netmask: {address.netmask}")
#                 print(f"  Broadcast IP: {address.broadcast}")
#             elif str(address.family) == 'AddressFamily.AF_PACKET':
#                 print(f"  MAC Address: {address.address}")
#                 print(f"  Netmask: {address.netmask}")
#                 print(f"  Broadcast MAC: {address.broadcast}")
#     ##get IO statistics since boot
#     net_io = psutil.net_io_counters()
#     print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
#     print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")


# if __name__ == "__main__":

#     System_information()
#DON BREAK

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


