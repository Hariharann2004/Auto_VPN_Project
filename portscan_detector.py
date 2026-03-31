from scapy.all import sniff, TCP, IP
import logging
import time
from collections import defaultdict

_portscan_threat_score = 0.0
_syn_tracker = defaultdict(list)

PORT_THRESHOLD = 10
TIME_WINDOW = 5


def get_portscan_threat_score():
    return _portscan_threat_score


def detect_port_scan(packet):
    global _portscan_threat_score

    if packet.haslayer(TCP) and packet.haslayer(IP):
        if packet[TCP].flags == "S":
            src_ip = packet[IP].src
            now = time.time()

            _syn_tracker[src_ip].append((packet[TCP].dport, now))
            _syn_tracker[src_ip] = [
                (p, t) for p, t in _syn_tracker[src_ip]
                if now - t <= TIME_WINDOW
            ]

            ports = {p for p, _ in _syn_tracker[src_ip]}

            if len(ports) >= PORT_THRESHOLD:
                _portscan_threat_score = min(1.0, _portscan_threat_score + 0.3)
                logging.warning(
                    f"PORT SCAN DETECTED | Source IP: {src_ip}"
                )
                print(f"[PORTSCAN] Scan detected from {src_ip}")
                _syn_tracker[src_ip].clear()


def start_portscan_monitor():
    print("[PORTSCAN] Monitoring started...")
    logging.info("Port scan monitoring started")
    sniff(filter="tcp", prn=detect_port_scan, store=False)
