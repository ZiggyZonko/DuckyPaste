import pyperclip
import tkinter as tk
from constants import *

# ---- Variables ---- #
history = []
last_clip = ""
clips = 0

# ---- Tkinter Initlisation ---- #
root = tk.Tk()
root.title("🦆 DuckyPaste")
root.geometry("400x600")
root.minsize(350, 500)
root.configure(bg=BG)

# ---- UI + Widgets ---- #
title = tk.Label(root, text="🦆 DuckyPaste", font=("Segoe UI", 20, "bold"), bg=BG, fg=ACCENT)
subtitle = tk.Label(root, text="Your clipboard, remembered.", font=("Segoe UI", 10), bg=BG, fg=SUBTEXT)
listbox = tk.Listbox(root, bg=PANEL, fg=TEXT, selectbackground=ACCENT, selectforeground="black", borderwidth=0, highlightthickness=0, font=("Consolas", 10))
status = tk.Label(root, text="0 clips stored", bg=PANEL, fg=SUBTEXT)
title.pack(pady=10)
subtitle.pack()
status.pack(side="bottom", fill="x")
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

def check_clipboard():
    global last_clip
    global history
    global clips

    current = pyperclip.paste()
    
    if (current != last_clip and current.strip() != "" and current not in history):
        clips += 1
        last_clip = current

        if current in history:
            history.remove(current)
            print(history)

        history.insert(0, current)
        listbox.insert(0, current)

        print("Added:", current)
        status.config(text="Clips Stored: " + str(clips))

    root.after(500, check_clipboard)

def on_select(event):
    selection = listbox.curselection()

    if selection:
        text = listbox.get(selection[0])
        pyperclip.copy(text)
    

listbox.bind("<<ListboxSelect>>", on_select)

check_clipboard()
root.mainloop()
