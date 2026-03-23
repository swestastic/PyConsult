"""
Landing Window Module
Main startup window for PyConsult with connection and mode selection
"""

import tkinter as tk
import tkinter.ttk as ttk
import serial.tools.list_ports
import time
from Utils.Connection import PortConnect, ECU_Connect


class LandingWindow:
    def __init__(self, config_file='configJSON.json'):
        self.PORT = None
        self.COMPORT = None
        self.BYPASSED = False
        self.ECU_CONNECTED = False
        self.TEST_MODE = False
        self.config_file = config_file
        
        # GUI parameters
        ipadx = 40
        ipady = 40
        padx = 10
        pady = 10
        geox = 460
        geoy = 360
        buttonwidth = 20

        # Create main window
        self.window = tk.Tk()
        self.window.title("PyConsult GUI")
        self.window.geometry(str(geox) + "x" + str(geoy))
        self.window.resizable(False, False)
        self.window.focus_force()

        # Create buttons and labels
        selectionlabel = ttk.Label(self.window, text="Select Mode!", width=10, font=("Arial", 16))
        ds_button = ttk.Button(self.window, text="Data Stream", width=buttonwidth, command=self.launch_data_stream)
        dtc_button = ttk.Button(self.window, text="DTCs", width=buttonwidth, command=self.launch_dtc)
        test_button = ttk.Button(self.window, text="Testing", width=buttonwidth, command=self.launch_testing)
        setting_button = ttk.Button(self.window, text="Settings", width=buttonwidth, command=self.launch_settings)
        self.connect_button = ttk.Button(self.window, text="Connect", width=buttonwidth, command=self.connection)
        
        # Initialize COM ports list with Test Mode option
        com_ports = ["Test Mode (Random Data)"] + [str(port) for port in serial.tools.list_ports.comports()]
        self.coms_box = ttk.Combobox(self.window, values=com_ports)

        # Place widgets in grid
        ds_button.grid(row=1, column=0, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        dtc_button.grid(row=2, column=0, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        test_button.grid(row=1, column=1, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        setting_button.grid(row=2, column=1, ipadx=ipadx, ipady=ipady, padx=padx, pady=pady)
        self.connect_button.grid(row=3, column=1, ipadx=ipadx/4, ipady=ipady/4, padx=padx, pady=pady)
        self.coms_box.grid(row=3, column=0, ipadx=ipadx/4, ipady=ipady/4, padx=padx, pady=pady)
        selectionlabel.grid(row=0, column=0, columnspan=2)

        # Start background task for updating COM ports
        self._update_com_ports()

    def _update_com_ports(self):
        """Update the COM ports list periodically"""
        if not self.ECU_CONNECTED and not self.TEST_MODE:
            com_ports = ["Test Mode (Random Data)"] + [str(port) for port in serial.tools.list_ports.comports()]
            self.coms_box.config(values=com_ports)
            self.window.after(500, self._update_com_ports)

    def connection(self):
        """Handle connection to ECU or enable test mode"""
        self.COMPORT = self.coms_box.get()
        
        # Check if Test Mode is selected
        if self.COMPORT == "Test Mode (Random Data)":
            self.TEST_MODE = True
            self.ECU_CONNECTED = True
            
            # Create a popup window to show test mode enabled
            popup = tk.Toplevel(self.window)
            popup.title("Test Mode Enabled")
            popup.geometry("300x100")
            label = ttk.Label(popup, text="Test Mode - Random Data Enabled")
            label.pack(pady=20)
            button = ttk.Button(popup, text="OK", command=popup.destroy)
            button.pack(pady=10)
            
            self.connect_button.config(text="Test Mode")
            self.connect_button.config(state=tk.DISABLED)
            return
        
        # Normal connection flow for real device
        start_time = time.time()
        i = 1
        
        while self.PORT is None:
            print("Connecting")
            self.PORT = PortConnect(self.PORT, self.COMPORT)
            print(self.PORT)
            time.sleep(0.25)
            i = 1 + i % 6
            self.connect_button.config(text="Connecting" + "."*i)
            self.window.update_idletasks()
            if time.time() - start_time > 3:
                break
                
        if self.PORT is not None:
            print("Connected to port")
            self.ECU_CONNECTED, self.BYPASSED = ECU_Connect(self.PORT, self.ECU_CONNECTED, self.BYPASSED)

        # Create a popup window to show connection status
        popup = tk.Toplevel(self.window)
        popup.title("Connection Status")
        popup.geometry("300x100")
        
        if self.ECU_CONNECTED:
            label = ttk.Label(popup, text="Connected to ECU")
            self.connect_button.config(text="Connected")
            self.connect_button.config(state=tk.DISABLED)
        else:
            label = ttk.Label(popup, text="Failed to connect to ECU")
            self.connect_button.config(text="Connect")

        label.pack(pady=20)
        button = ttk.Button(popup, text="OK", command=popup.destroy)
        button.pack(pady=10)

    def _check_connection(self):
        """Check if ECU is connected, show error if not"""
        if not self.ECU_CONNECTED:
            popup = tk.Toplevel(self.window)
            popup.title("Error")
            popup.geometry("300x100")
            ttk.Label(popup, text="Please connect to the ECU first").pack(pady=10)
            ttk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)
            return False
        return True

    def launch_data_stream(self):
        """Launch data stream window"""
        if self._check_connection():
            from Windows.DataStreamWindow import DataStreamWindow
            DataStreamWindow(self.PORT, self.config_file, test_mode=self.TEST_MODE)

    def launch_dtc(self):
        """Launch DTC window"""
        if self._check_connection():
            from Windows.DTCWindow import DTCWindow
            DTCWindow(self.PORT).run()

    def launch_testing(self):
        """Launch testing window"""
        if self._check_connection():
            from Windows.TestingWindow import TestingWindow
            TestingWindow(self.PORT)

    def launch_settings(self):
        """Launch settings window"""
        from Windows.SettingsWindow import SettingsWindow
        SettingsWindow(self.config_file)

    def run(self):
        """Start the main event loop"""
        self.window.mainloop()
