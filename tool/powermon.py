import sys
import glob
import serial
import ttk
import tkFileDialog
from Tkinter import *



class MainView:
    def __init__(self, master):
        self.master = master

        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        ttk.Label(mainframe, text="Select Port").grid(column=1, row=1, sticky=W)
        ttk.Button(mainframe, text="Realtime Plot", command=self.real_time_plotting).grid(column=1, row=2, sticky=W)

        ttk.Button(mainframe, text="Record Session", command=self.record_session).grid(column=2, row=2, sticky=W)
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def real_time_plotting(self):
        print("real_time_plotting")
        #self.newWindow = Toplevel(root)
        #self.app = Create_host(self.newWindow)

    def record_session(self):
        print("record_session")
        self.newWindow = Toplevel(root)
        self.app = record_session(self.newWindow)


class record_session:
    def __init__(self, master):
        self.master = master
        self.master.title("Session parameters")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        duration = StringVar()

        ttk.Button(mainframe, text="Select a location to store session.csv file", command=self.select_dir).grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Record Duration in seconds:").grid(column=1, row=2, sticky=W)
        duration_entry_box = ttk.Entry(mainframe, width=5, textvariable=duration)
        duration_entry_box.grid(column=2, row=2, sticky=W)
        ttk.Button(mainframe, text="Start recording", command=self.record).grid(column=1, row=4, sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def select_dir(self):
        print("select dir")
        path = tkFileDialog.askdirectory()
        #append file name to the path
        if len(path):
            path = path + "/session.csv"
            print(path)

    def record(self):
        print("recording")

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    result = ports
    return result


def establish_connection(device):
    connected = False
    ## establish connection to the serial port that your arduino
    ## is connected to.
    try:
        print("trying to connect to device....")
        ser = serial.Serial(device, 115200)
    except:
        print "Failed to connect on", device

    ## loop until the arduino tells us it is ready
    while not connected:
        serin = ser.read()
        connected = True

    #open text file to store the power values
    text_file = open("data.csv", 'w')
    #read serial data from arduino and
    #write it to the text file 'Data.csv'
    try:
        while True:
            if ser.inWaiting():
                # Read a line and convert it from b'xxx\r\n' to xxx
                line = ser.readline()
                print(line)
                if line:  # If it isn't a blank line
                    text_file.write(line)
        text_file.close()
    except KeyboardInterrupt:
        print("closing port")
        ser.close()
        pass

if __name__ == '__main__':
    root = Tk()
    root.title("Power Monitoring tool")
    main = MainView(root)
    root.mainloop()

    #listofports = serial_ports()
    #print(type(listofports))
    #print(listofports)
    #establish_connection('/dev/tty.usbmodem1431')

