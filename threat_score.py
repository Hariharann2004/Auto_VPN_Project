import time

threat_score = 0.0
last_update = time.time()

DECAY_RATE = 0.05   # score decay per minute

def add_score(value):
    global threat_score
    threat_score = min(1.0, threat_score + value)
    return threat_score

def decay_score():
    global threat_score, last_update
    now = time.time()
    elapsed = (now - last_update) / 60  # minutes

    if elapsed > 0:
        threat_score = max(0.0, threat_score - (DECAY_RATE * elapsed))
        last_update = now

    return threat_score

def get_score():
    decay_score()
    return threat_score
