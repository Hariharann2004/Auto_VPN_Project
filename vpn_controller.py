import subprocess
import logging

# UPDATE THIS PATH if your .ovpn file is elsewhere
OVPN_CONFIG_PATH = r"C:\Program Files\OpenVPN\config\vpnbook-de20-tcp443.ovpn"

vpn_active = False


def vpn_on():
    global vpn_active

    if vpn_active:
        return

    try:
        subprocess.Popen(
            [
                r"C:\Program Files\OpenVPN\bin\openvpn.exe",
                "--config",
                OVPN_CONFIG_PATH
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        vpn_active = True
        print("[VPN] VPN turned ON")
        logging.info("VPN turned ON")

    except Exception as e:
        logging.error(f"VPN ON failed: {e}")


def vpn_off():
    global vpn_active

    if not vpn_active:
        return

    try:
        subprocess.run(
            ["taskkill", "/F", "/IM", "openvpn.exe"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        vpn_active = False
        print("[VPN] VPN turned OFF")
        logging.info("VPN turned OFF")

    except Exception as e:
        logging.error(f"VPN OFF failed: {e}")
