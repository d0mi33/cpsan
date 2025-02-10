# CP Scan - Quick and Efficient Pentesting Enum Script 🚀  

CP Scan was created with pentesting in mind. It quickly identifies open ports, allowing you to start enumeration while a full scan runs in the background. The script generates clean output files and even performs subdirectory enumeration with **Feroxbuster** using its default wordlist (which you can change).  

## Features  
- **Fast port scanning**: Identifies open ports quickly.  
- **Detailed enumeration**: Runs a deep service scan on discovered ports.  
- **Subdirectory enumeration**: Uses Feroxbuster for HTTP services.  
- **Clean output files**: Saves results neatly for later analysis.  
- **Includes UDP scan**: Scans the top 100 UDP ports for additional attack surface.  

## Installation  
```bash
git clone https://github.com/<your-username>/cp_scan.git  
cd cp_scan  
chmod +x cp_scan.py  
```

## Run the script  
```bash
python3 cp_scan.py <TARGET_IP>
```

## Add the script globally (optional)  
You can run `cp_scan` from anywhere by adding it to `/usr/local/bin`:  
```bash
sudo cp cp_scan.py /usr/local/bin/cp_scan  
sudo chmod +x /usr/local/bin/cp_scan  
```
Now you can run:  
```bash
cp_scan <TARGET_IP>
```

## Dependencies  
Ensure you have the following installed:  
```bash
sudo apt install nmap  
sudo apt install feroxbuster  
```

## Example Usage  
```bash
cp_scan 192.168.1.1
```
- Performs an **initial fast scan** to identify open ports.  
- Runs a **detailed service scan** on discovered ports.  
- Checks for **HTTP services** and **runs Feroxbuster** for directory enumeration.  
- Finally, performs a **UDP scan** on the top 100 ports.  

## Output Files  
Results are saved in a folder named `output_<TARGET_IP>`:  
```
output_192.168.1.1/
│── nmap_all_ports.txt
│── nmap_detailed_scan.txt
│── subdomain_enum_port_80.txt (if HTTP found)
│── udp_scan.txt
```

## Disclaimer  
This tool is intended for **legal** penetration testing and research **only**. **Do not use** it on unauthorized systems.  

---
⭐ **Star this repo if you find it useful!** 🚀  
