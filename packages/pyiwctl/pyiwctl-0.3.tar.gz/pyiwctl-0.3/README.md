# pyiwctl

`pyiwctl` is a Python package for managing WiFi connections using `iwctl`.

## Installation

### Prerequisites

Ensure you have `iwd` (iNet Wireless Daemon) installed on your system. You can install it using the following commands:

```bash
- Debian:
sudo apt install iwd -y

- Fedora:
sudo dnf install iwd

- Arch Linux:
sudo pacman -Sy iwd

```

### Python Package

Install the `pyiwctl` package using `pip`:

```bash
pip install pyiwctl
```

## Usage

```python
from pyiwctl import WiFiManager

manager = WiFiManager()
manager.scan_networks()
ssids = manager.get_ssids()
print("Available networks:", ssids)

success = manager.connect_to_network('SSID_NAME', 'PASSWORD')
print("Connection successful:", success)
```