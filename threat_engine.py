# threat_engine.py

from logger import log_event

THREAT_THRESHOLD = 0.7
threat_score = 0.0


def add_threat(score):
    global threat_score
    threat_score += score
    if threat_score > 1.0:
        threat_score = 1.0
    log_event(f"THREAT increased by {score}. Current score = {threat_score}")


def reduce_threat(score=0.1):
    global threat_score
    threat_score -= score
    if threat_score < 0.0:
        threat_score = 0.0
    log_event(f"THREAT reduced. Current score = {threat_score}")


def is_network_unsafe():
    return threat_score >= THREAT_THRESHOLD
