import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x_values = []  # just time
index = 0
y_values = []  # voltage

# Configure your serial port
port = 'COM4'  # Replace with your serial port
baudrate = 9600  # Set the baud rate (must match the device's baud rate)

# Initialize the serial connection
ser = serial.Serial(port, baudrate, timeout=1)  # Adjust timeout as necessary

plt.style.use('fivethirtyeight')


#plt.figure(figsize=(10, 5))  # Set width to 10 inches and height to 5 inches


class CapacitorDataArray:  # class to store the serial monitor output records most recent size bits of data
    def __init__(self, size):
        self.size = size
        self.x_values = []
        self.voltage_values = []
        self.index = 0

    def push(self, voltage):
        # if queue full then remove oldest recorded voltage to make room for newest
        if len(self.x_values) >= self.size:
            self.voltage_values.pop(0)
        else:  # increment index
            self.index += 1
            self.x_values.append(self.index)
        self.voltage_values.append(voltage)


capData = CapacitorDataArray(size=200)
useFixedSizeGraph = True

def animate(i):
    global index

    try:
        if ser.in_waiting > 0:  # Check if there is data waiting
            line = ser.readline().decode('utf-8').rstrip()  # Read and decode the line
            print(line)  # Print the line
            voltage = float(line)

            plt.cla()
            plt.xlabel("Interval")  # Set the x label
            plt.ylabel("Voltage")  # Set the y label
            if useFixedSizeGraph:
                capData.push(voltage)
                plt.plot(capData.x_values, capData.voltage_values)
            else:
                y_values.append(voltage)
                x_values.append(index)
                index += 1
                plt.plot(x_values, y_values)
    except:
        print('byte missing')

    #plt.tight_layout()


try:
    # Give some time for the serial connection to establish
    time.sleep(2)  # Wait for the connection to establish

    ani = FuncAnimation(plt.gcf(), animate, interval=10)
    plt.show()
except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()  # Always close the port when done
