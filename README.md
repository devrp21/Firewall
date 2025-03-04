# Firewall & Packet Sniffer

A lightweight Python-based **Firewall & Packet Sniffer** that allows users to block specific websites, IP addresses, and ports using **WinDivert**. The program efficiently captures and filters network packets in real-time with multi-threading for better performance.

## Features 🚀
- **Packet Filtering:** Block websites and specific ports (e.g., HTTP & HTTPS traffic).
- **IP and Hostname Resolution:** Convert hostnames to IPs and vice versa.
- **Multi-threading for Efficiency:** Faster execution with separate threads for capturing and processing packets.
- **Graceful Exit:** Press `Ctrl+C` to stop the program cleanly.

---
## Installation 🛠

### Prerequisites
- **Windows OS** (Required for WinDivert)
- **Python 3.9+** (Recommended for compatibility)
- **WinDivert** (Windows packet capture & modification tool)

### Install Dependencies
1. **Install Python Packages**
   ```bash
   pip install pydivert
   ```
2. **Download WinDivert**
   - Download `WinDivert` from [here](https://reqrypt.org/windivert.html)
   - Extract and copy `WinDivert64.sys` and `WinDivert64.dll` to your project folder.

---
## Usage 📌

1. **Run the Script**
   ```bash
   python firewall.py
   ```
2. **Enter the website to block**
   ```
   Enter the Website you want to block: example.com
   ```
3. **Firewall starts filtering packets in real-time**
   ```
   example.com's IP: 93.184.216.34 will be blocked
   Blocked: 192.168.1.5:52345 -> 93.184.216.34:80 (Hostname: example.com)
   ```
4. **Press `Ctrl+C` to stop the program.**

---
## Troubleshooting & FAQs ❓

### "WinError 87: The parameter is incorrect"
- Ensure **WinDivert is properly installed**.
- Restart your system and try running the script again.

### "Ctrl+C Doesn't Stop the Program"
- The program now handles `Ctrl+C` correctly using a shutdown event.
- Ensure you're running the latest optimized version of the script.

---
## License 📝
This project is **open-source** and licensed under the **MIT License**.

---
## Author ✨
Developed by Dev

For any issues or suggestions, feel free to open an issue or contribute! 🚀


## Screenshot
![image](https://github.com/user-attachments/assets/4de4255c-b2d5-4d1b-9ad5-3289e19b25f9)


