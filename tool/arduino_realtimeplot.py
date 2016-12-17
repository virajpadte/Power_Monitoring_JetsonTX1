import serial  # import Serial Library
import numpy  # Import numpy
import matplotlib.pyplot as plt  # import matplotlib library
from drawnow import *

powerW = []
port = '/dev/tty.usbmodem1431'
closing_status  = False

#configure the plot
plt.ion()  # Tell matplotlib you want interactive mode to plot live data
plt.rcParams['toolbar'] = 'None'


def handle_close(evt):
    global closing_status
    print('Closed Figure!')
    closing_status  = True

#create a fig
fig = plt.figure(0)
fig.canvas.set_window_title('Window 3D')
fig.canvas.mpl_connect('close_event', handle_close)

#window size for plotting
cnt = 0
window_size = 20
connected = False

try:
    print("trying to connect to device....")
    arduinoData = serial.Serial(port, 115200)
except:
    print "Failed to connect on", port

# ## loop until the arduino tells us it is ready
while not connected:
    serin = arduinoData.read()
    connected = True

def makeFig():  # Create a function that makes our desired plot
    plt.ylim(0, 15)  # Set y min and max values
    plt.title('Plotting power consumption')  # Plot the title
    plt.grid(True)  # Turn the grid on
    plt.ylabel('Power (Watts)')  # Set ylabels
    plt.plot(powerW, 'ro-', label='Power W')  # plot the temperature
    plt.legend(loc='upper right')  # plot the legend



try:
    while not closing_status:  # While loop that loops forever
        if arduinoData.inWaiting(): # Wait here until there is data
            power = arduinoData.readline()  # read the line of text from the serial port
            print(power)
            powerW.append(power)  # Build our tempF array by appending temp readings
            drawnow(makeFig)  # Call drawnow to update our live graph
            plt.pause(.000001)# Pause Briefly. Important to keep drawnow from crashing
            cnt = cnt + 1
            if (cnt >window_size):  # If you have 50 or more points, delete the first one from the array
                powerW.pop(0)  # This allows us to just see the last 50 data points
    print("closing port")
    arduinoData.close()
except KeyboardInterrupt:
    print("closing port")
    arduinoData.close()

