"""
Settings Window Module
Configuration window for PyConsult settings
"""

import tkinter as tk
import tkinter.ttk as ttk
from Utils.Settings import Load_Config, Save_Config


class SettingsWindow:
    def __init__(self, config_file='configJSON.json'):
        self.config_file = config_file
        self.config = Load_Config(self.config_file)
        
        # GUI parameters
        padx = 5
        pady = 5
        geox = 460
        geoy = 300

        # Create settings window
        self.window = tk.Tk()
        self.window.title("PyConsult Settings")
        self.window.geometry(str(geox) + "x" + str(geoy))
        self.window.resizable(False, False)
        self.window.focus_force()

        # Create input boxes for settings
        self.rpm_warning = ttk.Entry(self.window, text="RPM Warning")
        self.rpm_warning.insert(0, self.config["RPM_Warning"])

        self.temp_warning = ttk.Entry(self.window, text="Temperature Warning")
        self.temp_warning.insert(0, self.config["Coolant_Warning"])

        self.speed_units = ttk.Combobox(self.window, values=["MPH", "KPH"])
        self.speed_units.set(self.config["Units_Speed"])

        self.temp_units = ttk.Combobox(self.window, values=["F", "C"])
        self.temp_units.set(self.config["Units_Temp"])

        self.stock_tire_width = ttk.Entry(self.window, text="Stock Tire Width")
        self.stock_tire_width.insert(0, self.config["Stock_Tire_Width"])
        
        self.stock_tire_ar = ttk.Entry(self.window, text="Stock Aspect Ratio")
        self.stock_tire_ar.insert(0, self.config["Stock_Tire_AR"])
        
        self.stock_tire_diam = ttk.Entry(self.window, text="Stock Tire Diameter")
        self.stock_tire_diam.insert(0, self.config["Stock_Tire_Diam"])

        self.new_tire_width = ttk.Entry(self.window, text="New Tire Width")
        self.new_tire_width.insert(0, self.config["New_Tire_Width"])
        
        self.new_tire_ar = ttk.Entry(self.window, text="New Aspect Ratio")
        self.new_tire_ar.insert(0, self.config["New_Tire_AR"])
        
        self.new_tire_diam = ttk.Entry(self.window, text="New Tire Diameter")
        self.new_tire_diam.insert(0, self.config["New_Tire_Diam"])

        self.stock_diff = ttk.Entry(self.window, text="Stock Final Drive")
        self.stock_diff.insert(0, self.config["Stock_Final"])
        
        self.new_diff = ttk.Entry(self.window, text="New Final Drive")
        self.new_diff.insert(0, self.config["New_Final"])

        # Create labels for input boxes
        rpm_warning_label = ttk.Label(self.window, text="RPM Warning")
        temp_warning_label = ttk.Label(self.window, text="Temperature Warning")
        speed_units_label = ttk.Label(self.window, text="Speed Units")
        temp_units_label = ttk.Label(self.window, text="Temp Units")

        stock_label = ttk.Label(self.window, text="Stock")
        new_label = ttk.Label(self.window, text="New")

        ar_label = ttk.Label(self.window, text="AR")
        width_label = ttk.Label(self.window, text="Width")
        diam_label = ttk.Label(self.window, text="Diameter")
        diff_label = ttk.Label(self.window, text="Final Drive")

        # Place input boxes and labels in grid
        # Warnings
        rpm_warning_label.grid(row=0, column=0, padx=padx, pady=pady)
        self.rpm_warning.grid(row=0, column=1, padx=padx, pady=pady)

        temp_warning_label.grid(row=1, column=0, padx=padx, pady=pady)
        self.temp_warning.grid(row=1, column=1, padx=padx, pady=pady)

        # Units
        speed_units_label.grid(row=2, column=0, padx=padx, pady=pady)
        self.speed_units.grid(row=2, column=1, padx=padx, pady=pady)

        temp_units_label.grid(row=3, column=0, padx=padx, pady=pady)
        self.temp_units.grid(row=3, column=1, padx=padx, pady=pady)

        # Speed correction
        stock_label.grid(row=12, column=1)
        new_label.grid(row=12, column=2)

        width_label.grid(row=13, column=0)
        self.stock_tire_width.grid(row=13, column=1, padx=padx, pady=pady)
        self.new_tire_width.grid(row=13, column=2, padx=padx, pady=pady)

        ar_label.grid(row=14, column=0)
        self.stock_tire_ar.grid(row=14, column=1, padx=padx, pady=pady)
        self.new_tire_ar.grid(row=14, column=2, padx=padx, pady=pady)

        diam_label.grid(row=15, column=0)
        self.stock_tire_diam.grid(row=15, column=1, padx=padx, pady=pady)
        self.new_tire_diam.grid(row=15, column=2, padx=padx, pady=pady)

        # Differential
        diff_label.grid(row=16, column=0, padx=padx, pady=pady)
        self.stock_diff.grid(row=16, column=1, padx=padx, pady=pady)
        self.new_diff.grid(row=16, column=2, padx=padx, pady=pady)

        # Save button
        save_button = ttk.Button(self.window, text="Save", command=self.save_settings)
        save_button.grid(row=17, column=1)

    def save_settings(self):
        """Save all settings to config file"""
        self.config["RPM_Warning"] = self.rpm_warning.get()
        self.config["Coolant_Warning"] = self.temp_warning.get()
        self.config["Units_Speed"] = self.speed_units.get()
        self.config["Units_Temp"] = self.temp_units.get()
        self.config["Stock_Tire_Width"] = self.stock_tire_width.get()
        self.config["Stock_Tire_AR"] = self.stock_tire_ar.get()
        self.config["Stock_Tire_Diam"] = self.stock_tire_diam.get()
        self.config["New_Tire_Width"] = self.new_tire_width.get()
        self.config["New_Tire_AR"] = self.new_tire_ar.get()
        self.config["New_Tire_Diam"] = self.new_tire_diam.get()
        self.config["Stock_Final"] = self.stock_diff.get()
        self.config["New_Final"] = self.new_diff.get()
        Save_Config(self.config_file, self.config)

        # Create a popup window to indicate that settings have been saved
        popup = tk.Toplevel(self.window)
        popup.title("Save Confirmation")
        popup.geometry("200x100")
        label = ttk.Label(popup, text="Settings saved successfully!")
        label.pack(pady=20)
        ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
        ok_button.pack()

    def run(self):
        """Start the main event loop"""
        self.window.mainloop()
