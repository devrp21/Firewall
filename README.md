## **🛡️ Custom Firewall & Packet Sniffer**
A simple Python-based **firewall and packet sniffer** using **WinDivert** that allows you to:  
✅ **Block specific IPs**  
✅ **Block specific ports** (e.g., HTTP, HTTPS, etc.)  
✅ **Block websites** (by resolving them to IP addresses)  
✅ **Monitor network traffic**  

---

## **🚀 Features**
✔ **Customizable Filtering** – Choose which IPs, ports, or websites to block  
✔ **Multiple Input Support** – Enter values as **comma-separated lists**  
✔ **Multithreading** – Improves performance and reduces packet drops  
✔ **Graceful Exit** – Press `Ctrl+C` to stop the firewall cleanly  

---

## **⚙️ Requirements**
### **🔹 Install Dependencies**
1. Install **Python 3.9+** (Recommended)
2. Install required modules:
   ```bash
   pip install pydivert
   ```
3. **Download and Install WinDivert**:  
   - Get it from: [WinDivert Download](https://reqrypt.org/windivert.html)  
   - Extract the files  
   - Place `WinDivert64.sys` and `WinDivert64.dll` in the same directory as your script  

---

## **📝 How to Use**
1. **Run the script**:  
   ```bash
   python firewall.py
   ```
2. **Choose what to block**  
   - Enter **IP addresses** (comma-separated)  
   - Enter **Ports** (comma-separated, e.g., `80,443,22`)  
   - Enter **Websites** (comma-separated, e.g., `example.com, google.com`)  
3. The firewall will now **monitor and block** selected IPs, ports, and websites.

### **🎯 Example Input**
```
Enter IP addresses to block (comma-separated, leave empty to skip): 192.168.1.100, 192.168.1.101
Enter Ports to block (comma-separated, leave empty to skip): 80, 443
Enter Websites to block (comma-separated, leave empty to skip): facebook.com, youtube.com
```
**Output:**  
```
Blocking facebook.com (157.240.22.35)
Blocking youtube.com (142.250.180.206)
Active Filter: (ip.DstAddr == 192.168.1.100 or ip.DstAddr == 192.168.1.101 or tcp.DstPort == 80 or tcp.DstPort == 443)
Blocked: 192.168.1.50:54123 -> 142.250.180.206:443 (Hostname: youtube.com)
Blocked: 192.168.1.50:54124 -> 157.240.22.35:443 (Hostname: facebook.com)
```

---

## **❌ How to Stop**
Press `Ctrl+C` to **exit safely**.

---

## **📌 Notes**
- Requires **Admin Privileges** to run.  
- Works only on **Windows** (since it uses `WinDivert`).  
- **Ensure WinDivert is correctly installed**; otherwise, the script won't work.  
- If **firewall rules seem slow**, try running the script **as Administrator**.

---

## **📜 License**
MIT License – Feel free to modify and use!  

---

