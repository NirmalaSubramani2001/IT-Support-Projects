#!/usr/bin/env python3

import subprocess
import os

# -----------------------------
# 1️⃣ Disk Usage Check
# -----------------------------
def check_disk(threshold=75):
    print("=== Disk Usage Check ===")
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    lines = result.stdout.split("\n")
    for line in lines[1:]:
        if line:
            parts = line.split()
            filesystem, size, used, avail, use_perc, mount = parts
            usage = int(use_perc.strip('%'))
            if usage > threshold:
                print(f"⚠️ ALERT: {mount} usage at {use_perc}")
            else:
                print(f"{mount} usage OK: {use_perc}")
    print()

# -----------------------------
# 2️⃣ Service Status Check
# -----------------------------
def check_service(service_name):
    print(f"=== Checking Service: {service_name} ===")
    result = subprocess.run(["systemctl", "is-active", service_name], capture_output=True, text=True)
    status = result.stdout.strip()
    if status == "active":
        print(f"✅ {service_name} is running")
    else:
        print(f"⚠️ {service_name} is NOT running")
    print()

# -----------------------------
# 3️⃣ Parse Logs for Errors
# -----------------------------
def check_logs(log_file="/var/log/syslog", keyword="error"):
    print(f"=== Checking Logs: {log_file} for '{keyword}' ===")
    if not os.path.exists(log_file):
        print(f"Log file {log_file} does not exist!")
        return
    with open(log_file, "r") as f:
        for line in f:
            if keyword.lower() in line.lower():
                print(f"⚠️ {line.strip()}")
    print()

# -----------------------------
# Main Function
# -----------------------------
if __name__ == "__main__":
    check_disk(threshold=75)
    check_service("ssh")
    check_service("nginx")
    check_logs("/var/log/syslog", "error")
