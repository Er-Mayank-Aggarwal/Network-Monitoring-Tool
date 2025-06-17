import nmap
import socket
import os
import csv
import time
from datetime import datetime
import subprocess


scanner = nmap.PortScanner()
subnet = 'enter your subnet id'  # e.g., '192.168.1.0/24'
csv_file = "network_log.csv"

devices = {}

# CSV headers
csv_headers = ["Hostname", "IP Address", "MAC Address", "IP Added Time", "Status", "Response Time (ms)", "Offline At"]

# Create CSV if not exists
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_headers)

def ping_host(ip):
    try:
        if os.name == 'nt':
            output = subprocess.check_output(['ping', '-n', '1', '-w', '1000', ip], stderr=subprocess.STDOUT)
        else:
            output = subprocess.check_output(['ping', '-c', '1', '-W', '1', ip], stderr=subprocess.STDOUT)

        output = output.decode()
        if "TTL" in output or "ttl" in output:
            if "time=" in output:
                time_ms = output.split("time=")[1].split("ms")[0].strip()
                return "Connected", float(time_ms)
            else:
                return "Connected", None
        else:
            return "Failed", None
    except Exception:
        return "Failed", None

print("📡 Monitoring started... Press Ctrl+C to stop.")

try:
    while True:
        scanner.scan(hosts=subnet, arguments='-sn -R')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        active_ips = set()

        for host in scanner.all_hosts():
            ip = host
            mac = scanner[host]['addresses'].get('mac', 'N/A')

            try:
                hostname = scanner[host].hostname()
                if not hostname:
                    hostname = socket.gethostbyaddr(ip)[0]
            except:
                hostname = "N/A"

            status, response_time = ping_host(ip)
            active_ips.add(ip)

            if ip not in devices:
                devices[ip] = {
                    "hostname": hostname,
                    "ip": ip,
                    "mac": mac,
                    "ip_added_time": current_time,
                    "status": status,
                    "response_time": response_time,
                    "offline_at": ""
                }

                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        hostname, ip, mac, current_time, status,
                        response_time if response_time is not None else "N/A", ""
                    ])

            else:
                if devices[ip]["status"] != status:
                    devices[ip]["status"] = status
                    devices[ip]["response_time"] = response_time

                    if status == "Failed":
                        devices[ip]["offline_at"] = current_time
                    else:
                        devices[ip]["offline_at"] = ""

                    with open(csv_file, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            hostname, ip, mac,
                            devices[ip]["ip_added_time"], status,
                            response_time if response_time is not None else "N/A",
                            devices[ip]["offline_at"]
                        ])

        for ip, info in devices.items():
            if ip not in active_ips and info["status"] == "Connected":
                devices[ip]["status"] = "Failed"
                devices[ip]["offline_at"] = current_time

                with open(csv_file, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        info["hostname"], ip, info["mac"],
                        info["ip_added_time"], "Failed", "N/A", current_time
                    ])

        time.sleep(10)

except KeyboardInterrupt:
    print("\n🛑 Monitoring stopped.")
