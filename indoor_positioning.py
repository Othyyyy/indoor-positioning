# indoor_positioning.py

# This is an indoor positioning script that enables to estimate the coordinates of a phone inside a classroom using 4 Raspberry Pis connected to the phone's hotspot

# Author : othmane-elannani@hotmail.fr
# Date : 12/06/2023

import tkinter as tk                                                                        # Importing the tkinter library for GUI
from PIL import Image, ImageTk                                                              # Importing the PIL library for image processing
import numpy as np                                                                          # Importing numpy library for numerical computations
from scipy.optimize import minimize                                                         # Importing minimize function from scipy.optimize
import random                                                                               # Importing random library for generating random numbers
import socket                                                                               # Importing socket library for network communication
import subprocess                                                                           # Importing subprocess library for running shell commands
import time                                                                                 # Importing time library for time-related operations
import struct                                                                               # Importing struct library for packing and unpacking binary data

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                        # Creating a socket object
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                                     # Setting socket option
s.bind(("172.20.10.4", 1234))                                                               # Binding the socket to the IP address and port of the main Raspberry Pi
s.listen(5)                                                                                 # Listening for incoming connections

def repeat_function():
  global last_coordinates
  global line_ids
  raspberry_addresses = ["172.20.10.3", "172.20.10.6", "172.20.10.5"]                       # IP addresses of the other Raspberry Pis
  data_list = []                                                                            # Empty list to store received data
  def get_rssi():
    # Run the 'iwconfig wlan0' command and capture the output
    output = subprocess.run(["iwconfig", "wlan0"], stdout = subrpocess.PIPE)                # Running a shell command
    output = output.stdout.decode()                                                         # Decoding the output to string
    # Parse the output to extract the signal level (RSSI) value
    for line in output.split("\n"):                                                         # Splitting the output into lines
      if "Signal level" in line:                                                            # Checking if line contains "Signal level"
        rssi = int(line.split("Signal level=")[1].split(" ")[0])                            # Extracting the signal level value
  rssi = get_rssi()                                                                         # Getting the signal strength
  a = -2.071
  b = -32.817
  d = pow(10, ((rssi-b)/(10*a)))                                                            # Calculating distance based on RSSI
  data_list.append(d)                                                                       # Adding distance to data list
  i = 0
  while len(data_list) !=4:                                                                 # Loop until data for all Raspberry Pis is received
    conn, addr = s.accept()                                                                 # Accepting connection
    if addr[0] == raspberry_addresses[i]:                                                   # Checking if the address matches Raspberry Pi's address
      packed_data = conn.recv(4)                                                            # Receiving 4 bytes of data
      data = struct.unpack("!f", packed_data)[0]                                            # Unpacking the received data
      data_list.append(data)                                                                # Adding received data to the list
      i += 1

# Define the coordinates and radii of the 4 circles
circles = [
    {"x": 0, "y": 0, "r": data_list[0]*100},
    {"x": 0, "y": 700, "r": data_list[1]*100},
    {"x": 800, "y": 0, "r": data_list[2]*100},
    {"x": 800, "y": 700, "r": data_list[3]*100}
]

def objective_function(x):
    point = x
    total_distance = 0
    for circle in circles:
        # Calculate the distance between the point and each circle
        distance = np.sqrt((point[0] - circle["x"])**2 + (point[1] - circle["y"])**2) - circle["r"]
        total_distance += distance**2
    return total_distance

# Define an initial guess for the point's coordinates
initial_guess = [1, 1]

# Use minimize function with Nelder-Mead algorithm to minimize the objective function
result = minimize(objective_function, initial_guess, method='Nelder-Mead')

# Print the coordinates of the phone located between the 4 Raspberry Pis
print("The coordinates of the point that is located between the 4 circles are:", result.x/100, end = "\r")

# Draw classroom dimensions
classroom = tk.Tk()
canvas = tk.Canvas(classroom, height=710, width=810, bg="white")
canvas.pack()

# Draw walls
canvas.create_rectangle(10, 10, 800, 700, fill="white")

# Draw desks
canvas.create_rectangle(100, 550, 160, 650, fill="#6d5a0a")

canvas.create_rectangle(250, 100, 310, 600, fill="#F5F5DD")
canvas.create_rectangle(380, 100, 440, 600, fill="#F5F5DD")
canvas.create_rectangle(510, 100, 570, 600, fill="#F5F5DD")
canvas.create_rectangle(640, 100, 700, 600, fill="#F5F5DD")

# Draw lines1
canvas.create_line(250, 200, 310, 200)
canvas.create_line(250, 300, 310, 300)
canvas.create_line(250, 400, 310, 400)
canvas.create_line(250, 500, 310, 500)

# Draw lines2
canvas.create_line(380, 200, 440, 200)
canvas.create_line(380, 300, 440, 300)
canvas.create_line(380, 400, 440, 400)
canvas.create_line(380, 500, 440, 500)

# Draw lines3
canvas.create_line(510, 200, 570, 200)
canvas.create_line(510, 300, 570, 300)
canvas.create_line(510, 400, 570, 400)
canvas.create_line(510, 500, 570, 500)

# Draw lines4
canvas.create_line(640, 200, 700, 200)
canvas.create_line(640, 300, 700, 300)
canvas.create_line(640, 400, 700, 400)
canvas.create_line(640, 500, 700, 500)

# Draw desk teacher desk
canvas.create_rectangle(90, 500, 95, 620, fill="#6d5a0a")

# Draw chair1
canvas.create_rectangle(315, 60, 320, 145, fill="#6d5a0a")
canvas.create_rectangle(315, 110, 320, 190, fill="#6d5a0a")
canvas.create_rectangle(315, 160, 320, 245, fill="#6d5a0a")
canvas.create_rectangle(315, 210, 320, 290, fill="#6d5a0a")
canvas.create_rectangle(315, 260, 320, 345, fill="#6d5a0a")
canvas.create_rectangle(315, 310, 320, 390, fill="#6d5a0a")
canvas.create_rectangle(315, 360, 320, 445, fill="#6d5a0a")
canvas.create_rectangle(315, 410, 320, 490, fill="#6d5a0a")
canvas.create_rectangle(315, 410, 320, 545, fill="#6d5a0a")
canvas.create_rectangle(315, 410, 320, 590, fill="#6d5a0a")

# Draw chair2
canvas.create_rectangle(445, 110, 450, 145, fill="#6d5a0a")
canvas.create_rectangle(445, 155, 450, 190, fill="#6d5a0a")
canvas.create_rectangle(445, 210, 450, 245, fill="#6d5a0a")
canvas.create_rectangle(445, 255, 450, 290, fill="#6d5a0a")
canvas.create_rectangle(445, 310, 450, 345, fill="#6d5a0a")
canvas.create_rectangle(445, 355, 450, 390, fill="#6d5a0a")
canvas.create_rectangle(445, 410, 450, 445, fill="#6d5a0a")
canvas.create_rectangle(445, 455, 450, 490, fill="#6d5a0a")
canvas.create_rectangle(445, 510, 450, 545, fill="#6d5a0a")
canvas.create_rectangle(445, 555, 450, 590, fill="#6d5a0a")

# Draw chair3
canvas.create_rectangle(575, 110, 580, 145, fill="#6d5a0a")
canvas.create_rectangle(575, 155, 580, 190, fill="#6d5a0a")
canvas.create_rectangle(575, 210, 580, 245, fill="#6d5a0a")
canvas.create_rectangle(575, 255, 580, 290, fill="#6d5a0a")
canvas.create_rectangle(575, 310, 580, 345, fill="#6d5a0a")
canvas.create_rectangle(575, 355, 580, 390, fill="#6d5a0a")
canvas.create_rectangle(575, 410, 580, 445, fill="#6d5a0a")
canvas.create_rectangle(575, 455, 580, 490, fill="#6d5a0a")
canvas.create_rectangle(575, 510, 580, 545, fill="#6d5a0a")
canvas.create_rectangle(575, 555, 580, 590, fill="#6d5a0a")

# Draw chair4
canvas.create_rectangle(705, 110, 710, 145, fill="#6d5a0a")
canvas.create_rectangle(705, 155, 710, 190, fill="#6d5a0a")
canvas.create_rectangle(705, 210, 710, 245, fill="#6d5a0a")
canvas.create_rectangle(705, 255, 710, 290, fill="#6d5a0a")
canvas.create_rectangle(705, 310, 710, 345, fill="#6d5a0a")
canvas.create_rectangle(705, 355, 710, 390, fill="#6d5a0a")
canvas.create_rectangle(705, 410, 710, 445, fill="#6d5a0a")
canvas.create_rectangle(705, 455, 710, 490, fill="#6d5a0a")
canvas.create_rectangle(705, 510, 710, 545, fill="#6d5a0a")
canvas.create_rectangle(705, 555, 710, 590, fill="#6d5a0a")

# Draw blackboard
canvas.create_rectangle(10, 150, 15, 550, fill="#274c43")

# Draw doors
canvas.create_arc(40, -35, 140, 55, start=0, extent=-90, fill="white")
canvas.create_arc(700, -35, 800, 55, start=-180, extent=90, fill="white")

# Insert images
image = Image.open("/home/pi/Desktop/Raspberry.png")
width, height = image.size
new_width = int(width * 0.02)
new_height = int(height * 0.02)
im_resized = image.resize(new_width, new_height)
im_tk = ImageTk.PhotoImage(im_resized)

# Place Raspberry Pi 1
frame = tk.Frame(canvas, width = new_width, height = new_height, bg = None)
frame.pack()

# Create a label to display the image
label = tk.label(frame, image = im_tk)
label.pack()
label.config(bg = "white")

# Place the frame at specific coordinates
frame.place(x = 12, y = 12)

# Place Raspberry Pi 2
frame = tk.Frame(canvas, width = new_width, height = new_height, bg = None)
frame.pack()

# Create a label to display the image
label = tk.label(frame, image = im_tk)
label.pack()
label.config(bg = "white")

# Place the frame at specific coordinates
frame.place(x = 12, y = 660)

# Place Raspberry Pi 3
frame = tk.Frame(canvas, width = new_width, height = new_height, bg = None)
frame.pack()

# Create a label to display the image
label = tk.label(frame, image = im_tk)
label.pack()
label.config(bg = "white")

# Place the frame at specific coordinates
frame.place(x = 770, y = 12)

# Place Raspberry Pi 4
frame = tk.Frame(canvas, width = new_width, height = new_height, bg = None)
frame.pack()

# Create a label to display the image
label = tk.label(frame, image = im_tk)
label.pack()
label.config(bg = "white")

# Place the frame at specific coordinates
frame.place(x = 770, y = 660)

classroom.after(4000, repeat_function)

classroom.mainloop()
