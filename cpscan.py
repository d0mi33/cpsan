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

    # Step 2: Run nmap -sCV scan on open ports
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

        # Step 3: Identify HTTP and HTTPS services from the nmap detailed scan
        print("Identifying HTTP and HTTPS services...")
        http_ports = []
        https_ports = []
        for line in nmap_detailed_output.splitlines():
            if "/tcp" in line and "open" in line:
                parts = line.split()
                if len(parts) >= 3:
                    port_part = parts[0]
                    port = port_part.split('/')[0]
                    service = parts[2].lower()
                    if service == 'http':
                        http_ports.append(port)
                    elif service in ['ssl/http', 'https']:
                        https_ports.append(port)

        print(f"HTTP ports: {http_ports}")
        print(f"HTTPS ports: {https_ports}")

        # Step 4: Run subdomain enumeration for each HTTP and HTTPS service port
        if http_ports or https_ports:
            # Handle HTTP ports
            for http_port in http_ports:
                print_animation()
                print(f"\nRunning subdirectory scan on HTTP port {http_port}...")
                feroxbuster_cmd = f"feroxbuster -u http://{ip}:{http_port} -C 400,404,403,503"
                feroxbuster_output = run_command(feroxbuster_cmd)

                # Save feroxbuster output
                feroxbuster_file = os.path.join(output_dir, f"subdomain_enum_http_{http_port}.txt")
                with open(feroxbuster_file, "w") as f:
                    f.write(feroxbuster_output)

                print(f"Subdirectory scan results for HTTP port {http_port} saved to {feroxbuster_file}")

            # Handle HTTPS ports
            for https_port in https_ports:
                print_animation()
                print(f"\nRunning subdirectory scan on HTTPS port {https_port}...")
                feroxbuster_cmd = f"feroxbuster -u https://{ip}:{https_port} -k -C 400,404,403,503 -n"
                feroxbuster_output = run_command(feroxbuster_cmd)

                # Save feroxbuster output
                feroxbuster_file = os.path.join(output_dir, f"subdomain_enum_https_{https_port}.txt")
                with open(feroxbuster_file, "w") as f:
                    f.write(feroxbuster_output)

                print(f"Subdirectory scan results for HTTPS port {https_port} saved to {feroxbuster_file}")
        else:
            print("No HTTP or HTTPS services found. Skipping subdirectory scans.")
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
