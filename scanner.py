import socket
import threading
import sys
from datetime import datetime
from queue import Queue

# Configuration
target = ""
queue = Queue()
open_ports = []

def port_scan(port):
    """
    Tries to connect to a specific port. 
    If successful, returns True.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1) # Don't wait forever
        result = s.connect_ex((target, port))
        if result == 0:
            return True
        s.close()
    except:
        pass
    return False

def worker():
    """
    Worker thread that pulls ports from the queue and scans them.
    """
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            print(f"[+] Port {port} is OPEN")
            open_ports.append(port)
        queue.task_done()

def run_scanner(target_ip, start_port=1, end_port=1024):
    global target
    target = target_ip
    
    print(f"Scanning target: {target}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    # 1. Fill the queue with ports
    for port in range(start_port, end_port + 1):
        queue.put(port)

    # 2. Create threads (The Speed Boost)
    # We create 100 'workers' to do the job at the same time
    thread_list = []
    for _ in range(100):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        
    # 3. Start threads
    for thread in thread_list:
        thread.start()
        
    # 4. Wait for all threads to finish
    for thread in thread_list:
        thread.join()
        
    print("-" * 50)
    print(f"Scan completed. Open ports: {sorted(open_ports)}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        target = sys.argv[1]
        run_scanner(target)
    else:
        print("Syntax Error! Usage: python3 scanner.py <ip_address>")
