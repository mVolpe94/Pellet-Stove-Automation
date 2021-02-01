#import RPi.GPIO as gpio
import time, os, sys
import mainprocess
from tkinter import *
from tkinter import ttk

augers = 5
heat_exg_blower = 13
combustion_blower = 21
room_air_sensor = 19
outgoing_air_sensor = 26
flame_sensor = 20

#pin setup
# gpio.setup(augers, gpio.OUT)
# gpio.setup(heat_exg_blower, gpio.OUT)
# gpio.setup(combustion_blower, gpio.OUT)
# gpio.setup(room_air_sensor, gpio.IN)
# gpio.setup(outgoing_air_sensor, gpio.IN)
# gpio.setup(flame_sensor, gpio.IN)



class RndGui:
    def __init__(self, root):
        root.title("PELLET STOVE RnD")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)


        #Main Frame
        settings_frame = ttk.Frame(root, padding="15 15 15 15")
        settings_frame.grid(column=0, row=0, sticky=(N, S, E, W))

        #Stats Frame
        stats_frame = ttk.Frame(root, padding="15 15 15 15")
        stats_frame.grid(column=1, row=0, sticky=(N, S, E, W))


        #Auger Test
        auger_run_time = IntVar()
        auger_label = ttk.Label(settings_frame, text='Auger Run Time:')
        auger_label.grid(column=0, row=0, sticky=W)

        self.auger_time = ttk.Entry(settings_frame, width=11, textvariable=auger_run_time)
        self.auger_time.grid(column=1, row=0, padx=5, sticky=(W,E))

        self.auger_button = ttk.Button(settings_frame, text="Run", command=None)
        self.auger_button.grid(column=2, row=0, padx=5, sticky=W)

        auger_run_button = ttk.Button(settings_frame, text="On", command=None)
        auger_run_button.grid(column=1, row=1, padx=5, sticky=W)

        auger_off_button = ttk.Button(settings_frame, text="Off", command=None)
        auger_off_button.grid(column=2, row=1, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=2, pady=8, columnspan=3, sticky=(E,W))

        #Combustion Blower Test
        combustion_blower_label = ttk.Label(settings_frame, text="Combustion Blower Speed:")
        combustion_blower_label.grid(column=0, row=3, sticky=W)

        combustion_blower_off = ttk.Button(settings_frame, text="Off", command=None)
        combustion_blower_off.grid(column=1, row=3, padx=5, sticky=W)

        combustion_blower_low = ttk.Button(settings_frame, text="Low", command=None)
        combustion_blower_low.grid(column=2, row=3, padx=5, sticky=W)

        combustion_blower_med = ttk.Button(settings_frame, text="Medium", command=None)
        combustion_blower_med.grid(column=1, row=4, padx=5, sticky=W)

        combustion_blower_high = ttk.Button(settings_frame, text="High", command=None)
        combustion_blower_high.grid(column=2, row=4, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=5, pady=8, columnspan=3, sticky=(E,W))

        #Starter Test
        starter_run_time = IntVar()
        starter_label = ttk.Label(settings_frame, text="Starter Time Test:")
        starter_label.grid(column=0, row=6, sticky=W)

        starter_time = ttk.Entry(settings_frame, width=11, textvariable=starter_run_time)
        starter_time.grid(column=1, row=6, padx=5, sticky=(W,E))

        starter_button = ttk.Button(settings_frame, text="Run", command=None)
        starter_button.grid(column=2, row=6, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=7, pady=8, columnspan=3, sticky=(E,W))


        #Convection Blower Test
        convection_blower_label = ttk.Label(settings_frame, text="Convection Blower Speed:")
        convection_blower_label.grid(column=0, row=8, sticky=W)

        convection_blower_off = ttk.Button(settings_frame, text="Off", command=None)
        convection_blower_off.grid(column=1, row=8, padx=5, sticky=W)

        convection_blower_low = ttk.Button(settings_frame, text="Low", command=None)
        convection_blower_low.grid(column=2, row=8, padx=5, sticky=W)

        convection_blower_med = ttk.Button(settings_frame, text="Medium", command=None)
        convection_blower_med.grid(column=1, row=9, padx=5, sticky=W)

        convection_blower_high = ttk.Button(settings_frame, text="High", command=None)
        convection_blower_high.grid(column=2, row=9, padx=5, sticky=W)


        #Read Room Temp
        room_air_temp = IntVar()
        room_temp_label = ttk.Label(stats_frame, text=f"Room Temperature: {room_air_temp}")        
        room_temp_label.grid(column=0, row=0, sticky=W)

        read_temp_button = ttk.Button(stats_frame, text="Read Temp", command=lambda: room_air_temp.set(read_temp()))
        read_temp_button.grid(column=1, row=0, sticky=W, padx=5)

def read_temp():
    temp_file = open("TestingEnvironment/temptest.txt")
    lines = temp_file.readlines()
    p = re.compile(r"[t][=](\d*)")
    result = p.search(lines[1])
    room_air_temp = result.group(1)
    room_air_temp = int(room_air_temp) / 1000
    room_air_temp = 9 / 5 * room_air_temp + 32
    return room_air_temp


root = Tk()
RndGui(root)
root.mainloop()

