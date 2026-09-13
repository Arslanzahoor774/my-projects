import tkinter as tk
from datetime import datetime

# ===============================
# FIFA WORLD CUP 2026
# PART 1
# ===============================

root = tk.Tk()
root.title("FIFA World Cup 2026")
root.geometry("1400x800")
root.configure(bg="#061A40")

# --------------------------------
# Header
# --------------------------------

header = tk.Frame(root, bg="#003366", height=80)
header.pack(fill="x")

title = tk.Label(
    header,
    text="🏆 FIFA WORLD CUP 2026",
    font=("Arial", 28, "bold"),
    fg="black",          # Changed to black
    bg="#003366"
)
title.pack(pady=15)

# --------------------------------
# Navigation (Centered)
# --------------------------------

nav = tk.Frame(root, bg="#0A2342")
nav.pack(fill="x")

nav_buttons = tk.Frame(nav, bg="#0A2342")
nav_buttons.pack(pady=10)

buttons = [
    "Home",
    "Qualified Teams",
    "Group Stage",
    "Fixtures",
    "Statistics",
    "Predictions",
    "Settings"
]

for item in buttons:
    b = tk.Button(
        nav_buttons,
        text=item,
        font=("Arial", 12, "bold"),
        bg="#007ACC",
        fg="black",      # Changed to black
        relief="flat",
        padx=18,
        pady=8,
        cursor="hand2"
    )
    b.pack(side="left", padx=8)

# --------------------------------
# Hero Section
# --------------------------------

hero = tk.Frame(root, bg="#061A40")
hero.pack(fill="both", expand=True)

welcome = tk.Label(
    hero,
    text="WELCOME TO FIFA WORLD CUP 2026",
    font=("Arial", 30, "bold"),
    fg="gold",
    bg="#061A40"
)
welcome.pack(pady=30)

subtitle = tk.Label(
    hero,
    text="Official Tournament Dashboard",
    font=("Arial", 18),
    fg="black",          # Changed to black
    bg="#061A40"
)
subtitle.pack()

# --------------------------------
# Countdown
# --------------------------------

countdown = tk.Label(
    hero,
    font=("Arial", 24, "bold"),
    fg="cyan",
    bg="#061A40"
)
countdown.pack(pady=30)

target = datetime(2026, 6, 11)

def update_timer():
    now = datetime.now()
    diff = target - now

    if diff.total_seconds() > 0:
        days = diff.days
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        seconds = diff.seconds % 60

        countdown.config(
            text=f"{days} Days  {hours} Hours  {minutes} Minutes  {seconds} Seconds"
        )
    else:
        countdown.config(text="🏆 TOURNAMENT HAS STARTED!")

    root.after(1000, update_timer)

update_timer()

# --------------------------------
# Dashboard Buttons
# --------------------------------

dashboard = tk.Frame(hero, bg="#061A40")
dashboard.pack(pady=20)

sections = [
    "Qualified Teams",
    "Player Statistics",
    "Golden Boot",
    "Golden Glove",
    "Live Standings",
    "Match Predictions"
]

for section in sections:
    btn = tk.Button(
        dashboard,
        text=section,
        width=22,
        height=2,
        bg="#00A86B",
        fg="black",      # Changed to black
        font=("Arial", 12, "bold"),
        relief="raised",
        cursor="hand2"
    )
    btn.pack(pady=8)

# --------------------------------
# Status Bar
# --------------------------------

status = tk.Label(
    root,
    text="Version 1.0 | FIFA World Cup 2026 Dashboard",
    bg="#003366",
    fg="black",          # Changed to black
    anchor="w"
)
status.pack(fill="x", side="bottom")

# --------------------------------
# Run Application
# --------------------------------

root.mainloop()