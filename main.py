import tkinter as tk
import random


class EnhancedTeslaRTOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Tesla Cyber-RTOS Dashboard")
        self.root.geometry("850x600")
        self.root.configure(bg="#0A0A0A")

        self.system_mode = "NORMAL"
        self.cpu_load = 45
        self.task_states = {
            "Brakes": {"load": 10, "crit": True, "active": True},
            "Autopilot": {"load": 35, "crit": True, "active": True},
            "Nav UI": {"load": 25, "crit": False, "active": True},
            "Music": {"load": 15, "crit": False, "active": True}
        }

        self.setup_ui()
        self.animate_loop()

    def setup_ui(self):
        # Title Header
        header = tk.Label(self.root, text="SYSTEM DIAGNOSTICS: CORE EXECUTION METRICS",
                          font=("Courier", 14, "bold"), fg="#FF3B30", bg="#0A0A0A")
        header.pack(pady=15)

        # Top Section: Master CPU Load Meter
        cpu_frame = tk.Frame(self.root, bg="#121212", bd=1, relief=tk.SOLID)
        cpu_frame.pack(fill=tk.X, padx=25, pady=5)

        tk.Label(cpu_frame, text="GLOBAL CPU COMPUTE OVERHEAD", font=("Courier", 10, "bold"), fg="#8E8E93",
                 bg="#121212").pack(anchor="w", padx=15, pady=5)

        self.cpu_canvas = tk.Canvas(cpu_frame, height=25, bg="#1A1A1A", highlightthickness=0)
        self.cpu_canvas.pack(fill=tk.X, padx=15, pady=5)

        self.lbl_cpu_text = tk.Label(cpu_frame, text="CPU: 45% [NOMINAL]", font=("Courier", 11, "bold"), fg="#00FF00",
                                     bg="#121212")
        self.lbl_cpu_text.pack(pady=2)

        # Split Layout Panel
        panel_frame = tk.Frame(self.root, bg="#0A0A0A")
        panel_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)

        # Left Control Panel
        left_ctrl = tk.Frame(panel_frame, bg="#121212", width=250, bd=1, relief=tk.SOLID)
        left_ctrl.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        left_ctrl.pack_propagate(False)

        tk.Label(left_ctrl, text="OPERATIONAL MODES", font=("Courier", 11, "bold"), fg="#FFFFFF", bg="#121212").pack(
            pady=15)

        btn_normal = tk.Button(left_ctrl, text="1. HIGHWAY CRUISE\n(Standard Load)", font=("Courier", 10, "bold"),
                               bg="#1C1C1E", fg="#00FF00", bd=1, relief=tk.RAISED, command=self.set_normal_mode)
        btn_normal.pack(fill=tk.X, padx=15, pady=10, ipady=5)

        btn_surge = tk.Button(left_ctrl, text="2. HAZARD SURGE\n(Eliminate Low-Crit)", font=("Courier", 10, "bold"),
                              bg="#FF3B30", fg="#FFFFFF", bd=0, command=self.set_surge_mode)
        btn_surge.pack(fill=tk.X, padx=15, pady=10, ipady=5)

        self.lbl_status_brief = tk.Label(left_ctrl, text="MODE: NORMAL\nAll systems functional.",
                                         font=("Courier", 9), fg="#8E8E93", bg="#121212", justify=tk.LEFT)
        self.lbl_status_brief.pack(side=tk.BOTTOM, pady=20, padx=10)

        # Right Live Resource Monitoring Panel
        right_monitor = tk.Frame(panel_frame, bg="#121212", bd=1, relief=tk.SOLID)
        right_monitor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        tk.Label(right_monitor, text="THREAD SCHEDULER MONITOR", font=("Courier", 11, "bold"), fg="#FFFFFF",
                 bg="#121212").pack(pady=10)

        self.task_bars = {}
        for name, info in self.task_states.items():
            task_row = tk.Frame(right_monitor, bg="#121212")
            task_row.pack(fill=tk.X, padx=20, pady=8)

            lbl_tag = " [CRIT]" if info["crit"] else " [LOW]"
            lbl_color = "#FF9500" if info["crit"] else "#007AFF"

            lbl = tk.Label(task_row, text=f"{name}{lbl_tag}", font=("Courier", 10, "bold"), fg=lbl_color, bg="#121212",
                           width=16, anchor="w")
            lbl.pack(side=tk.LEFT)

            canvas = tk.Canvas(task_row, height=18, bg="#1A1A1A", highlightthickness=0)
            canvas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

            self.task_bars[name] = canvas

    def set_normal_mode(self):
        self.system_mode = "NORMAL"
        self.lbl_status_brief.config(text="MODE: NORMAL\nAll tasks scheduled\nand running smoothly.", fg="#00FF00")
        for name in self.task_states:
            self.task_states[name]["active"] = True

    def set_surge_mode(self):
        self.system_mode = "CRITICAL_SURGE"
        self.lbl_status_brief.config(
            text="ALERT: SURGE MODE!\nNon-critical threads\ninstantly dropped to\nguarantee core safety.", fg="#FF3B30")
        for name in self.task_states:
            if not self.task_states[name]["crit"]:
                self.task_states[name]["active"] = False

    def draw_bar(self, canvas, percentage, color):
        canvas.delete("all")
        width = canvas.winfo_width()
        fill_width = (percentage / 100) * width
        canvas.create_rectangle(0, 0, fill_width, 18, fill=color, outline="")
        canvas.create_text(width - 30, 9, text=f"{int(percentage)}%", fill="#FFFFFF", font=("Courier", 8, "bold"))

    def animate_loop(self):
        # Dynamically recalculate allocations based on current state
        if self.system_mode == "NORMAL":
            self.task_states["Brakes"]["load"] = random.randint(8, 15)
            self.task_states["Autopilot"]["load"] = random.randint(30, 40)
            self.task_states["Nav UI"]["load"] = random.randint(20, 30)
            self.task_states["Music"]["load"] = random.randint(10, 18)
            self.cpu_load = sum(t["load"] for t in self.task_states.values())
            cpu_color = "#00FF00"
            cpu_text = f"CPU LOAD: {self.cpu_load}% [NOMINAL]"
        else:
            # Hazard conditions command extreme compute processing power
            self.task_states["Brakes"]["load"] = random.randint(35, 45)
            self.task_states["Autopilot"]["load"] = random.randint(85, 95)
            self.task_states["Nav UI"]["load"] = 0
            self.task_states["Music"]["load"] = 0
            self.cpu_load = self.task_states["Brakes"]["load"] + self.task_states["Autopilot"]["load"]
            cpu_color = "#FF3B30"
            cpu_text = f"CPU LOAD: {self.cpu_load}% [CRITICAL SURGE OVERRIDE]"

        # Refresh Master CPU bar
        self.draw_bar(self.cpu_canvas, min(self.cpu_load, 100), cpu_color)
        self.lbl_cpu_text.config(text=cpu_text, fg=cpu_color)

        # Refresh Individual Task bars
        for name, canvas in self.task_bars.items():
            info = self.task_states[name]
            if info["active"]:
                color = "#FF9500" if info["crit"] else "#007AFF"
                self.draw_bar(canvas, info["load"], color)
            else:
                # Visually present dropped threads as hollow, dead red zones
                canvas.delete("all")
                canvas.create_rectangle(0, 0, canvas.winfo_width(), 18, fill="#2C2C2E", outline="")
                canvas.create_text(40, 9, text="[DROPPED / OFFLINE]", fill="#FF3B30", font=("Courier", 8, "bold"))

        self.root.after(150, self.animate_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedTeslaRTOS(root)
    root.mainloop()