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
