"""
DTC Window Module
Diagnostic Trouble Code reading and management interface
"""

import tkinter as tk
import tkinter.ttk as ttk
import datetime


class DTCWindow:
    def __init__(self, port):
        self.PORT = port
        
        # Create a new window
        self.window = tk.Tk()
        self.window.title("Diagnostic Trouble Codes (DTC)")
        self.window.geometry("600x500")
        self.window.resizable(False, False)

        # Create main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Diagnostic Trouble Codes", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        # Read DTC button
        read_button = ttk.Button(button_frame, text="Read DTC", command=self.read_dtc, width=15)
        read_button.pack(side=tk.LEFT, padx=5)

        # Erase DTC button
        erase_button = ttk.Button(button_frame, text="Erase DTC", command=self.erase_dtc, width=15)
        erase_button.pack(side=tk.LEFT, padx=5)

        # DTC List frame
        dtc_frame = ttk.LabelFrame(main_frame, text="Stored DTCs", padding="10")
        dtc_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # DTC text box with scrollbar
        scrollbar = ttk.Scrollbar(dtc_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.dtc_box = tk.Text(dtc_frame, height=20, width=60, yscrollcommand=scrollbar.set)
        self.dtc_box.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.dtc_box.yview)

        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)

        self.status_label = ttk.Label(status_frame, text="Ready", foreground="blue")
        self.status_label.pack(side=tk.LEFT)

        # Close button
        close_button = ttk.Button(main_frame, text="Close", command=self.window.destroy)
        close_button.pack(pady=5)

    def read_dtc(self):
        """Read DTCs from ECU"""
        self.status_label.config(text="Reading DTCs...", foreground="blue")
        self.dtc_box.delete('1.0', tk.END)
        
        # Placeholder functionality - would normally read from ECU
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dtc_box.insert(tk.END, f"DTC Read Request: {timestamp}\n")
        self.dtc_box.insert(tk.END, "="*50 + "\n\n")
        self.dtc_box.insert(tk.END, "No DTCs found.\n")
        
        self.status_label.config(text="Read complete", foreground="green")

    def erase_dtc(self):
        """Erase DTCs from ECU"""
        self.status_label.config(text="Erasing DTCs...", foreground="orange")
        
        # Placeholder functionality - would normally erase from ECU
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.dtc_box.insert(tk.END, f"\nDTC Erase Request: {timestamp}\n")
        self.dtc_box.insert(tk.END, "="*50 + "\n")
        self.dtc_box.insert(tk.END, "DTCs cleared successfully.\n")
        self.dtc_box.see(tk.END)
        
        self.status_label.config(text="Erase complete", foreground="green")

    def run(self):
        """Start the main event loop"""
        self.window.mainloop()
