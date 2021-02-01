#import RPi.GPIO as gpio
import time, os, sys
from tkinter import *
from tkinter import ttk


#tasks
# When room temp is lower than set temperature, activate heat exchange blower, add pellets
# If heat exchange intake delta t is low, increase feul into burn pot (activate auger)
# If heat exchagne intake is same temp as set temp, add more fuel when temp set is higher than room temp
# 1 second cycles
# check all temps every minute
#

#Variable Setup
room_air_temp = 65


# IO Setup

#pin numbers
augers = 5
heat_exg_blower = 13
combustion_blower = 21
room_air_sensor = 19
#outgoing_air_sensor = 26
burn_pot_sensor = 20

#pin setup
# gpio.setup(auger1, gpio.OUT)
# gpio.setup(auger2, gpio.OUT)
# gpio.setup(heat_exg_blower, gpio.OUT)
# gpio.setup(combustion_blower, gpio.OUT)
# gpio.setup(room_air_sensor, gpio.IN)
# gpio.setup(outgoing_air_sensor, gpio.IN)
# gpio.setup(burn_pot_sensor, gpio.IN)

class PelletStove:

    def __init__(self, root):
        root.title("Pellet Stove")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        stats_frame = ttk.Frame(root, padding="15 15 15 15")
        stats_frame.grid(column=0, row=0, sticky=(N, W, E, S))

        room_temp_label = ttk.Label(stats_frame, text=f"Room Temperature: {room_air_temp}" + u"\N{DEGREE SIGN}")
        room_temp_label.grid(column=0, row=0, sticky=W)

        








root = Tk()
PelletStove(root)
root.mainloop()


def read_temp():
    temp_file = open("/sys/bus/w1/devices/28-021466be69ff/w1_slave")
    lines = temp_file.readlines()
    p = re.compile(r"[t][=](\d*)")
    result = p.search(lines[1])
    room_air_temp = result.group(1)
    room_air_temp = int(room_air_temp) / 1000
    room_air_temp = 9 / 5 * room_air_temp + 32
    return room_air_temp


def deltaTtimer(room_air_temp):
    old_room_temp = room_air_temp #Take input of incoming air temp
    time.sleep(5)
    new_temp = 66 #Take input of incoming air
    deltaT = new_temp - old_room_temp
    return deltaT

deltaT = deltaTtimer(room_air_temp)
if deltaT <= 0:
    pass
    #Add more pellets
elif deltaT <= 1:
    pass
elif deltaT > 1:
    pass


def deltaTtimed(room_air_temp):
    start_time = time.time()
    current_room_temp = read_temp() #Take input of incoming air temp
    target_temp = current_room_temp + 1
    while current_room_temp <= target_temp:
        current_room_temp = read_temp()#Take input of incoming air
        time.sleep(1)
    end_time = time.time()
    return end_time - start_time
    
    