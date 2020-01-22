#! /usr/bin/env python3

import serial
import sys
import time
import os
from datetime import datetime

baud = 2000000
filename = ""

if(len(sys.argv) > 4 or len(sys.argv) < 2):
    print("Incorrect arguments. run with -h to see options")
    sys.exit(1)

print("--------------Simple Serial Monitor-------------")
if str(sys.argv[1]) == "-h":
    print("Useage:")
    print("    monitor.py <port> <baud_rate> <logfile>\n")
    print("    port        serial port of system to listen")
    print("                eg COM3 on windows, USB0 on linux (omit `/dev/tty` prefix on linux)")
    print("    baud_rate   baud rate of serial link")
    print("                Baudrate defaults to 2M Baud if not specified")
    print("    logfile     specify path to save log file")
    print("                Defaults to Logs folder in the current directory")
    print("    ctrl+c      quit\n")
    print("    Example 1: Create a serial monitor on /dev/ttyUSB0 @ 115200 baud")
    print("        'monitor.py USB0 115200'")
    print("    Example 2: Create a serial monitor on COM3 on windows @ 2000000 Baud")
    print("        'monitor.py COM3'")
    sys.exit(1)

# if(len(sys.argv) == 3):
    
if(len(sys.argv) == 4):
    baud = sys.argv[2]
    filename = os.path.join(os.getcwd(), sys.argv[3], "Logs") 
os.system('cls' if os.name == 'nt' else 'clear')

print("This session: Port: /dev/tty" + str(sys.argv[1]) + " Baud: " + str(baud) + " Log: " + str(filename))
print("------------------------------------------------")

serial_prefix = "/dev/tty"
if os.name == 'nt':
    serial_prefix = ""

if not os.path.exists(filename):
    os.makedirs(filename)

with open(os.path.join(filename, (datetime.now()).strftime("%d%m%Y_%H%M%S")), "a+", encoding="utf-8") as f:

    with serial.Serial(serial_prefix + sys.argv[1], baud, timeout=1) as ser:
        while True:
            try:
                time.sleep(0.05)
                bytesToRead = ser.inWaiting() # get the amount of bytes available at the input queue
                if bytesToRead:
                    line = ser.read(ser.inWaiting())
                    print(line.decode('utf-8'), end="")
                    
                    f.write(str(line))

                    # print(line.strip().decode('utf-8'))
            except UnicodeDecodeError:
                thing =1
                # dont do anything..
            except serial.SerialException:
                print("Monitor: Disconnected (Serial exception)")
                serial.close()
                print("Log path: " + str(f.name))
                sys.exit(1)
            except IOError:
                print("Monitor: Disconnected (I/O Error)")
                serial.close()
                print("Log path: " + str(f.name))
                sys.exit(1)
            except KeyboardInterrupt:
                print("Monitor: Keyboard Interrupt. Exiting Now...")
                print("Log path: " + str(f.name))
                sys.exit(1)
                
    
    f.close()