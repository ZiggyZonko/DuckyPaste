import pyperclip
import tkinter as tk
from constants import *
import json
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading

# ---- Variables ---- #
history = []
last_clip = ""
clips = 0

# ---- Icon ---- #
icon = Image.open(ICON_PATH)

# ---- Tkinter Initlisation ---- #
root = tk.Tk()
root.title("🦆 DuckyPaste")
root.geometry("400x600")
root.minsize(350, 500)
root.configure(bg=BG)

# ---- Show / Hide the window ---- #

def show_window(icon, item):
    root.after(0, root.deiconify)

def hide_window():
    root.withdraw()

def quit_app(icon, item):
    icon.stop()
    root.after(0, root.destroy)

tray_icon = Icon("DuckyPaste", icon, menu=Menu(MenuItem("Show", show_window), MenuItem("Quit", quit_app)))

# ---- Search Box ---- #
search_frame = tk.Frame(root, bg=BG)
search_frame.pack(fill="x", padx=10, pady=10)

search_icon = tk.Label(
    search_frame,
    text="🔍",
    bg=PANEL,
    fg=SUBTEXT,
    font=("Segoe UI", 11)
)
search_icon.pack(side="left", padx=(8, 0))

search_var = tk.StringVar()

search_box = tk.Entry(
    search_frame,
    textvariable=search_var,
    bg=PANEL,
    fg=TEXT,
    insertbackground=TEXT,
    relief="flat",
    borderwidth=0,
    font=("Segoe UI", 11)
)
search_box.pack(side="left", fill="x", expand=True, padx=8)

# ---- UI + Widgets ---- #
title = tk.Label(root, text="🦆 DuckyPaste", font=("Segoe UI", 20, "bold"), bg=BG, fg=ACCENT)
subtitle = tk.Label(root, text="Your clipboard, remembered.", font=("Segoe UI", 10), bg=BG, fg=SUBTEXT)
listbox = tk.Listbox(root, bg=PANEL, fg=TEXT, selectbackground=ACCENT, selectforeground="black", borderwidth=0, highlightthickness=0, font=("Consolas", 10))
button_frame = tk.Frame(root, bg=BG)
status = tk.Label(root, text="0 clips stored", bg=PANEL, fg=SUBTEXT)
pin_button = tk.Button(
    root,
    text="📌 Pin Selected",
    bg=PANEL,
    fg=TEXT,
    activebackground=ACCENT,
    activeforeground="black",
    relief="flat",
    borderwidth=0,
    font=("Segoe UI", 10, "bold"),
    cursor="hand2",
    padx=12,
    pady=6
)
delete_button = tk.Button(
    root,
    text = "🗑️ Delete Selected",
    bg=PANEL,
    fg=TEXT,
    activebackground=ACCENT,
    activeforeground="black",
    relief="flat",
    borderwidth=0,
    font=("Segoe UI", 10, "bold"),
    cursor="hand2",
    padx=12,
    pady=6
)
title.pack(pady=10)
subtitle.pack()
button_frame.pack(fill="x", padx=10, pady=10)
pin_button.pack(
    in_=button_frame,
    side="left",
    expand=True,
    fill="x",
    padx=(0, 5)
)

delete_button.pack(
    in_=button_frame,
    side="left",
    expand=True,
    fill="x",
    padx=(5, 0)
)
status.pack(side="bottom", fill="x")
search_box.pack(fill="x", padx=10, pady=5)
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ---- Saving Functions ---- #
def save_history():
    with open(DB_PATH, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)
        clips = len(history)

def load_history():
    global history

    try:
        with open(DB_PATH, "r", encoding="utf-8") as file:
            history = json.load(file)

        for item in history:
            listbox.insert(tk.END, item)

    except FileNotFoundError:
        history = []

def delete_clip(event):
    selected = listbox.curselection()

    if not selected:
        return
    
    selected = int(selected[0])

    if selected >= len(history):
        return
    
    print(selected)
    del history[selected]
    listbox.delete(selected)

    save_history()
    search_history()

# ---- Search Function ---- #

def search_history(*args):
    query = search_var.get().lower()

    listbox.delete(0, tk.END)

    for item in history:
        if query in item.lower():
            listbox.insert(tk.END, item)


# ---- Main Functionality ---- #
def check_clipboard():
    global last_clip
    global history
    global clips
    clips = len(history)

    current = pyperclip.paste()
    
    if (current != last_clip and current.strip() != "" and current not in history):
        last_clip = current

        if current in history:
            history.remove(current)
            print(history)

        history.insert(0, current)
        listbox.insert(0, current)

        save_history()

        print("Added:", current)
        status.config(text="Clips Stored: " + str(clips))

    root.after(500, check_clipboard)

def on_select(event):
    selection = listbox.curselection()

    if selection:
        text = listbox.get(selection[0])
        pyperclip.copy(text)

# ---- Hover On buttons Effect ---- #
def pin_hover(event):
    pin_button.config(bg=ACCENT, fg="black")

def pin_leave(event):
    pin_button.config(bg=PANEL, fg=TEXT)

pin_button.bind("<Enter>", pin_hover)
pin_button.bind("<Leave>", pin_leave)

# ---- Tray Icon Daemon ---- #
threading.Thread(
    target=tray_icon.run,
    daemon=True
).start()
    
# ---- Calling the Functions ---- #

listbox.bind("<Double-Button-1>", on_select)
search_var.trace_add("write", search_history)
delete_button.bind("<Button-1>", delete_clip)

load_history()
check_clipboard()
root.protocol("WM_DELETE_WINDOW", hide_window)
root.mainloop()
