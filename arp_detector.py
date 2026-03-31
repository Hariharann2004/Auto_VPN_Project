from scapy.all import sniff, ARP
import logging

_arp_threat_score = 0.0
_known_devices = {}


def get_arp_threat_score():
    return _arp_threat_score


def detect_arp_spoof(packet):
    global _arp_threat_score

    if packet.haslayer(ARP) and packet[ARP].op == 2:
        ip = packet[ARP].psrc
        mac = packet[ARP].hwsrc

        if ip in _known_devices:
            if _known_devices[ip] != mac:
                _arp_threat_score = min(1.0, _arp_threat_score + 0.4)
                logging.warning(
                    f"ARP SPOOF DETECTED | IP {ip} MAC changed"
                )
                print(f"[ARP] Spoof detected for IP {ip}")
        else:
            _known_devices[ip] = mac


def start_arp_monitor():
    print("[ARP] Monitoring started...")
    logging.info("ARP monitoring started")
    sniff(filter="arp", prn=detect_arp_spoof, store=False)
