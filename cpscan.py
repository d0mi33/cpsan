#!/usr/bin/env python3
import subprocess
import sys
import os
import time
import warnings

def run_command(command):
    try:
        print(f"Executing command: {command}")  # Debug: Log the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stderr:
            print(f"Error output: {result.stderr}")  # Debug: Log errors
        return result.stdout
    except Exception as e:
        print(f"Error running command: {command}\n{e}")
        sys.exit(1)


def print_animation():
    animation = ["|", "/", "-", "\\"]
    for _ in range(10):
        for frame in animation:
            print(f"\rRunning CP Scan... {frame}", end="", flush=True)
            time.sleep(0.2)
    print("\rScan complete!      ")


def print_ascii_art():
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=SyntaxWarning)
        ascii_art = '''
   ____ ____    ____  ____   ____ ___   _    _ 
  / ___/ ___|  |  _ \\|  _ \\ / ___/ _ \\ | |  | |
 | |   \\___ \\  | |_) | |_) | |  | | | || |  | |
 | |___ ___) | |  __/|  __/| |__| |_| || |__| |
  \\____|____/  |_|   |_|    \\____\\___(_)____(_)

        '''
        print(ascii_art)


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 cp_scan.py <IP>")
        sys.exit(1)

    # Display ASCII art
    print_ascii_art()

    ip = sys.argv[1]
    output_dir = f"output_{ip}"
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Run initial nmap scan for all ports
    print_animation()
    print("\nRunning initial nmap scan for all ports...")
    nmap_all_ports_cmd = f"nmap -p- --min-rate 10000 -T5 -Pn -n {ip}"
    nmap_all_ports_output = run_command(nmap_all_ports_cmd)

    # Save nmap all ports output
    nmap_all_ports_file = os.path.join(output_dir, "nmap_all_ports.txt")
    with open(nmap_all_ports_file, "w") as f:
        f.write(nmap_all_ports_output)

    # Extract open ports
    print("Extracting open ports...")
    open_ports = []
    for line in nmap_all_ports_output.splitlines():
        if "/tcp" in line and "open" in line:
            port = line.split("/")[0]
            open_ports.append(port)

    print(f"Open ports: {open_ports}")

    # Ensure only port numbers in the open_ports list
    open_ports = [port.split()[-1] if "Discovered" in port else port for port in open_ports]

    # Step 2: Run nmap -sC -sV -sT scan on open ports
    if open_ports:
        open_ports_str = ",".join(open_ports)  # Ensure ports are comma-separated
        print_animation()
        print("\nRunning detailed nmap scan on open ports...")
        nmap_detailed_cmd = f"nmap -p{open_ports_str} -Pn -sC -sV -n {ip}"
        nmap_detailed_output = run_command(nmap_detailed_cmd)

        # Save detailed nmap scan output
        nmap_detailed_file = os.path.join(output_dir, "nmap_detailed_scan.txt")
        with open(nmap_detailed_file, "w") as f:
            f.write(nmap_detailed_output)

        print(f"Detailed nmap scan results saved to {nmap_detailed_file}")

        # Step 3: Identify HTTP services from the nmap detailed scan
        print("Identifying HTTP services...")
        http_ports = []
        for line in nmap_detailed_output.splitlines():
            if "http" in line and "/tcp" in line and "open" in line:
                port = line.split("/")[0]
                http_ports.append(port)

        print(f"Ports with HTTP services: {http_ports}")

        # Step 4: Run subdomain enumeration for each HTTP service port
        if http_ports:
            for http_port in http_ports:
                print_animation()
                print(f"\nRunning subdirectory scan on port {http_port}...")
                feroxbuster_cmd = f"feroxbuster -u http://{ip}:{http_port} -C 400,404,403,503 -n"
                feroxbuster_output = run_command(feroxbuster_cmd)

                # Save feroxbuster output
                feroxbuster_file = os.path.join(output_dir, f"subdomain_enum_port_{http_port}.txt")
                with open(feroxbuster_file, "w") as f:
                    f.write(feroxbuster_output)

                print(f"Subdirectory scan results for port {http_port} saved to {feroxbuster_file}")
        else:
            print("No HTTP services found. Skipping subdirectory scans.")
    else:
        print("No open ports found. Skipping detailed nmap scan.")

    # Step 5: Run UDP scan on the top 100 ports
    print_animation()
    print("\nRunning UDP scan on top 100 ports...")
    udp_scan_cmd = f"sudo nmap -Pn -n {ip} -sU --top-ports=100 --reason"
    udp_scan_output = run_command(udp_scan_cmd)

    # Save UDP scan output
    udp_scan_file = os.path.join(output_dir, "nmap_udp_scan.txt")
    with open(udp_scan_file, "w") as f:
        f.write(udp_scan_output)

    print(f"UDP scan results saved to {udp_scan_file}")

if __name__ == "__main__":
    main()
