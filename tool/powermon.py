import sys
import glob
import serial
import ttk
import tkFileDialog
from Tkinter import *

#for plotting we need these:
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from drawnow import *


class MainView:

    #CLASS VARIABLES:
    closing_status = False
    powerW = []

    def __init__(self, master):
        self.master = master

        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        port = StringVar()
        port.set(" ")  # initial value

        ttk.Label(mainframe, text="Select Port").grid(column=1, row=1, sticky=W)
        port_list = self.serial_ports()
        port_list.insert(0," ")
        print(port_list)
        port = StringVar(mainframe)
        port.set(port_list[1])  # default value
        dropdown = ttk.OptionMenu(mainframe,port,*port_list)
        dropdown.configure(width=20)
        dropdown.grid(column=2, row=1, sticky=W)

        ttk.Button(mainframe, text="Realtime Plot",  command=lambda: self.real_time_plotting(port)).grid(column=1, row=2, sticky=W)

        ttk.Button(mainframe, text="Record Session", command=lambda: self.record_session(port)).grid(column=2, row=2, sticky=W)
        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def record_session(self,port):
        print("record_session")
        port = port.get()
        print("record port",port)
        self.newWindow = Toplevel(root)
        self.app = record_session(self.newWindow,port)

    def serial_ports(self):
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

    def handle_close(self):
        print('Closed Figure!')
        self.closing_status = True

    def real_time_plotting(self,port):

        cnt = 0
        window_size = 20
        connected = False


        port = port.get()
        print("real_time_plotting")
        print("realtime data port", port)
        try:
            print("trying to connect to device....")
            ser = serial.Serial(port, 115200)
        except:
            print "Failed to connect on", port

        # ## loop until the arduino tells us it is ready
        while not connected:
            serin = ser.read()
            connected = True

        try:
            while not self.closing_status:  # While loop that loops forever
                if ser.inWaiting():  # Wait here until there is data
                    power = ser.readline()  # read the line of text from the serial port
                    print(power)
                    self.powerW.append(power)  # Build our tempF array by appending temp readings
                    drawnow(self.makeFig)  # Call drawnow to update our live graph
                    plt.pause(.000001)  # Pause Briefly. Important to keep drawnow from crashing
                    cnt = cnt + 1
                    if (cnt > window_size):  # If you have 50 or more points, delete the first one from the array
                        self.powerW.pop(0)  # This allows us to just see the last 50 data points
            print("closing port")
            ser.close()
        except KeyboardInterrupt:
            print("closing port")
            ser.close()

    def makeFig(self):  # Create a function that makes our desired plot

        # configure the plot
        plt.ion()  # Tell matplotlib you want interactive mode to plot live data
        plt.rcParams['toolbar'] = 'None'

        # create a fig
        #fig = plt.figure(0)
        #fig.canvas.set_window_title('Window 3D')
        #fig.canvas.mpl_connect('close_event', self.handle_close())

        plt.ylim(0, 15)  # Set y min and max values
        plt.title('Plotting power consumption')  # Plot the title
        plt.grid(True)  # Turn the grid on
        plt.ylabel('Power (Watts)')  # Set ylabels
        plt.plot(self.powerW, 'ro-', label='Power W')  # plot the temperature
        plt.legend(loc='upper right')  # plot the legend

    def handle_close(self):
        print('Closed Figure!')
        self.closing_status = True

class record_session:
    #class variable:
    path  = ""

    def __init__(self, master,port):
        self.master = master
        self.master.title("Session parameters")
        mainframe = ttk.Frame(self.master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)

        print("passed port", port)
        duration = StringVar()
        autoplot = IntVar()
        autoplot.set(0)  # initial value

        ttk.Button(mainframe, text="Select a location to store session.csv file", command=self.select_dir).grid(column=1, row=1, sticky=W)
        ttk.Label(mainframe, text="Record Duration in seconds:").grid(column=1, row=2, sticky=W)
        duration_entry_box = ttk.Entry(mainframe, width=5, textvariable=duration)
        duration_entry_box.grid(column=2, row=2, sticky=W)
        ttk.Checkbutton(mainframe, text="Auto Plotting enabled", variable=autoplot).grid(column=1, row=3, sticky=W)
        ttk.Button(mainframe, text="Start recording", command=lambda: self.record(port,autoplot)).grid(column=1, row=4, sticky=W)

        for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

    def select_dir(self):
        global path
        print("select dir")
        path = tkFileDialog.askdirectory()
        #append file name to the path
        if len(path):
            path = path + "/session.csv"
            print(path)

    def record(self,port,autoplot):
        global path
        print("recording")
        autoplot_status = autoplot.get()
        print("autoplot_status", autoplot_status)
        connected = False
        ## establish connection to the serial port that your arduino
        ## is connected to.
        try:
            print("trying to connect to device....")
            ser = serial.Serial(port, 115200)
        except:
            print "Failed to connect on", port

        # ## loop until the arduino tells us it is ready
        while not connected:
            serin = ser.read(self)
            connected = True

        #open text file to store the power values
        text_file = open(path, 'w')
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

if __name__ == '__main__':
    root = Tk()
    root.title("Power Monitoring tool")
    main = MainView(root)
    root.mainloop()

