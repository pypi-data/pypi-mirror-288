import subprocess
import re

class WiFiManager:
    def __init__(self, interface='wlan0'):
        """
        Initializes the WiFiManager with the specified network interface.
        """
        self.interface = interface

    def scan_networks(self):
        """
        Scans for available WiFi networks using iwctl.
        """
        try:
            subprocess.run(
                ["iwctl", "station", self.interface, "scan"], capture_output=True, check=True
            )
            print("Network scan initiated.")
        except subprocess.CalledProcessError as e:
            print(f"Error scanning networks: {e}")
        except Exception as e:
            print(f"Unexpected error scanning networks: {e}")

    def get_ssids(self):
        """
        Retrieves a list of SSIDs from the network scan results.
        
        Returns:
            list: A list of SSIDs.
        """
        try:
            result = subprocess.run(
                ["iwctl", "station", self.interface, "get-networks"],
                capture_output=True,
                text=True,
            )
            scan_result = result.stdout

            # Remove ANSI escape sequences
            cleaned_result = re.sub(r"\x1B\[[0-9;]*[a-zA-Z]", "", scan_result)

            # Process the result to extract and clean SSIDs
            ssids = []
            for line in cleaned_result.splitlines()[4:-1]:  # Skip the header and last line
                line = re.sub(r"^\s*[>]*\s*", "", line)  # Remove leading spaces and '>'
                ssid = re.sub(
                    r"\s+(psk|open|8021x).*", "", line
                ).strip()  # Remove security type and trailing spaces
                if ssid:
                    ssids.append(ssid)

            return ssids
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving networks: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error retrieving networks: {e}")
            return []

    def connect_to_network(self, ssid, password):
        """
        Connects to a WiFi network with the given SSID and password.

        Args:
            ssid (str): The SSID of the network.
            password (str): The password for the network.
        
        Returns:
            bool: True if connected successfully, False otherwise.
        """
        try:
            result = subprocess.run(
                [
                    "iwctl",
                    "--passphrase",
                    password,
                    "station",
                    self.interface,
                    "connect",
                    ssid,
                ],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print(f"Connected to: {ssid}")
                return True
            else:
                print("Error connecting to network. Check SSID and password.")
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to network: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error connecting to network: {e}")
            return False

    def disconnect(self):
        """
        Disconnects from the current WiFi network.
        
        Returns:
            bool: True if disconnected successfully, False otherwise.
        """
        try:
            result = subprocess.run(
                ["iwctl", "station", self.interface, "disconnect"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print(f"Disconnected from: {self.interface}")
                return True
            else:
                print("Error disconnecting from network.")
                return False
        except subprocess.CalledProcessError as e:
            print(f"Error disconnecting from network: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error disconnecting from network: {e}")
            return False

    def check_iwd_installed(self):
        """
        Checks if the iwd (iNet Wireless Daemon) is installed.
        
        Returns:
            bool: True if iwd is installed, False otherwise.
        """
        try:
            result = subprocess.run(
                ["which", "iwd"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                print("iwd is installed.")
                return True
            else:
                print("iwd is not installed.")
                return False
        except Exception as e:
            print(f"Unexpected error checking iwd installation: {e}")
            return False

def main():
    manager = WiFiManager()
    if not manager.check_iwd_installed():
        print("Please install iwd using: sudo apt install iwd -y")
        return

    print("Scanning networks...")
    manager.scan_networks()
    ssids = manager.get_ssids()
    print("Available networks:", ssids)

if __name__ == "__main__":
    main()
