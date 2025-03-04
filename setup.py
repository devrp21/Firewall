import pydivert
import socket
import threading
import queue
import signal
import sys

# Function to resolve hostname to IP
def hostname_to_ip(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None  # Return None if invalid

# Function to resolve IP to hostname
def ip_to_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown Host"

# Define blocked IPs and ports
BLOCKED_IPS = {"192.168.0.102"}  # Default blocked IP
BLOCKED_PORTS = {80, 443}  # Block HTTP and HTTPS traffic

# Ask for website to block
website = input("Enter the Website you want to block: ")
website_ip = hostname_to_ip(website)

if website_ip:
    print(f"{website}'s IP: {website_ip} will be blocked")
    BLOCKED_IPS.add(website_ip)
else:
    print(f"Invalid website: {website}")

# Create a valid filter string
FILTER = "(tcp.DstPort == 80 or tcp.DstPort == 443)"
for ip in BLOCKED_IPS:
    FILTER += f" or ip.DstAddr == {ip}"

# Packet queue for multithreading
packet_queue = queue.Queue()
shutdown_event = threading.Event()  # Used to signal threads to exit


# Function to capture packets
def capture_packets():
    with pydivert.WinDivert(FILTER) as w:
        print("[*] Packet capturing started...")
        for packet in w:
            if shutdown_event.is_set():
                break  # Exit loop when shutdown is signaled
            packet_queue.put(packet)  # Add packet to queue


# Function to process packets
def handle_packets():
    with pydivert.WinDivert(FILTER) as w:
        print("[*] Packet processing started...")
        while not shutdown_event.is_set():
            try:
                packet = packet_queue.get(timeout=1)  # Avoids blocking indefinitely
            except queue.Empty:
                continue  # Skip iteration if queue is empty

            if packet.dst_addr in BLOCKED_IPS or packet.dst_port in BLOCKED_PORTS:
                print(f"Blocked: {packet.src_addr}:{packet.src_port} -> {packet.dst_addr}:{packet.dst_port} "
                      f"(Hostname: {ip_to_hostname(packet.dst_addr)})")
                # Do NOT send the packet to drop it
            else:
                w.send(packet)  # Forward allowed packets

            packet_queue.task_done()  # Mark as done


# Signal handler for Ctrl+C
def signal_handler(sig, frame):
    print("\n[!] Ctrl+C detected. Stopping...")
    shutdown_event.set()  # Notify all threads to exit
    sys.exit(0)  # Exit program

# Attach signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)

# Start threads
capture_thread = threading.Thread(target=capture_packets, daemon=True)
handler_thread = threading.Thread(target=handle_packets, daemon=True)

capture_thread.start()
handler_thread.start()

# Wait for threads to finish
capture_thread.join()
handler_thread.join()
