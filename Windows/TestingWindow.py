"""
Testing Window Module
Manual ECU command testing and control interface
"""

import tkinter as tk
import tkinter.ttk as ttk
import datetime


class TestingWindow:
    def __init__(self, port):
        self.PORT = port
        
        # Create a new window
        self.window = tk.Tk()
        self.window.title("ECU Testing & Control")
        self.window.geometry("900x700")
        self.window.resizable(False, False)

        # Create main frame with two columns
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left column - Controls
        left_frame = ttk.LabelFrame(main_frame, text="ECU Controls", padding="10")
        left_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Right column - Manual Commands
        right_frame = ttk.LabelFrame(main_frame, text="Manual Commands", padding="10")
        right_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # === LEFT COLUMN - CONTROLS ===
        
        # Fuel Pump Toggle
        fuel_frame = ttk.LabelFrame(left_frame, text="Fuel Pump Control", padding="10")
        fuel_frame.pack(fill=tk.X, pady=10)
        
        self.fuel_pump_var = tk.BooleanVar(value=False)
        fuel_toggle = ttk.Checkbutton(
            fuel_frame, 
            text="Fuel Pump On/Off", 
            variable=self.fuel_pump_var,
            command=self.toggle_fuel_pump
        )
        fuel_toggle.pack(anchor=tk.W)
        self.fuel_status_label = ttk.Label(fuel_frame, text="Status: OFF", foreground="red")
        self.fuel_status_label.pack(anchor=tk.W, pady=5)

        # Cylinder Deactivation
        cylinder_frame = ttk.LabelFrame(left_frame, text="Cylinder Deactivation", padding="10")
        cylinder_frame.pack(fill=tk.X, pady=10)
        
        self.cylinder_vars = []
        for i in range(1, 7):  # Assuming 6-cylinder engine
            var = tk.BooleanVar(value=False)
            self.cylinder_vars.append(var)
            cb = ttk.Checkbutton(
                cylinder_frame,
                text=f"Disable Cylinder {i}",
                variable=var,
                command=lambda idx=i-1: self.toggle_cylinder(idx)
            )
            cb.pack(anchor=tk.W, pady=2)

        # Manual Input Controls
        inputs_frame = ttk.LabelFrame(left_frame, text="Manual Inputs", padding="10")
        inputs_frame.pack(fill=tk.X, pady=10)

        # Engine Temperature
        temp_label = ttk.Label(inputs_frame, text="Engine Temperature (°F):")
        temp_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.temp_spinbox = ttk.Spinbox(inputs_frame, from_=50, to=250, width=10)
        self.temp_spinbox.set(180)
        self.temp_spinbox.grid(row=0, column=1, padx=10, pady=5)
        temp_send_btn = ttk.Button(inputs_frame, text="Send", command=self.send_temperature)
        temp_send_btn.grid(row=0, column=2, pady=5)

        # AAC (Auxiliary Air Control)
        aac_label = ttk.Label(inputs_frame, text="AAC Valve (%):")
        aac_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.aac_spinbox = ttk.Spinbox(inputs_frame, from_=0, to=100, width=10)
        self.aac_spinbox.set(50)
        self.aac_spinbox.grid(row=1, column=1, padx=10, pady=5)
        aac_send_btn = ttk.Button(inputs_frame, text="Send", command=self.send_aac)
        aac_send_btn.grid(row=1, column=2, pady=5)

        # Timing Adjustment
        timing_label = ttk.Label(inputs_frame, text="Timing Adjustment (°):")
        timing_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.timing_spinbox = ttk.Spinbox(inputs_frame, from_=-20, to=40, width=10)
        self.timing_spinbox.set(15)
        self.timing_spinbox.grid(row=2, column=1, padx=10, pady=5)
        timing_send_btn = ttk.Button(inputs_frame, text="Send", command=self.send_timing)
        timing_send_btn.grid(row=2, column=2, pady=5)

        # === RIGHT COLUMN - MANUAL COMMANDS ===
        
        # Command input
        cmd_label = ttk.Label(right_frame, text="Raw Command (Hex):")
        cmd_label.pack(anchor=tk.W, pady=5)
        
        self.input_box = ttk.Entry(right_frame, width=40)
        self.input_box.pack(pady=5)

        send_button = ttk.Button(right_frame, text="Send Command", command=self.send_data)
        send_button.pack(pady=5)

        # Response box
        response_label = ttk.Label(right_frame, text="Response Log:")
        response_label.pack(anchor=tk.W, pady=5)
        
        self.response_box = tk.Text(right_frame, height=25, width=50)
        self.response_box.pack(pady=5)

        # Scrollbar for response box
        scrollbar = ttk.Scrollbar(right_frame, command=self.response_box.yview)
        self.response_box.configure(yscrollcommand=scrollbar.set)

        # Buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(pady=10)
        
        clear_button = ttk.Button(button_frame, text="Clear Log", command=self.clear_response)
        clear_button.pack(side=tk.LEFT, padx=5)

        close_button = ttk.Button(button_frame, text="Close", command=self.window.destroy)
        close_button.pack(side=tk.LEFT, padx=5)

    def toggle_fuel_pump(self):
        """Toggle fuel pump on/off"""
        if self.fuel_pump_var.get():
            self.fuel_status_label.config(text="Status: ON", foreground="green")
            self.log_response("Fuel Pump: ON")
        else:
            self.fuel_status_label.config(text="Status: OFF", foreground="red")
            self.log_response("Fuel Pump: OFF")

    def toggle_cylinder(self, cylinder_index):
        """Toggle individual cylinder on/off"""
        status = "DISABLED" if self.cylinder_vars[cylinder_index].get() else "ENABLED"
        self.log_response(f"Cylinder {cylinder_index + 1}: {status}")

    def send_temperature(self):
        """Send engine temperature command"""
        temp = self.temp_spinbox.get()
        self.log_response(f"Setting Temperature: {temp}°F")

    def send_aac(self):
        """Send AAC valve command"""
        aac = self.aac_spinbox.get()
        self.log_response(f"Setting AAC: {aac}%")

    def send_timing(self):
        """Send timing adjustment command"""
        timing = self.timing_spinbox.get()
        self.log_response(f"Setting Timing: {timing}°")

    def send_data(self):
        """Send raw hex data to ECU"""
        data = self.input_box.get()
        if not data:
            return
        self.log_response(f"Command: {data} (hex)")

    def log_response(self, message):
        """Add message to response log"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.response_box.insert(tk.END, f"[{timestamp}] {message}\n")
        self.response_box.see(tk.END)

    def clear_response(self):
        """Clear the response box"""
        self.response_box.delete('1.0', tk.END)

    def run(self):
        """Start the main event loop"""
        self.window.mainloop()
