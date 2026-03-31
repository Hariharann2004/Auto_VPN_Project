import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import time
import threading
import random

# ================== MAIN WINDOW ==================
root = tk.Tk()
root.title("Auto VPN – Cyber Security Dashboard")
root.geometry("1100x620")
root.resizable(False, False)
root.configure(bg="#0f172a")  # Dark background

# ================== STYLE ==================
style = ttk.Style()
style.theme_use("clam")

style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground="white", background="#0f172a")
style.configure("Sub.TLabel", font=("Segoe UI", 11), foreground="#cbd5e1", background="#0f172a")
style.configure("Card.TLabelframe", background="#020617", foreground="white")
style.configure("Card.TLabelframe.Label", font=("Segoe UI", 11, "bold"))
style.configure("Status.TLabel", font=("Segoe UI", 16, "bold"), background="#020617")
style.configure("Btn.TButton", font=("Segoe UI", 11, "bold"))

# ================== HEADER ==================
title = ttk.Label(root, text="🛡 AUTO VPN SECURITY SYSTEM", style="Title.TLabel")
title.pack(pady=10)

subtitle = ttk.Label(
    root,
    text="Real-time Threat Detection • Automatic VPN Protection",
    style="Sub.TLabel"
)
subtitle.pack()

# ================== MAIN LAYOUT ==================
container = ttk.Frame(root)
container.pack(fill="both", expand=True, padx=20, pady=15)

# ================== LEFT PANEL ==================
left = ttk.Frame(container)
left.pack(side="left", fill="y", padx=10)

# VPN CARD
vpn_card = ttk.LabelFrame(left, text="🔐 VPN STATUS", style="Card.TLabelframe", padding=15)
vpn_card.pack(fill="x", pady=10)

vpn_status = ttk.Label(vpn_card, text="OFF", foreground="red", style="Status.TLabel")
vpn_status.pack(pady=5)

# THREAT CARD
threat_card = ttk.LabelFrame(left, text="⚠ THREAT LEVEL", style="Card.TLabelframe", padding=15)
threat_card.pack(fill="x", pady=10)

threat_label = ttk.Label(threat_card, text="LOW", foreground="green", style="Status.TLabel")
threat_label.pack()

threat_bar = ttk.Progressbar(threat_card, length=250, mode="determinate")
threat_bar.pack(pady=10)

# CONTROL CARD
control_card = ttk.LabelFrame(left, text="🎛 CONTROLS", style="Card.TLabelframe", padding=15)
control_card.pack(fill="x", pady=10)

# ================== RIGHT PANEL ==================
right = ttk.Frame(container)
right.pack(side="right", fill="both", expand=True)

# GRAPH CARD
graph_card = ttk.LabelFrame(right, text="📊 THREAT GRAPH", style="Card.TLabelframe", padding=10)
graph_card.pack(fill="x", pady=10)

canvas = tk.Canvas(graph_card, bg="#020617", height=180)
canvas.pack(fill="x")

graph_points = []

# LOG CARD
log_card = ttk.LabelFrame(right, text="📜 SYSTEM LOGS", style="Card.TLabelframe", padding=10)
log_card.pack(fill="both", expand=True)

log_box = ScrolledText(log_card, font=("Consolas", 10), bg="#020617", fg="#e5e7eb", state="disabled")
log_box.pack(fill="both", expand=True)

# ================== LOG FUNCTION ==================
def log(msg):
    log_box.configure(state="normal")
    log_box.insert("end", f"{time.strftime('%H:%M:%S')} | {msg}\n")
    log_box.configure(state="disabled")
    log_box.yview("end")

# ================== GRAPH FUNCTION ==================
def draw_graph(value):
    graph_points.append(value)
    if len(graph_points) > 30:
        graph_points.pop(0)

    canvas.delete("all")
    w = canvas.winfo_width()
    h = 180

    if len(graph_points) < 2:
        return

    step = w / len(graph_points)

    for i in range(len(graph_points) - 1):
        x1 = i * step
        y1 = h - graph_points[i] * h
        x2 = (i + 1) * step
        y2 = h - graph_points[i + 1] * h
        canvas.create_line(x1, y1, x2, y2, fill="#22c55e", width=2)

# ================== SIMULATION ==================
running = False

def simulate():
    global running
    while running:
        threat = random.random()
        threat_bar["value"] = threat * 100
        draw_graph(threat)

        if threat >= 0.7:
            threat_label.config(text="HIGH", foreground="red")
            vpn_status.config(text="ON", foreground="lime")
            log("🚨 High threat detected → VPN ENABLED")

        elif threat >= 0.3:
            threat_label.config(text="MEDIUM", foreground="orange")
            log("⚠ Medium threat detected")

        else:
            threat_label.config(text="LOW", foreground="green")
            vpn_status.config(text="OFF", foreground="red")
            log("✅ System safe → VPN OFF")

        time.sleep(2)

def start_system():
    global running
    if not running:
        running = True
        log("▶ System started")
        threading.Thread(target=simulate, daemon=True).start()

def stop_system():
    global running
    running = False
    log("⏹ System stopped")

# ================== BUTTONS ==================
start_btn = ttk.Button(control_card, text="▶ START", command=start_system)
start_btn.pack(fill="x", pady=5)

stop_btn = ttk.Button(control_card, text="⏹ STOP", command=stop_system)
stop_btn.pack(fill="x", pady=5)

# ================== FOOTER ==================
footer = ttk.Label(
    root,
    text="© Auto VPN | Cyber Security Project | Real-Time Protection System",
    font=("Segoe UI", 9),
    foreground="#94a3b8",
    background="#0f172a"
)
footer.pack(pady=8)

root.mainloop()
