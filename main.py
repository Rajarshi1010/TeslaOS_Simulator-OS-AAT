import tkinter as tk
import random


class MultiAlgorithmTeslaRTOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Tesla RTOS vs. Round-Robin Benchmarking Suite")
        self.root.geometry("900x680")
        self.root.configure(bg="#0A0A0A")

        # Control States
        self.system_mode = "NORMAL"  # NORMAL or SURGE
        self.algorithm = "PREEMPTIVE_PRIORITY"  # PREEMPTIVE_PRIORITY or ROUND_ROBIN
        self.cpu_load = 45

        # Process Pool Configuration
        self.task_pool = {
            "Brakes": {"priority": 1, "load": 10, "active": True},
            "Autopilot": {"priority": 2, "load": 35, "active": True},
            "Nav UI": {"priority": 5, "load": 25, "active": True},
            "Music": {"priority": 6, "load": 15, "active": True}
        }

        self.setup_ui()
        self.scheduler_core_loop()

    def setup_ui(self):
        # Window Header
        header = tk.Label(self.root, text="OS BENCHMARK: PREEMPTIVE PRIORITY VS. ROUND ROBIN",
                          font=("Courier", 14, "bold"), fg="#FF3B30", bg="#0A0A0A")
        header.pack(pady=10)

        # Top Module: Global Overhead Graph
        cpu_frame = tk.Frame(self.root, bg="#121212", bd=1, relief=tk.SOLID)
        cpu_frame.pack(fill=tk.X, padx=25, pady=5)
        tk.Label(cpu_frame, text="GLOBAL CPU COMPUTE OVERHEAD", font=("Courier", 9, "bold"), fg="#8E8E93",
                 bg="#121212").pack(anchor="w", padx=15, pady=2)

        self.cpu_canvas = tk.Canvas(cpu_frame, height=20, bg="#1A1A1A", highlightthickness=0)
        self.cpu_canvas.pack(fill=tk.X, padx=15, pady=5)

        self.lbl_cpu_text = tk.Label(cpu_frame, text="CPU: 45% [NOMINAL]", font=("Courier", 10, "bold"), fg="#00FF00",
                                     bg="#121212")
        self.lbl_cpu_text.pack(pady=2)

        # Center Section Split Layout
        split_frame = tk.Frame(self.root, bg="#0A0A0A")
        split_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left Column: Configuration Controls
        left_ctrl = tk.Frame(split_frame, bg="#121212", width=280, bd=1, relief=tk.SOLID)
        left_ctrl.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        left_ctrl.pack_propagate(False)

        # Control Group A: Algorithm Selection
        tk.Label(left_ctrl, text="1. SELECT CPU ALGORITHM", font=("Courier", 10, "bold"), fg="#FFFFFF",
                 bg="#121212").pack(pady=10)

        self.btn_priority = tk.Button(left_ctrl, text="PREEMPTIVE PRIORITY\n(RTOS Framework)",
                                      font=("Courier", 9, "bold"),
                                      bg="#007AFF", fg="#FFFFFF", bd=0, command=self.set_priority_algo)
        self.btn_priority.pack(fill=tk.X, padx=15, pady=5, ipady=4)

        self.btn_rr = tk.Button(left_ctrl, text="ROUND ROBIN\n(Fair Share Framework)", font=("Courier", 9, "bold"),
                                bg="#2C2C2E", fg="#8E8E93", bd=0, command=self.set_rr_algo)
        self.btn_rr.pack(fill=tk.X, padx=15, pady=5, ipady=4)

        # Control Group B: Workload Mode Trigger
        tk.Label(left_ctrl, text="2. SELECT WORKLOAD MODE", font=("Courier", 10, "bold"), fg="#FFFFFF",
                 bg="#121212").pack(pady=10)

        self.btn_norm_mode = tk.Button(left_ctrl, text="HIGHWAY CRUISE\n(Normal Load)", font=("Courier", 9, "bold"),
                                       bg="#1C1C1E", fg="#00FF00", bd=1, command=self.set_normal_load)
        self.btn_norm_mode.pack(fill=tk.X, padx=15, pady=5, ipady=4)

        self.btn_surge_mode = tk.Button(left_ctrl, text="HAZARD SURGE\n(Critical Overload)",
                                        font=("Courier", 9, "bold"),
                                        bg="#1C1C1E", fg="#FF3B30", bd=1, command=self.set_surge_load)
        self.btn_surge_mode.pack(fill=tk.X, padx=15, pady=5, ipady=4)

        # Dynamic System Operational Text Box
        self.lbl_system_brief = tk.Label(left_ctrl, text="STATUS: System Nominal.\nPriority controls active.",
                                         font=("Courier", 9), fg="#8E8E93", bg="#121212", justify=tk.LEFT)
        self.lbl_system_brief.pack(side=tk.BOTTOM, pady=15, padx=10)

        # Right Column: Visual Component Timelines
        right_monitor = tk.Frame(split_frame, bg="#121212", bd=1, relief=tk.SOLID)
        right_monitor.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(right_monitor, text="READY QUEUE COMPONENT TRACKER", font=("Courier", 11, "bold"), fg="#FFFFFF",
                 bg="#121212").pack(pady=10)

        self.task_bars = {}
        for name, info in self.task_pool.items():
            task_row = tk.Frame(right_monitor, bg="#121212")
            task_row.pack(fill=tk.X, padx=15, pady=6)

            tag = " [CRIT]" if info["priority"] <= 2 else " [LOW]"
            tag_color = "#FF9500" if info["priority"] <= 2 else "#007AFF"

            lbl = tk.Label(task_row, text=f"{name}{tag}", font=("Courier", 10, "bold"), fg=tag_color, bg="#121212",
                           width=15, anchor="w")
            lbl.pack(side=tk.LEFT)

            canvas = tk.Canvas(task_row, height=16, bg="#1A1A1A", highlightthickness=0)
            canvas.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            self.task_bars[name] = canvas

        # Bottom Frame: The System Efficiency & Safety Matrix Dashboard
        efficiency_frame = tk.Frame(self.root, bg="#1A1A1A", bd=1, relief=tk.SOLID)
        efficiency_frame.pack(fill=tk.X, padx=25, pady=15)

        tk.Label(efficiency_frame, text="SYSTEM EFFICIENCY & SAFETY MATRIX", font=("Courier", 11, "bold"), fg="#FFFFFF",
                 bg="#1A1A1A").pack(pady=5)

        metrics_sub_frame = tk.Frame(efficiency_frame, bg="#1A1A1A")
        metrics_sub_frame.pack(fill=tk.X, padx=20, pady=5)

        self.lbl_crit_rate = tk.Label(metrics_sub_frame, text="Critical Deadline Success: 100%",
                                      font=("Courier", 10, "bold"), fg="#00FF00", bg="#1A1A1A")
        self.lbl_crit_rate.pack(side=tk.LEFT, expand=True)

        self.lbl_info_qos = tk.Label(metrics_sub_frame, text="Infotainment QoS: 100%", font=("Courier", 10, "bold"),
                                     fg="#00FF00", bg="#1A1A1A")
        self.lbl_info_qos.pack(side=tk.LEFT, expand=True)

        self.lbl_safety_score = tk.Label(efficiency_frame, text="VEHICLE SAFETY STATE: SECURE",
                                         font=("Courier", 12, "bold"), fg="#00FF00", bg="#1A1A1A")
        self.lbl_safety_score.pack(pady=8)

    # State Switching Commands
    def set_priority_algo(self):
        self.algorithm = "PREEMPTIVE_PRIORITY"
        self.btn_priority.config(bg="#007AFF", fg="#FFFFFF")
        self.btn_rr.config(bg="#2C2C2E", fg="#8E8E93")
        self.update_status_description()

    def set_rr_algo(self):
        self.algorithm = "ROUND_ROBIN"
        self.btn_rr.config(bg="#007AFF", fg="#FFFFFF")
        self.btn_priority.config(bg="#2C2C2E", fg="#8E8E93")
        self.update_status_description()

    def set_normal_load(self):
        self.system_mode = "NORMAL"
        self.update_status_description()

    def set_surge_load(self):
        self.system_mode = "SURGE"
        self.update_status_description()

    def update_status_description(self):
        if self.system_mode == "NORMAL":
            self.lbl_system_brief.config(
                text=f"ALGO: {self.algorithm}\nMODE: NORMAL\nResource usage balanced.\nSystem operating safely.",
                fg="#00FF00")
        else:
            if self.algorithm == "PREEMPTIVE_PRIORITY":
                self.lbl_system_brief.config(
                    text="ALGO: PREEMPTIVE\nMODE: SURGE ALERT!\nLow-priority channels\neliminated to preserve\ncore automotive safety.",
                    fg="#FF9500")
            else:
                self.lbl_system_brief.config(
                    text="ALGO: ROUND ROBIN\nMODE: SURGE ALERT!\nFair time slices sharing\ncauses critical process\nsynchronization lag!",
                    fg="#FF3B30")

    def draw_bar(self, canvas, percentage, color):
        canvas.delete("all")
        width = canvas.winfo_width()
        fill_width = (percentage / 100) * width
        canvas.create_rectangle(0, 0, fill_width, 16, fill=color, outline="")
        canvas.create_text(width - 35, 8, text=f"{int(percentage)}%", fill="#FFFFFF", font=("Courier", 8, "bold"))

    # Central Core Simulation Logic Engine
    def scheduler_core_loop(self):
        # 1. Evaluate Load & Handle Processing Channels based on Selection Context
        if self.system_mode == "NORMAL":
            self.task_pool["Brakes"]["load"] = random.randint(8, 12)
            self.task_pool["Autopilot"]["load"] = random.randint(30, 38)
            self.task_pool["Nav UI"]["load"] = random.randint(20, 26)
            self.task_pool["Music"]["load"] = random.randint(10, 15)
            self.task_pool["Nav UI"]["active"] = True
            self.task_pool["Music"]["active"] = True

            self.cpu_load = sum(t["load"] for t in self.task_pool.values())

            # Normal Metrics
            self.lbl_crit_rate.config(text="Critical Deadline Success: 100%", fg="#00FF00")
            self.lbl_info_qos.config(text="Infotainment QoS: 100%", fg="#00FF00")
            self.lbl_safety_score.config(text="VEHICLE SAFETY STATE: SECURE", fg="#00FF00")
            cpu_color = "#00FF00"

        else:  # SURGE OVERLOAD MODE
            if self.algorithm == "PREEMPTIVE_PRIORITY":
                # Real-Time OS behavior: Drop low-priority immediately
                self.task_pool["Brakes"]["load"] = random.randint(35, 45)
                self.task_pool["Autopilot"]["load"] = random.randint(50, 55)
                self.task_pool["Nav UI"]["load"] = 0
                self.task_pool["Music"]["load"] = 0
                self.task_pool["Nav UI"]["active"] = False
                self.task_pool["Music"]["active"] = False

                self.cpu_load = self.task_pool["Brakes"]["load"] + self.task_pool["Autopilot"]["load"]

                # Preemptive Efficiency Outputs
                self.lbl_crit_rate.config(text="Critical Deadline Success: 100%", fg="#00FF00")
                self.lbl_info_qos.config(text="Infotainment QoS: 0% [SHUTDOWN]", fg="#FF9500")
                self.lbl_safety_score.config(text="VEHICLE SAFETY STATE: SECURE (Resource Reclaimed)", fg="#00FF00")
                cpu_color = "#FF9500"

            else:  # ROUND ROBIN UNDER SURGE
                # Fair Share Failure: Infotainment forces data contention
                self.task_pool["Brakes"]["load"] = random.randint(20, 25)  # Stalled!
                self.task_pool["Autopilot"]["load"] = random.randint(25, 30)  # Stalled!
                self.task_pool["Nav UI"]["load"] = random.randint(25, 35)  # Continues consuming cycles
                self.task_pool["Music"]["load"] = random.randint(15, 20)  # Continues consuming cycles
                self.task_pool["Nav UI"]["active"] = True
                self.task_pool["Music"]["active"] = True

                self.cpu_load = 100  # CPU saturated completely

                # Round Robin Failure Metrics
                self.lbl_crit_rate.config(text="Critical Deadline Success: 42% [FAIL]", fg="#FF3B30")
                self.lbl_info_qos.config(text="Infotainment QoS: 85% [LAGGY]", fg="#FF9500")
                self.lbl_safety_score.config(text="VEHICLE SAFETY STATE: CRITICAL SYSTEM CRASH (Brake Lag Detected!)",
                                             fg="#FF3B30")
                cpu_color = "#FF3B30"

        # 2. Render Interface Displays
        self.draw_bar(self.cpu_canvas, self.cpu_load, cpu_color)
        self.lbl_cpu_text.config(text=f"CPU LOAD: {self.cpu_load}%", fg=cpu_color)

        for name, canvas in self.task_bars.items():
            info = self.task_pool[name]
            if info["active"]:
                color = "#FF9500" if info["priority"] <= 2 else "#007AFF"
                self.draw_bar(canvas, info["load"], color)
            else:
                canvas.delete("all")
                canvas.create_rectangle(0, 0, canvas.winfo_width(), 16, fill="#2C2C2E", outline="")
                canvas.create_text(65, 8, text="[ELIMINATED BY RTOS]", fill="#FF3B30", font=("Courier", 8, "bold"))

        self.root.after(200, self.scheduler_core_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = MultiAlgorithmTeslaRTOS(root)
    root.mainloop()