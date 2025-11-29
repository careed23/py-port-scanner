import threading
import sys
import json
from datetime import datetime
from queue import Queue

# Configuration
target = ""
queue = Queue()
open_ports = []

def port_scan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            return True
        s.close()
    except:
        pass
    return False

def worker():
    while not queue.empty():
        port = queue.get()
        if port_scan(port):
            # Resolve service name (e.g., 80 -> http) if possible
            try:
                service = socket.getservbyport(port, 'tcp')
            except:
                service = "Unknown"
            
            print(f"[+] Port {port} is OPEN ({service})")
            
            # Add to our list for the database
            open_ports.append({
                "port": port,
                "service": service,
                "status": "OPEN",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        queue.task_done()

def run_scanner(target_ip, start_port=1, end_port=1024):
    global target
    target = target_ip
    
    print(f"Scanning target: {target}...")
    
    for port in range(start_port, end_port + 1):
        queue.put(port)

    thread_list = []
    for _ in range(100):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        
    for thread in thread_list:
        thread.start()
        
    for thread in thread_list:
        thread.join()
        
    # --- SAVE TO DATABASE (JSON) ---
    print("Saving results to database...")
    data = {
        "target": target,
        "scan_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": sorted(open_ports, key=lambda x: x['port'])
    }
    
    with open("scan_results.json", "w") as f:
        json.dump(data, f, indent=4)
        
    print("✅ Scan Complete. Data saved to 'scan_results.json'")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        target = sys.argv[1]
        run_scanner(target)
    else:
        print("Usage: python3 scanner.py <ip_address>")
