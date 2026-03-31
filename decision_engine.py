UNSAFE_THRESHOLD = 0.7
network_state = "SAFE"

def evaluate_network(threat_score):
    global network_state

    if threat_score >= UNSAFE_THRESHOLD and network_state != "UNSAFE":
        network_state = "UNSAFE"
        print("[DECISION] Network state changed to UNSAFE")
        return "UNSAFE"

    if threat_score < UNSAFE_THRESHOLD and network_state != "SAFE":
        network_state = "SAFE"
        print("[DECISION] Network state changed to SAFE")
        return "SAFE"

    return network_state
