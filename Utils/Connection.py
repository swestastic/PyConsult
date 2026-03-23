import serial
import time

def PortConnect(PORT,COMPORT):
    try:
        PORT = serial.Serial(COMPORT, 9600, timeout=None)
    except OSError:
        if PORT:
            if PORT.is_open:  # Check if PORT is not None and is open
                print("Open")
        else:
            if PORT:
                PORT.open()  # port is not none but is closed
            else:
                print("Init fail")  # Handle the case where PORT is still None
    return PORT

def ECU_Connect(PORT,ECU_CONNECTED,BYPASSED):
    # Attempts to connect to the ECU using the initialization sequence.
    # Then depending on which mode we want we can send the mode-specific
    # initialization sequence
    
    while ECU_CONNECTED == False and BYPASSED == False:
        try:

            PORT.flushInput()
            print("Flushed")
            time.sleep(0.1)
            
            PORT.write(bytes([0xFF,0xFF,0xEF])) #initialization sequence
            print("Write Init")
            time.sleep(0.1)

            Connected = PORT.read_all()

            if Connected == b'\x00\x00\x10':
                print("ECU connected")
                ECU_CONNECTED = True

            else: # NOTE might be able to remove this
                PORT = PortConnect(PORT)

        except ValueError:
            # PORT.open()
            print('Value error')
    return ECU_CONNECTED, BYPASSED