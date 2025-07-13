# Import packages
import tkinter as tk
import tkinter.ttk as ttk

# from ctypes import windll # This allows us to change the DPI settings for the application

import numpy as np
import serial
import serial.tools.list_ports
import time
import threading
from Utils.Settings import Load_Config, Save_Config

from Utils.Connection import PortConnect, ECU_Connect
from Utils.Read import ReadStream

# Load data from config
CONF = 'configJSON.json' # config file
Config = Load_Config(CONF)

PORT,COMPORT,BYPASSED, ECU_CONNECTED, landing = None, None, False, False, None

### Data Stream Window ###
def DataStreamWindow():
    global PORT,BYPASSED, ECU_CONNECTED, Config, R
    R = ReadStream(port=PORT, daemon=True)
    # Create a new window
    DataStream = tk.Tk()
    DataStream.title("Data Stream")
    DataStream.geometry("800x600")
    DataStream.resizable(False, False)

    # Create labels for the names and the data with a box around them
    frame_width = 200
    frame_height = 100

    ############################################

    RPMframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    RPMframe.grid_propagate(False)  # Prevent frame from resizing to fit contents
    RPMlabel = ttk.Label(RPMframe, text="RPM", font=("Arial", 20),justify="left")
    RPMvalue = ttk.Label(RPMframe, text=R.RPM_Value, font=("Arial", 20))

    Speedframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    Speedframe.grid_propagate(False)
    Speedlabel = ttk.Label(Speedframe, text="Speed", font=("Arial", 20),justify="left")
    Speedvalue = ttk.Label(Speedframe, text=str(R.SPEED_Value), font=("Arial", 20))

    TPSframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    TPSframe.grid_propagate(False)
    TPSlabel = ttk.Label(TPSframe, text="TPS", font=("Arial", 20),justify="left")
    TPSvalue = ttk.Label(TPSframe, text=str(R.TPS_Value), font=("Arial", 20))

    Tempframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    Tempframe.grid_propagate(False)
    Templabel = ttk.Label(Tempframe, text="Temp", font=("Arial", 20),justify="left")
    Tempvalue = ttk.Label(Tempframe, text=str(R.TEMP_Value), font=("Arial", 20))

    Timingframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    Timingframe.grid_propagate(False)
    Timinglabel = ttk.Label(Timingframe, text="Timing", font=("Arial", 20),justify="left")
    Timingvalue = ttk.Label(Timingframe, text=str(R.TIM_Value), font=("Arial", 20))

    Batteryframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    Batteryframe.grid_propagate(False)
    Batterylabel = ttk.Label(Batteryframe, text="Battery", font=("Arial", 20),justify="left")
    Batteryvalue = ttk.Label(Batteryframe, text=str(R.BATT_Value), font=("Arial", 20))

    AACframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    AACframe.grid_propagate(False)
    AAClabel = ttk.Label(AACframe, text="AAC", font=("Arial", 20),justify="left")
    AACvalue = ttk.Label(AACframe, text=str(R.AAC_Value), font=("Arial", 20))

    Injectorframe = tk.Frame(DataStream, relief=tk.RIDGE, borderwidth=2, width=frame_width, height=frame_height)
    Injectorframe.grid_propagate(False)
    Injectorlabel = ttk.Label(Injectorframe, text="Injector", font=("Arial", 20),justify="left")
    Injectorvalue = ttk.Label(Injectorframe, text=str(R.INJ_Value), font=("Arial", 20))

    ############################################

    # Place the labels in the window
    RPMlabel.pack(side=tk.LEFT, padx=10, pady=10)
    RPMvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    RPMframe.grid(row=0, column=0, padx=10, pady=10)

    Speedlabel.pack(side=tk.LEFT, padx=10, pady=10)
    Speedvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    Speedframe.grid(row=0, column=1, padx=10, pady=10)

    Templabel.pack(side=tk.LEFT, padx=10, pady=10)
    Tempvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    Tempframe.grid(row=0, column=2, padx=10, pady=10)

    TPSlabel.pack(side=tk.LEFT, padx=10, pady=10)
    TPSvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    TPSframe.grid(row=1, column=0, padx=10, pady=10)

    Timinglabel.pack(side=tk.LEFT, padx=10, pady=10)
    Timingvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    Timingframe.grid(row=1, column=1, padx=10, pady=10)

    Batterylabel.pack(side=tk.LEFT, padx=10, pady=10)
    Batteryvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    Batteryframe.grid(row=1, column=2, padx=10, pady=10)

    AAClabel.pack(side=tk.LEFT, padx=10, pady=10)
    AACvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    AACframe.grid(row=2, column=0, padx=10, pady=10)

    Injectorlabel.pack(side=tk.LEFT, padx=10, pady=10)
    Injectorvalue.pack(side=tk.RIGHT, padx=10, pady=10)
    Injectorframe.grid(row=2, column=1, padx=10, pady=10)

    # # Start the updates in a separate thread

    DataStream.mainloop()


def launch_data_stream():
    global landing, PORT, ECU_CONNECTED, BYPASSED
    # landing.destroy() # close original window
    
    if ECU_CONNECTED == False:
        PopUp = tk.Tk()
        PopUp.title("Error")
        PopUp.geometry("300x100")
        ttk.Label(PopUp, text="Please connect to the ECU first").pack(pady=10)
        ttk.Button(PopUp, text="OK", command=PopUp.destroy).pack(pady=10)

    else:
        DataStreamWindow()

def launch_dtc():
    global landing, PORT, ECU_CONNECTED, BYPASSED
    # landing.destroy() # close original window
    
    if ECU_CONNECTED == False:
        PopUp = tk.Tk()
        PopUp.title("Error")
        PopUp.geometry("300x100")
        ttk.Label(PopUp, text="Please connect to the ECU first").pack(pady=10)
        ttk.Button(PopUp, text="OK", command=PopUp.destroy).pack(pady=10)

    else:
        DataStreamWindow()

def launch_testing():
    global landing, PORT, ECU_CONNECTED, BYPASSED
    # landing.destroy() # close original window
    
    if ECU_CONNECTED == False:
        PopUp = tk.Tk()
        PopUp.title("Error")
        PopUp.geometry("300x100")
        ttk.Label(PopUp, text="Please connect to the ECU first").pack(pady=10)
        ttk.Button(PopUp, text="OK", command=PopUp.destroy).pack(pady=10)

    else:
        #DataStreamWindow()
        TestingWindow()
    
# def launch_settings():
    # global landing
    # landing.destroy() # close original window
    # SettingsWindow()

def Connection():
    global PORT,BYPASSED, ECU_CONNECTED, coms_box, COMPORT, connect_button,landing
    # This function is triggered by pressing connect on landing screen
    start_time = time.time() # Start timer for connection
    COMPORT = coms_box.get()
    i = 1
    while PORT is None:
        print("Connecting")
        PORT = PortConnect(PORT,COMPORT) # Connect to the port
        print(PORT)
        time.sleep(0.25)
        i = 1 + i % 6
        connect_button.config(text="Connecting" + "."*i)
        landing.update_idletasks()
        if time.time() - start_time > 3: # If it takes longer than 3 seconds, break
            break
    if PORT is not None:
        print("Connected to port")
        ECU_CONNECTED,BYPASSED = ECU_Connect(PORT,ECU_CONNECTED,BYPASSED) # Connect to the ECU 

    # Create a popup window to show connection status
    popup = tk.Tk()
    popup.title("Connection Status")
    popup.geometry("300x100")
    if ECU_CONNECTED == True:
        label = ttk.Label(popup, text="Connected to ECU")
        connect_button.config(text="Connected")
        connect_button.config(state=tk.DISABLED)
    else:
        label = ttk.Label(popup, text="Failed to connect to ECU")
        connect_button.config(text="Connect")

    label.pack(pady=20)
    button = ttk.Button(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)
    popup.mainloop()

def Save_Settings(CONF,Config):
    global rpm_warning, temp_warning, speed_units, temp_units, stock_tire_width, stock_tire_ar, stock_tire_diam, new_tire_width, new_tire_ar, new_tire_diam, stock_diff, new_diff
    Config["RPM_Warning"] = rpm_warning.get()
    Config["Coolant_Warning"] = temp_warning.get()
    Config["Units_Speed"] = speed_units.get()
    Config["Units_Temp"] = temp_units.get()
    Config["Stock_Tire_Width"] = stock_tire_width.get()
    Config["Stock_Tire_AR"] = stock_tire_ar.get()
    Config["Stock_Tire_Diam"] = stock_tire_diam.get()
    Config["New_Tire_Width"] = new_tire_width.get()
    Config["New_Tire_AR"] = new_tire_ar.get()
    Config["New_Tire_Diam"] = new_tire_diam.get()
    Config["Stock_Final"] = stock_diff.get()
    Config["New_Final"] = new_diff.get()
    Save_Config(CONF, Config)
    
    # Create a popup window to indicate that settings have been saved
    popup = tk.Toplevel()
    popup.title("Save Confirmation")
    popup.geometry("200x100")
    label = ttk.Label(popup, text="Settings saved successfully!")
    label.pack(pady=20)
    ok_button = ttk.Button(popup, text="OK", command=popup.destroy)
    ok_button.pack()
    popup.mainloop()

### Settings Window ###
def SettingsWindow():
    global rpm_warning, temp_warning, speed_units, temp_units, stock_tire_width, stock_tire_ar, stock_tire_diam, new_tire_width, new_tire_ar, new_tire_diam, stock_diff, new_diff
    Config = Load_Config(CONF)
    # GUI parameters
    padx = 5
    pady = 5
    geox = 460
    geoy = 300

    # Create settings window
    settings = tk.Tk()
    settings.title("PyConsult Settings")
    settings.geometry(str(geox) + "x" + str(geoy))
    settings.resizable(False,False)
    settings.focus_force()
    # windll.shcore.SetProcessDpiAwareness(1) # Uncomment to enable DPI awareness, Windows only, needs items resized.

    # Create input boxes for settings
    rpm_warning = ttk.Entry(settings, text="RPM Warning")
    rpm_warning.insert(0,Config["RPM_Warning"])

    temp_warning = ttk.Entry(settings, text="Temperature Warning")
    temp_warning.insert(0,Config["Coolant_Warning"])

    speed_units = ttk.Combobox(settings, values=["MPH","KPH"])
    speed_units.set(Config["Units_Speed"])

    temp_units = ttk.Combobox(settings, values=["F","C"])
    temp_units.set(Config["Units_Temp"])

    stock_tire_width = ttk.Entry(settings, text="Stock Tire Width")
    stock_tire_width.insert(0,Config["Stock_Tire_Width"])
    stock_tire_ar = ttk.Entry(settings, text="Stock Aspect Ratio")
    stock_tire_ar.insert(0,Config["Stock_Tire_AR"])
    stock_tire_diam = ttk.Entry(settings, text="Stock Tire Diameter")
    stock_tire_diam.insert(0,Config["Stock_Tire_Diam"])

    new_tire_width = ttk.Entry(settings, text="New Tire Width")
    new_tire_width.insert(0,Config["New_Tire_Width"])
    new_tire_ar = ttk.Entry(settings, text="New Aspect Ratio")
    new_tire_ar.insert(0,Config["New_Tire_AR"])
    new_tire_diam = ttk.Entry(settings, text="New Tire Diameter")
    new_tire_diam.insert(0,Config["New_Tire_Diam"])

    stock_diff = ttk.Entry(settings, text="Stock Final Drive")
    stock_diff.insert(0,Config["Stock_Final"])
    new_diff = ttk.Entry(settings, text="New Final Drive")
    new_diff.insert(0,Config["New_Final"])

    # Create labels for input boxes
    rpm_warning_label = ttk.Label(settings, text="RPM Warning")
    temp_warning_label = ttk.Label(settings, text="Temperature Warning")

    speed_units_label = ttk.Label(settings, text="Speed Units")
    temp_units_label = ttk.Label(settings, text="Temp Units")

    stock_label = ttk.Label(settings, text="Stock")
    stock_label.grid(row=12,column=1)
    new_label = ttk.Label(settings, text="New")
    new_label.grid(row=12,column=2)

    ar_label = ttk.Label(settings,text="AR")
    width_label = ttk.Label(settings,text="Width")
    diam_label = ttk.Label(settings,text="Diameter")
    diff_label = ttk.Label(settings,text="Final Drive")

    # Place input boxes and labels in grid
    #Warnings
    rpm_warning.grid(row=0,column=1, padx=padx, pady=pady)
    rpm_warning_label.grid(row=0,column=0, padx=padx, pady=pady)

    temp_warning.grid(row=1,column=1, padx=padx, pady=pady)
    temp_warning_label.grid(row=1,column=0, padx=padx, pady=pady)

    #Units
    speed_units.grid(row=2,column=1, padx=padx, pady=pady)
    speed_units_label.grid(row=2,column=0, padx=padx, pady=pady)

    temp_units.grid(row=3,column=1, padx=padx, pady=pady)
    temp_units_label.grid(row=3,column=0, padx=padx, pady=pady)

    # Speed correction
    #Place labels
    width_label.grid(row=13,column=0)
    ar_label.grid(row=14,column=0)
    diam_label.grid(row=15,column=0)

    stock_tire_width.grid(row=13,column=1, padx=padx, pady=pady)
    stock_tire_ar.grid(row=14,column=1, padx=padx, pady=pady)
    stock_tire_diam.grid(row=15,column=1, padx=padx, pady=pady)

    new_tire_width.grid(row=13,column=2, padx=padx, pady=pady)
    new_tire_ar.grid(row=14,column=2, padx=padx, pady=pady)
    new_tire_diam.grid(row=15,column=2, padx=padx, pady=pady)

    # differential
    stock_diff.grid(row=16,column=1, padx=padx, pady=pady)
    new_diff.grid(row=16,column=2, padx=padx, pady=pady)
    diff_label.grid(row=16,column=0, padx=padx, pady=pady)

    # Save button
    save_button = ttk.Button(settings, text="Save", command=lambda: Save_Settings(CONF, Config))
    save_button.grid(row=17,column=1)

    settings.mainloop()


### Main landing/startup window ###
# GUI parameters
def LandingWindow():
    global coms_box, landing, connect_button
    ipadx = 40
    ipady = 40
    padx = 10
    pady = 10
    geox = 460
    geoy = 360
    buttonwidth = 20

    # Create main window
    landing = tk.Tk()
    landing.title("PyConsult GUI")
    landing.geometry(str(geox) + "x" + str(geoy))
    landing.resizable(False,False)
    landing.focus_force()

    # Create buttons and labels
    selectionlabel = ttk.Label(landing, text="Select Mode!",width=10,font=("Arial", 16))
    ds_button = ttk.Button(landing, text="Data Stream",width=buttonwidth,command=launch_data_stream)
    dtc_button = ttk.Button(landing, text="DTCs",width=buttonwidth,command=launch_dtc)
    test_button = ttk.Button(landing, text="Testing",width=buttonwidth,command=launch_testing)
    setting_button = ttk.Button(landing, text="Settings",width=buttonwidth,command=SettingsWindow)
    connect_button = ttk.Button(landing, text="Connect",width=buttonwidth,command=Connection)
    coms_box = ttk.Combobox(landing, values=serial.tools.list_ports.comports())

    ds_button.grid(row=1,column=0, ipadx=ipadx, ipady=ipady,padx=padx, pady=pady) 
    dtc_button.grid(row=2,column=0, ipadx=ipadx, ipady=ipady,padx=padx, pady=pady) 
    test_button.grid(row=1,column=1, ipadx=ipadx, ipady=ipady,padx=padx, pady=pady) 
    setting_button.grid(row=2,column=1, ipadx=ipadx, ipady=ipady,padx=padx, pady=pady) 
    connect_button.grid(row=3,column=1, ipadx=ipadx/4, ipady=ipady/4,padx=padx, pady=pady)
    coms_box.grid(row=3,column=0, ipadx=ipadx/4, ipady=ipady/4,padx=padx, pady=pady)

    selectionlabel.grid(row=0,column=0,columnspan=2)

    landing.mainloop()


def send_data():
    global PORT, input_box, response_box
    data = input_box.get()
    print(data)
    print(type(data))
    # PORT.write(bytes(data))
    print(bytes(int(data,16)))

    # response = PORT.read_all()
    # response_box.insert(tk.END, response)
    # response_box.insert(tk.END, "\n")

def TestingWindow():
    # This window will eventually be repurposed for DTC, but right now it will let us send code manually to the ECU for testing

    global PORT, ECU_CONNECTED, BYPASSED, landing, input_box, response_box
    # Create a new window
    Testing = tk.Tk()
    Testing.title("Testing")
    Testing.geometry("800x600")
    Testing.resizable(False, False)

    # Create input box for sending data
    input_box = ttk.Entry(Testing)
    input_box.pack(pady=10)

    # Create a button to send the data
    send_button = ttk.Button(Testing, text="Send",command=send_data)
    send_button.pack(pady=10)

    # Create a text box to display the response
    response_box = tk.Text(Testing, height=20, width=100)
    response_box.pack(pady=10)

    # Create a button to clear the response box
    clear_button = ttk.Button(Testing, text="Clear")
    clear_button.pack(pady=10)

    # Create a button to close the window
    close_button = ttk.Button(Testing, text="Close", command=Testing.destroy)
    close_button.pack(pady=10)


    Testing.mainloop()

def update_tasks():
    global ECU_CONNECTED, landing, coms_box, DataStream
    global RPMvalue, Speedvalue, TPSvalue, Tempvalue, Timingvalue, Batteryvalue, AACvalue, Injectorvalue, R
    while ECU_CONNECTED == False and landing is not None:
        # this chunk updates the combobox with the available com ports every 0.5 seconds
        time.sleep(0.5)
        coms_box.config(values=serial.tools.list_ports.comports()) # update coms box value
        landing.update_idletasks()

    while ECU_CONNECTED == True:
        # This updates all of the values in our data stream window
        RPMvalue.config(text=str(R.RPM_Value))
        Speedvalue.config(text=str(R.SPEED_Value))
        TPSvalue.config(text=str(R.TPS_Value))
        Tempvalue.config(text=str(R.TEMP_Value))
        Timingvalue.config(text=str(R.TIM_Value))
        Batteryvalue.config(text=str(R.BATT_Value))
        AACvalue.config(text=str(R.AAC_Value))
        Injectorvalue.config(text=str(R.INJ_Value))
        DataStream.update_idletasks()

tasks_thread = threading.Thread(target=update_tasks, daemon=True)
tasks_thread.start()

LandingWindow()