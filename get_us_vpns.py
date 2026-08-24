import os
import urllib.request
import ssl
import csv
import base64

# URL of the VPN Gate public API
VPNGATE_API_URL = "https://www.vpngate.net/api/iphone/"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "us_vpns")

def main():
    print("Fetching free VPN servers from VPN Gate...")
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Configure SSL context to avoid certificate validation issues
    ssl_context = ssl._create_unverified_context()
    
    try:
        req = urllib.request.Request(
            VPNGATE_API_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
            data = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching data from VPN Gate: {e}")
        return

    lines = data.splitlines()
    
    # Parse CSV content
    # VPNGate API starts with comments and metadata, then `#HostName,...`
    # and ends with `*` or a blank line.
    csv_rows = []
    header_found = False
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("*"):
            continue
        if line.startswith("#HostName"):
            header_found = True
            # Strip the leading '#' from the header line
            line = line.lstrip('#')
            csv_rows.append(line)
            continue
        if header_found:
            csv_rows.append(line)
            
    if len(csv_rows) <= 1:
        print("No VPN server records found in the API response.")
        return

    # Read records using csv reader
    reader = csv.DictReader(csv_rows)
    us_servers = []
    
    for row in reader:
        # Filter for United States (US)
        country_short = row.get("CountryShort", "").upper()
        country_long = row.get("CountryLong", "").lower()
        if country_short == "US" or "united states" in country_long:
            # Parse metrics for sorting
            try:
                score = int(row.get("Score", 0))
            except ValueError:
                score = 0
                
            try:
                speed = int(row.get("Speed", 0))
            except ValueError:
                speed = 0
                
            try:
                ping = int(row.get("Ping", 0))
            except ValueError:
                ping = 99999
                
            us_servers.append({
                "HostName": row.get("HostName"),
                "IP": row.get("IP"),
                "Score": score,
                "Ping": ping,
                "Speed": speed,
                "Country": row.get("CountryLong"),
                "ConfigBase64": row.get("OpenVPN_ConfigData_Base64")
            })

    if not us_servers:
        print("No US VPN servers found in the current list.")
        return

    # Sort servers by Score descending, then Speed descending, then Ping ascending
    us_servers.sort(key=lambda s: (-s["Score"], -s["Speed"], s["Ping"]))

    print(f"\nFound {len(us_servers)} US VPN servers. Saving top 5 to '{OUTPUT_DIR}'...\n")
    
    # Clean previous .ovpn files in the directory
    for file in os.listdir(OUTPUT_DIR):
        if file.endswith(".ovpn"):
            try:
                os.remove(os.path.join(OUTPUT_DIR, file))
            except Exception:
                pass

    saved_count = 0
    print(f"{'#':<3} {'IP Address':<16} {'Ping (ms)':<10} {'Speed (Mbps)':<12} {'Score':<10} {'Filename':<30}")
    print("-" * 85)
    
    for idx, s in enumerate(us_servers[:5], start=1):
        if not s["ConfigBase64"]:
            continue
            
        try:
            config_bytes = base64.b64decode(s["ConfigBase64"])
            # Format speed to Mbps
            speed_mbps = s["Speed"] / 1000000.0
            
            # Save file
            filename = f"us_vpn_{s['IP']}_score_{s['Score']}.ovpn"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, "wb") as f:
                f.write(config_bytes)
                
            print(f"{idx:<3} {s['IP']:<16} {s['Ping']:<10} {speed_mbps:<12.2f} {s['Score']:<10} {filename:<30}")
            saved_count += 1
        except Exception as e:
            print(f"Error saving config for {s['IP']}: {e}")

    print(f"\nSuccessfully saved {saved_count} configuration files to {OUTPUT_DIR}")
    print("You can import any of these files into OpenVPN Connect to establish the connection.")

if __name__ == "__main__":
    main()
