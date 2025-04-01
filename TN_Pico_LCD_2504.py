import time, subprocess, argparse, os, sys, json

def get_midclt_data(method):
    try:
        midclt_output = subprocess.run(
            ["/usr/bin/midclt", "call", method],
            capture_output=True,
            text=True,
            check=True
        )
        try:
            midclt_parsed = json.loads(midclt_output.stdout)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON response from midclt: {e}")
            sys.exit(1)     
        return midclt_parsed
        
    except subprocess.CalledProcessError as e:
        print("Error: calling midclt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def send_message(serial_port, message):
    try:
        with open(serial_port, "w") as ser:
            ser.write(message + "\n")
            ser.flush()
        time.sleep(8)
    except Exception as e:
        print(f"Error: {e}")

def get_cpu_temperature():
    try:
        output = subprocess.check_output(["sensors"]).decode()
        for line in output.split("\n"):
            if "Core 0" in line:
                return line.split()[2].replace("°C", "")
    except Exception as e:
        print(f"Error: {e}")
    return "N/A"

def get_cpu_temperature():
    try:
        output = subprocess.check_output(["sensors"]).decode()
        for line in output.split("\n"):
            if "Core 0" in line:
                return line.split()[2].replace("°C", "")
    except Exception as e:
        print(f"Error: {e}")
    return "N/A"

def get_cpu_usage_percent():
    try:
        output = subprocess.check_output("top -b -n1 | grep 'Cpu(s)'", shell=True).decode()
        usage = float(output.split('%')[0].split()[-1])
        return round(100 - usage, 2) 
    except Exception as e:
        print(f"Error: {e}")
    return "N/A"

def get_total_ram():
    try:
        output = subprocess.check_output("grep MemTotal /proc/meminfo", shell=True).decode()
        total_kb = int(output.split()[1])
        return round(total_kb / (1024 * 1024), 2)
    except Exception as e:
        print(f"Error: {e}")
    return "N/A" 

def get_pool_status():
    try:
        pools_data = get_midclt_data("pool.query")
    except Exception as e: 
        print(f"Error: {e}")
        
    pools_info = []
    pools_info.append("SECTION:POOL STATUS")
    try:
        for pool in pools_data:
            name = pool.get('name', 'N/A')
            status = pool.get('status', 'N/A')
            healthy = "Healthy" if pool.get('healthy', False) else "Unhealthy"
            size = pool.get('size', 0)
            free = pool.get('free', 0)
            free_percentage = (free / size * 100) if size > 0 else 0     
            pools_info.append(f"{name}:{status}")
            pools_info.append(f"{name}:{healthy}")
            pools_info.append(f"{name}:{free_percentage:.2f}% free")
        return pools_info
    except Exception as e: 
        print(f"Error: {e}")    
    

def get_ixapps_info():
    try:
        ixapps_data = get_midclt_data("app.query")
    except Exception as e: 
        print(f"Error: {e}")
    
    ixapps_info = []
    ixapps_info.append("SECTION:APP STATUS")
    try:    
        for ixapp in ixapps_data:
            name = ixapp.get('name', 'N/A')        
            state = ixapp.get('state', 'N/A') 
            ixapps_info.append(f"{name}:{state}")
            if ixapp.get('upgrade_available'):
                ixapps_info.append(f"{name}:Upgrade avail.")
        return ixapps_info
    except Exception as e: 
        print(f"Error: {e}")   

def main(serial_port):
    while True:
        try:
            # CPU Temperature
            cpu_temp = get_cpu_temperature()
            send_message(serial_port, f"CPU Temp:{cpu_temp} C")

            # CPU Usage
            cpu_usage = get_cpu_usage_percent()
            send_message(serial_port, f"CPU Usage:{cpu_usage}%")

            # Total RAM
            total_ram = get_total_ram()
            send_message(serial_port, f"Total RAM:{total_ram} GB")

            # Used RAM
            ram_used = get_total_ram_used()
            send_message(serial_port, f"RAM Used:{ram_used} GB")
            
            # Pool Status
            pools_info = get_pool_status()
            for pools in pools_info:
                send_message(serial_port, f"{pools}")
                
            # Catalogue App Status
            ixapps_info = get_ixapps_info()
            for ixapp in ixapps_info:
                send_message(serial_port, f"{ixapp}")


        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send TN data to a serial port")
    parser.add_argument("serial_port", type=str, help="Serial port (eg. /dev/ttyACM0)")

    args = parser.parse_args()

    if not os.path.exists(args.serial_port):
        print(f"Error: {args.serial_port} not exists")
        sys.exit(1)

    main(args.serial_port)
