import requests


# Cisco DevNet Sandbox Details
BASE_URL = "https://sandboxdnac.cisco.com"
USERNAME = "devnetuser"
PASSWORD = "Cisco123!"

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

def get_auth_token():
    """Obtain authentication token from Cisco DNA Center API."""
    url = f"{BASE_URL}/dna/system/api/v1/auth/token"
    
    response = requests.post(url, auth=(USERNAME, PASSWORD), verify=False)
    
    if response.status_code == 200:
        token = response.json()["Token"]
        print("✅ Authentication Successful!")
        return token
    else:
        print(f"❌ Authentication Failed: {response.status_code} - {response.text}")
        return None

def get_devices(token):
    """Fetch network devices from Cisco DNA Center API."""
    url = f"{BASE_URL}/dna/intent/api/v1/network-device"
    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        devices = response.json().get("response", [])
        
        if not devices:
            print("❌ No devices found.")
            return

        print("\n📌 Network Devices:")
        for device in devices:
            hostname = device.get("hostname", "Unknown")
            mgmt_ip = device.get("managementIpAddress", "Unknown")
            device_type = device.get("type", device.get("platformId", "Unknown"))

            print(f"🔹 Hostname: {hostname}")
            print(f"🌐 Management IP: {mgmt_ip}")
            print(f"🔧 Device Type: {device_type}")
            print("-" * 50)

    else:
        print(f"❌ Failed to retrieve devices: {response.status_code} - {response.text}")

# Run authentication and fetch devices
token = get_auth_token()
if token:
    get_devices(token)

