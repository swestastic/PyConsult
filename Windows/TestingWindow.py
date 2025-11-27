"""
Testing Window Module
Manual ECU command testing interface
"""

import tkinter as tk
import tkinter.ttk as ttk


class TestingWindow:
    def __init__(self, port):
        self.PORT = port
        
        # Create a new window
        self.window = tk.Tk()
        self.window.title("Testing")
        self.window.geometry("800x600")
        self.window.resizable(False, False)

        # Create input box for sending data
        self.input_box = ttk.Entry(self.window)
        self.input_box.pack(pady=10)

        # Create a button to send the data
        send_button = ttk.Button(self.window, text="Send", command=self.send_data)
        send_button.pack(pady=10)

        # Create a text box to display the response
        self.response_box = tk.Text(self.window, height=20, width=100)
        self.response_box.pack(pady=10)

        # Create a button to clear the response box
        clear_button = ttk.Button(self.window, text="Clear", command=self.clear_response)
        clear_button.pack(pady=10)

        # Create a button to close the window
        close_button = ttk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.pack(pady=10)

    def send_data(self):
        """Send data to ECU"""
        data = self.input_box.get()
        print(data)
        print(type(data))
        # PORT.write(bytes(data))
        print(bytes(int(data, 16)))

        # response = self.PORT.read_all()
        # self.response_box.insert(tk.END, response)
        # self.response_box.insert(tk.END, "\n")

    def clear_response(self):
        """Clear the response box"""
        self.response_box.delete('1.0', tk.END)

    def run(self):
        """Start the main event loop"""
        self.window.mainloop()
