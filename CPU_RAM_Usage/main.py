import time
import psutil

def display_usage(cpu_usage, memory_usage,bars=50):
    cpu_percent = (cpu_usage / 100.0)
    cpu_bar = ' ' * int(cpu_percent * bars) + '-' * (bars - int(cpu_percent * bars))
    
    memory_percent = (memory_usage / 100.0)
    mem_bar = ' ' * int(memory_percent * bars) + '-' * (bars - int(memory_percent * bars))
    
    
    print(f" CPU Usage | {cpu_bar}| {cpu_usage:.2f} %",end="")
    print(f" Ram Usage: | {mem_bar}| {memory_usage:.2f} %",end="\r")
    
    
while True:
    display_usage(psutil.cpu_percent(),psutil.virtual_memory().percent,30)
    time.sleep(0.5)