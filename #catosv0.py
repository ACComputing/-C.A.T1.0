import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import random
import time
import math
import re

class CAT_JARVIS:
    def __init__(self, root):
        self.root = root
        self.root.title("S.H.I.E.L.D. - C.A.T v0.4.7")
        
        # Dimensions as requested
        self.width = 600
        self.height = 400
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        # Tactical Colors
        self.clr_hud = "#00ccff"   
        self.clr_alert = "#ff2200"  
        self.clr_ok = "#00ffaa"     
        self.clr_dim = "#002233"    
        self.clr_bg = "#000000"

        self.is_booted = False
        self.is_executing = False
        self.rotation = 0

        self.setup_ui()
        
        # Start background threads
        threading.Thread(target=self.boot_sequence, daemon=True).start()
        self.animate_loop()

    def setup_ui(self):
        # Background Canvas for Animations
        self.canvas = tk.Canvas(self.root, bg=self.clr_bg, highlightthickness=0)
        self.canvas.place(x=0, y=0, width=self.width, height=self.height)

        # Draw Grid
        for i in range(0, self.width, 40):
            self.canvas.create_line(i, 0, i, self.height, fill="#051015")
        for i in range(0, self.height, 40):
            self.canvas.create_line(0, i, self.width, i, fill="#051015")

        # Tactical Rings (Center)
        cx, cy = self.width // 2, self.height // 2 - 20
        self.ring1 = self.canvas.create_oval(cx-80, cy-80, cx+80, cy+80, outline=self.clr_dim, dash=(5,5))
        self.ring2 = self.canvas.create_oval(cx-60, cy-60, cx+60, cy+60, outline=self.clr_hud, width=1)
        
        # --- Sidebars ---
        # Analytics (Left)
        self.canvas.create_text(10, 20, text="ANALYTICS", fill=self.clr_hud, font=("Consolas", 8, "bold"), anchor="w")
        self.stat_label = self.canvas.create_text(10, 40, text="SHIELD: CALIBRATING\nUPLINK: SEARCHING\nTHREAT: 0.00%", 
                                               fill=self.clr_ok, font=("Consolas", 7), anchor="nw", justify="left")

        # Objectives (Right)
        self.canvas.create_text(self.width-10, 20, text="OBJECTIVES", fill=self.clr_hud, font=("Consolas", 8, "bold"), anchor="e")
        self.obj_label = self.canvas.create_text(self.width-10, 40, text="• MONITOR CHANNELS\n• MAINTAIN SHIELD\n• READY", 
                                              fill=self.clr_dim, font=("Consolas", 7), anchor="ne", justify="right")

        # --- Terminal (Bottom) ---
        self.terminal = scrolledtext.ScrolledText(self.root, bg="#020508", fg=self.clr_ok, font=("Consolas", 8),
                                                bd=1, highlightthickness=1, highlightbackground=self.clr_dim, 
                                                state=tk.DISABLED, insertbackground=self.clr_hud)
        self.terminal.place(x=10, y=280, width=580, height=80)

        self.cmd_entry = tk.Entry(self.root, bg="#050a0c", fg=self.clr_hud, font=("Consolas", 9),
                                bd=0, highlightthickness=1, highlightbackground=self.clr_dim)
        self.cmd_entry.place(x=10, y=365, width=480, height=25)
        self.cmd_entry.bind("<Return>", self.handle_mission_cmd)

        self.exe_btn = tk.Button(self.root, text="INITIATE", bg=self.clr_hud, fg="#000000",
                               font=("Consolas", 8, "bold"), command=self.handle_mission_cmd)
        self.exe_btn.place(x=500, y=365, width=90, height=25)

        # --- CENTER CHATBOT ---
        self.chat_frame = tk.Frame(self.root, bg="#0a151b", highlightbackground=self.clr_hud, highlightthickness=1)
        self.chat_frame.place(x=self.width//2, y=self.height//2 - 20, width=280, height=180, anchor="center")

        self.chat_display = scrolledtext.ScrolledText(self.chat_frame, bg="#010305", fg="#cccccc", font=("Consolas", 8),
                                                    state=tk.DISABLED, bd=0)
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        self.chat_entry = tk.Entry(self.chat_frame, bg="#050a0c", fg=self.clr_hud, font=("Consolas", 9),
                                 insertbackground=self.clr_hud, bd=0)
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
        self.chat_entry.bind("<Return>", self.handle_chat)

        send_btn = tk.Button(self.chat_frame, text=">", bg=self.clr_hud, fg="#000000",
                           font=("Consolas", 8, "bold"), bd=0, command=self.handle_chat)
        send_btn.pack(side=tk.RIGHT, padx=2)

    def add_terminal(self, msg):
        self.terminal.config(state=tk.NORMAL)
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.terminal.insert(tk.END, f"[{ts}] {msg}\n")
        self.terminal.see(tk.END)
        self.terminal.config(state=tk.DISABLED)

    def add_chat(self, sender, msg):
        self.chat_display.config(state=tk.NORMAL)
        color = self.clr_hud if sender == "YOU" else self.clr_ok
        self.chat_display.insert(tk.END, f"{sender}: ", "sender")
        self.chat_display.insert(tk.END, f"{msg}\n")
        self.chat_display.tag_config("sender", foreground=color)
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)

    def boot_sequence(self):
        self.add_terminal(">> INITIALIZING BOOT...")
        time.sleep(1)
        self.add_terminal(">> CORE SYNC v0.4.7 ACTIVE.")
        self.canvas.itemconfig(self.stat_label, text="SHIELD: 98.4%\nUPLINK: STABLE\nTHREAT: MINIMAL", fill=self.clr_ok)
        self.add_chat("C.A.T", "Hello Operator. Systems Online.")
        self.is_booted = True

    def animate_loop(self):
        self.rotation += 2
        # Simple ring pulse/rotation simulation
        cx, cy = self.width // 2, self.height // 2 - 20
        # Update coordinates to simulate movement if desired, or just pulse color
        glow = "#%02x%02x%02x" % (0, int(150 + 100 * math.sin(self.rotation/20)), 255)
        self.canvas.itemconfig(self.ring2, outline=glow)
        self.root.after(50, self.animate_loop)

    def handle_chat(self, event=None):
        msg = self.chat_entry.get().strip()
        if not msg: return
        self.chat_entry.delete(0, tk.END)
        self.add_chat("YOU", msg)
        
        # Simple AI Logic
        response = "DIRECTIVE UNKNOWN."
        low = msg.lower()
        if "hello" in low: response = "Greetings, Operator."
        elif "status" in low: response = "All systems nominal."
        elif "shield" in low: response = "Integrity at 98.4%."
        
        self.root.after(500, lambda: self.add_chat("C.A.T", response))

    def handle_mission_cmd(self, event=None):
        cmd = self.cmd_entry.get().strip().upper()
        if not cmd or self.is_executing: return
        self.cmd_entry.delete(0, tk.END)
        
        self.is_executing = True
        self.add_terminal(f">> EXECUTING: {cmd}")
        
        def run_mission():
            time.sleep(1.5)
            self.add_terminal(f">> SUCCESS: {cmd} COMPLETED.")
            self.is_executing = False
        
        threading.Thread(target=run_mission, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = CAT_JARVIS(root)
    root.mainloop()