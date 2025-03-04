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


# User input: IPs, Ports, Websites to block
blocked_ips = set()
blocked_ports = set()

# Get IPs
ip_input = input("Enter IP addresses to block (comma-separated, leave empty to skip): ").strip()
if ip_input:
    blocked_ips.update(ip.strip() for ip in ip_input.split(",") if ip.strip())

# Get Ports
port_input = input("Enter Ports to block (comma-separated, leave empty to skip): ").strip()
if port_input:
    try:
        blocked_ports.update(int(port.strip()) for port in port_input.split(",") if port.strip().isdigit())
    except ValueError:
        print("Invalid port detected. Skipping invalid entries.")

# Get Websites
website_input = input("Enter Websites to block (comma-separated, leave empty to skip): ").strip()
if website_input:
    websites = [w.strip() for w in website_input.split(",") if w.strip()]
    for website in websites:
        ip = hostname_to_ip(website)
        if ip:
            print(f"Blocking {website} ({ip})")
            blocked_ips.add(ip)
        else:
            print(f"Invalid website: {website}")

# Create a valid filter string
FILTER = " or ".join([f"ip.DstAddr == {ip}" for ip in blocked_ips])
FILTER += " or " if FILTER else ""  # Add OR if both IPs and Ports exist
FILTER += " or ".join([f"tcp.DstPort == {port}" for port in blocked_ports])

if not FILTER:
    print("No valid filters set. Exiting.")
    sys.exit(0)

FILTER = f"({FILTER})"  # Wrap the filter expression

print(f"Active Filter: {FILTER}")

# Packet queue for threading
packet_queue = queue.Queue()
exit_event = threading.Event()  # Event to handle shutdown


# Function to capture packets
def capture_packets(w):
    try:
        for packet in w:
            if exit_event.is_set():
                break
            packet_queue.put(packet)  # Add packet to queue
    except KeyboardInterrupt:
        pass  # Ignore Ctrl+C interruptions


# Function to process packets
def handle_packets(w):
    try:
        while not exit_event.is_set():
            try:
                packet = packet_queue.get(timeout=1)  # Wait max 1 sec for a packet
            except queue.Empty:
                continue  # No packet, continue loop

            if packet.dst_addr in blocked_ips or packet.dst_port in blocked_ports:
                print(f"Blocked: {packet.src_addr}:{packet.src_port} -> {packet.dst_addr}:{packet.dst_port} "
                      f"(Hostname: {ip_to_hostname(packet.dst_addr)})")
                # Do NOT send the packet to drop it
            else:
                w.send(packet)  # Forward allowed packets

            packet_queue.task_done()  # Mark as processed
    except KeyboardInterrupt:
        pass  # Handle Ctrl+C cleanly


# Handle Ctrl+C to exit gracefully
def signal_handler(sig, frame):
    print("\n[+] Stopping firewall... Please wait.")
    exit_event.set()  # Signal threads to exit
    sys.exit(0)


# Register Ctrl+C signal
signal.signal(signal.SIGINT, signal_handler)

# Start the firewall
with pydivert.WinDivert(FILTER) as w:
    capture_thread = threading.Thread(target=capture_packets, args=(w,), daemon=True)
    handler_thread = threading.Thread(target=handle_packets, args=(w,), daemon=True)

    capture_thread.start()
    handler_thread.start()

    capture_thread.join()
    handler_thread.join()
