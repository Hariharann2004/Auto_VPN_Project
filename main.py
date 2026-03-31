import threading
import time
import logging

from arp_detector import start_arp_monitor, get_arp_threat_score
from portscan_detector import start_portscan_monitor, get_portscan_threat_score
from vpn_controller import vpn_on, vpn_off

# ================= LOGGING SETUP =================
logging.basicConfig(
    filename="auto_vpn.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

print("[SYSTEM] Auto VPN system starting...")
logging.info("SYSTEM STARTED")

# ================= START MONITORS =================
threading.Thread(target=start_arp_monitor, daemon=True).start()
threading.Thread(target=start_portscan_monitor, daemon=True).start()

print("[DECISION] Decision engine started...")
logging.info("Decision engine started")

THREAT_THRESHOLD = 0.7
SAFE_THRESHOLD = 0.3
DECAY_RATE = 0.05

total_threat = 0.0

# ================= DECISION LOOP =================
while True:
    arp_score = get_arp_threat_score()
    portscan_score = get_portscan_threat_score()

    total_threat = min(1.0, arp_score + portscan_score)

    if total_threat >= THREAT_THRESHOLD:
        print(f"[THREAT] HIGH ({total_threat:.2f}) → VPN ON")
        logging.warning(f"High threat level: {total_threat:.2f}")
        vpn_on()

    elif total_threat <= SAFE_THRESHOLD:
        print(f"[THREAT] LOW ({total_threat:.2f}) → VPN OFF")
        logging.info(f"Low threat level: {total_threat:.2f}")
        vpn_off()

    else:
        print(f"[THREAT] MEDIUM ({total_threat:.2f})")

    total_threat = max(0.0, total_threat - DECAY_RATE)
    time.sleep(5)
