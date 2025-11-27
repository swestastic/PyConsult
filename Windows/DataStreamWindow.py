"""
Data Stream Window Module
Displays live ECU data stream with real-time updates
"""

import tkinter as tk
import tkinter.ttk as ttk
import threading
from Utils.Read import ReadStream


class DataStreamWindow:
    def __init__(self, port, config_file='configJSON.json', test_mode=False):
        self.PORT = port
        self.config_file = config_file
        self.test_mode = test_mode
        
        # Use RandomReadStream for test mode, otherwise use real ReadStream
        if test_mode:
            from Utils.Read import RandomReadStream
            self.R = RandomReadStream(port=None, daemon=True)
        else:
            self.R = ReadStream(port=self.PORT, daemon=True)
        
        # Create a new window
        self.window = tk.Tk()
        self.window.title("Data Stream")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        # Frame dimensions
        frame_width = 200
        frame_height = 100

        # Create all sensor frames and labels
        self._create_sensor_frames(frame_width, frame_height)
        self._place_sensor_frames()
        
        # Store value labels for updates
        self.value_labels = {
            'RPM': self.RPMvalue,
            'Speed': self.Speedvalue,
            'TPS': self.TPSvalue,
            'Temp': self.Tempvalue,
            'Timing': self.Timingvalue,
            'Battery': self.Batteryvalue,
            'AAC': self.AACvalue,
            'Injector': self.Injectorvalue
        }
        
        # Start updating values
        self._update_values()
        
        # Handle window closing
        self.window.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_sensor_frames(self, frame_width, frame_height):
        """Create all sensor display frames"""
        # RPM
        self.RPMframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.RPMframe.grid_propagate(False)
        self.RPMlabel = ttk.Label(self.RPMframe, text="RPM", font=("Arial", 20), justify="left", width=8)
        self.RPMvalue = ttk.Label(self.RPMframe, text=str(self.R.RPM_Value), font=("Arial", 20), width=8, anchor="e")

        # Speed
        self.Speedframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.Speedframe.grid_propagate(False)
        self.Speedlabel = ttk.Label(self.Speedframe, text="Speed", font=("Arial", 20), justify="left", width=8)
        self.Speedvalue = ttk.Label(self.Speedframe, text=str(self.R.SPEED_Value), font=("Arial", 20), width=8, anchor="e")

        # TPS
        self.TPSframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.TPSframe.grid_propagate(False)
        self.TPSlabel = ttk.Label(self.TPSframe, text="TPS", font=("Arial", 20), justify="left", width=8)
        self.TPSvalue = ttk.Label(self.TPSframe, text=str(self.R.TPS_Value), font=("Arial", 20), width=8, anchor="e")

        # Temp
        self.Tempframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.Tempframe.grid_propagate(False)
        self.Templabel = ttk.Label(self.Tempframe, text="Temp", font=("Arial", 20), justify="left", width=8)
        self.Tempvalue = ttk.Label(self.Tempframe, text=str(self.R.TEMP_Value), font=("Arial", 20), width=8, anchor="e")

        # Timing
        self.Timingframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.Timingframe.grid_propagate(False)
        self.Timinglabel = ttk.Label(self.Timingframe, text="Timing", font=("Arial", 20), justify="left", width=8)
        self.Timingvalue = ttk.Label(self.Timingframe, text=str(self.R.TIM_Value), font=("Arial", 20), width=8, anchor="e")

        # Battery
        self.Batteryframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.Batteryframe.grid_propagate(False)
        self.Batterylabel = ttk.Label(self.Batteryframe, text="Battery", font=("Arial", 20), justify="left", width=8)
        self.Batteryvalue = ttk.Label(self.Batteryframe, text=str(self.R.BATT_Value), font=("Arial", 20), width=8, anchor="e")

        # AAC
        self.AACframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.AACframe.grid_propagate(False)
        self.AAClabel = ttk.Label(self.AACframe, text="AAC", font=("Arial", 20), justify="left", width=8)
        self.AACvalue = ttk.Label(self.AACframe, text=str(self.R.AAC_Value), font=("Arial", 20), width=8, anchor="e")

        # Injector
        self.Injectorframe = tk.Frame(self.window, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
        self.Injectorframe.grid_propagate(False)
        self.Injectorlabel = ttk.Label(self.Injectorframe, text="Injector", font=("Arial", 20), justify="left", width=8)
        self.Injectorvalue = ttk.Label(self.Injectorframe, text=str(self.R.INJ_Value), font=("Arial", 20), width=8, anchor="e")

    def _place_sensor_frames(self):
        """Place all sensor frames in the window grid"""
        # RPM
        self.RPMlabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.RPMvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.RPMframe.grid(row=0, column=0, padx=10, pady=10)

        # Speed
        self.Speedlabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.Speedvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.Speedframe.grid(row=0, column=1, padx=10, pady=10)

        # Temp
        self.Templabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.Tempvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.Tempframe.grid(row=0, column=2, padx=10, pady=10)

        # TPS
        self.TPSlabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.TPSvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.TPSframe.grid(row=1, column=0, padx=10, pady=10)

        # Timing
        self.Timinglabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.Timingvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.Timingframe.grid(row=1, column=1, padx=10, pady=10)

        # Battery
        self.Batterylabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.Batteryvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.Batteryframe.grid(row=1, column=2, padx=10, pady=10)

        # AAC
        self.AAClabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.AACvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.AACframe.grid(row=2, column=0, padx=10, pady=10)

        # Injector
        self.Injectorlabel.pack(side=tk.LEFT, padx=10, pady=10)
        self.Injectorvalue.pack(side=tk.RIGHT, padx=10, pady=10)
        self.Injectorframe.grid(row=2, column=1, padx=10, pady=10)

    def _update_values(self):
        """Update all displayed values from the ReadStream"""
        try:
            self.RPMvalue.config(text=str(self.R.RPM_Value))
            self.Speedvalue.config(text=str(self.R.SPEED_Value))
            self.TPSvalue.config(text=str(self.R.TPS_Value))
            self.Tempvalue.config(text=str(self.R.TEMP_Value))
            self.Timingvalue.config(text=str(self.R.TIM_Value))
            self.Batteryvalue.config(text=str(self.R.BATT_Value))
            self.AACvalue.config(text=str(self.R.AAC_Value))
            self.Injectorvalue.config(text=str(self.R.INJ_Value))
            
            # Schedule next update
            self.window.after(100, self._update_values)
        except:
            pass  # Window may have been closed

    def _on_closing(self):
        """Handle window closing"""
        self.window.destroy()

    def run(self):
        """Start the main event loop"""
        self.window.mainloop()
