import tkinter as tk
from tkinter import scrolledtext
import threading
import datetime
import random
import time
import math

class CAT_JARVIS:
    def __init__(self, root):
        self.root = root
        self.root.title("C.A.T - Central Advanced Technician v0.1")
        self.root.geometry("600x400")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        # UI Colors (Neon/Cyberpunk theme)
        self.color_primary = "#00d9ff"    # Cyan
        self.color_secondary = "#004455"  # Dark Cyan
        self.color_text = "#00ffaa"       # Mint
        self.color_bg = "#000000"         # Black

        # Animation variables
        self.animation_phase = 0
        self.is_booted = False
        
        # Build the interface
        self.setup_ui()

        # Start the "Holographic" Boot Sequence
        threading.Thread(target=self.holographic_boot, daemon=True).start()

    def setup_ui(self):
        # Background Canvas for HUD elements
        self.canvas = tk.Canvas(self.root, bg=self.color_bg, highlightthickness=0)
        self.canvas.place(x=0, y=0, width=600, height=400)

        # Decorative Brackets
        self.draw_hud_frame()

        # Central Pulse Ring (Hidden during boot)
        self.ring = self.canvas.create_oval(265, 45, 335, 115, outline=self.color_primary, width=2, state='hidden')
        self.core_text = self.canvas.create_text(300, 80, text="C.A.T", fill=self.color_primary, font=("Consolas", 12, "bold"), state='hidden')
        
        # Status Bar
        self.status_line = self.canvas.create_text(
            300, 20, text="SYSTEM STATUS: INITIALIZING...", 
            fill=self.color_secondary, font=("Consolas", 8)
        )

        # Terminal Log
        self.log = scrolledtext.ScrolledText(
            self.root, bg="#05080a", fg=self.color_text, font=("Consolas", 9),
            wrap=tk.WORD, state=tk.DISABLED, bd=0, highlightthickness=1, 
            highlightbackground=self.color_secondary, insertbackground=self.color_primary
        )
        self.log.place(x=25, y=140, width=550, height=200)

        # Input Area
        self.entry = tk.Entry(
            self.root, bg="#0a1215", fg=self.color_primary, font=("Consolas", 11),
            insertbackground=self.color_primary, bd=0, highlightthickness=1,
            highlightbackground=self.color_secondary
        )
        self.entry.place(x=25, y=355, width=460, height=30)
        self.entry.bind("<Return>", self.send_command)

        self.exe_btn = tk.Button(
            self.root, text="EXECUTE", bg=self.color_primary, fg="#000000",
            font=("Consolas", 9, "bold"), bd=0, activebackground=self.color_secondary,
            command=self.send_command, state=tk.DISABLED
        )
        self.exe_btn.place(x=495, y=355, width=80, height=30)

    def draw_hud_frame(self):
        # Brackets
        padding = 15
        length = 40
        # Top-Left
        self.canvas.create_line(padding, padding, padding + length, padding, fill=self.color_secondary)
        self.canvas.create_line(padding, padding, padding, padding + length, fill=self.color_secondary)
        # Bottom-Right
        self.canvas.create_line(600-padding, 400-padding, 600-padding-length, 400-padding, fill=self.color_secondary)
        self.canvas.create_line(600-padding, 400-padding, 600-padding, 400-padding-length, fill=self.color_secondary)

    def holographic_boot(self):
        """Simulates a tech-heavy boot sequence."""
        boot_logs = [
            "[OK] LOADING NEURAL KERNEL 0.1...",
            "[OK] CATSAN TECHNOLOGIES PROTOCOLS LOADED.",
            "[OK] ESTABLISHING SECURE OPERATOR LINK...",
            "[!!] SCANNING FOR HARDWARE VULNERABILITIES...",
            "[OK] ALL SYSTEMS NOMINAL.",
            "---------------------------------------",
            "CENTRAL ADVANCED TECHNICIAN ONLINE."
        ]

        for line in boot_logs:
            self.add_message("SYSTEM", line, color="#ffaa00")
            time.sleep(random.uniform(0.3, 0.7))
        
        # Show HUD elements
        self.canvas.itemconfig(self.ring, state='normal')
        self.canvas.itemconfig(self.core_text, state='normal')
        self.canvas.itemconfig(self.status_line, text="NEURAL LINK: ENCRYPTED | CATSAN v0.1", fill=self.color_primary)
        self.exe_btn.config(state=tk.NORMAL)
        self.is_booted = True
        
        self.animate_hud()
        self.add_message("C.A.T", "Greetings, Operator. I am C.A.T. How shall we proceed today?")

    def animate_hud(self):
        """Infinite pulse animation for the central holographic core."""
        if not self.is_booted: return
        
        self.animation_phase += 0.1
        pulse = abs(math.sin(self.animation_phase) * 4)
        
        # Update Ring
        blue_val = int(180 + 75 * math.sin(self.animation_phase))
        color = f"#00{blue_val:02x}ff"
        self.canvas.itemconfig(self.ring, width=1 + pulse, outline=color)
        self.canvas.itemconfig(self.core_text, fill=color)
        
        self.root.after(50, self.animate_hud)

    def add_message(self, sender, text, color=None):
        self.log.config(state=tk.NORMAL)
        tag_name = f"tag_{random.random()}"
        
        if not color:
            color = self.color_text if sender == "C.A.T" else "#55aaff"
            
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log.insert(tk.END, f"[{timestamp}] ", "dim")
        self.log.insert(tk.END, f"{sender}: {text}\n", tag_name)
        
        self.log.tag_config(tag_name, foreground=color)
        self.log.tag_config("dim", foreground="#003344")
        
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)

    def send_command(self, event=None):
        if not self.is_booted: return
        
        cmd = self.entry.get().strip()
        if not cmd: return
        self.entry.delete(0, tk.END)
        
        self.add_message("OPERATOR", cmd)
        self.process_ai_logic(cmd.lower())

    def process_ai_logic(self, cmd):
        # AI logic mapping (CATSAN Tech logic)
        responses = {
            "status": "Power levels at 98.4%. CPU cycle stable at 4.2GHz. No intrusions detected.",
            "time": f"Current system time is {datetime.datetime.now().strftime('%I:%M:%S %p')}.",
            "date": f"Standard calendar date is {datetime.datetime.now().strftime('%d %B, %Y')}.",
            "hello": "Interface synchronized. I am ready for your directives.",
            "who": "I am the Central Advanced Technician, version 0.1, developed by CATSAN Technologies.",
            "clear": "log_clear"
        }

        # Dynamic Analysis
        if cmd == "clear":
            self.log.config(state=tk.NORMAL)
            self.log.delete(1.0, tk.END)
            self.log.config(state=tk.DISABLED)
            return

        response = "Command not recognized in current security level. Analysis logged."
        for key in responses:
            if key in cmd:
                response = responses[key]
                break
        
        # Simulate processing delay
        self.root.after(400, lambda: self.add_message("C.A.T", response))

if __name__ == "__main__":
    root = tk.Tk()
    # Set window icon placeholder logic or styling
    try:
        root.attributes('-alpha', 0.95) # Slight transparency for that HUD feel
    except:
        pass
        
    app = CAT_JARVIS(root)
    root.mainloop()
