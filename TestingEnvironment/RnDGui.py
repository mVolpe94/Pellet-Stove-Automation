# import RPi.GPIO as gpio
import time, os, sys, re
import matplotlib.pyplot as plt
import utility
import mainprocess
from tkinter import *
from tkinter import ttk

augers = 5
starter = 6
convection_blower = 13
combustion_blower = 21
room_air_sensor = 19
outgoing_air_sensor = 26
flame_sensor = 20



#pin setup
# gpio.setup(augers, gpio.OUT)
# gpio.setup(convection_blower, gpio.OUT)
# gpio.setup(combustion_blower, gpio.OUT)
# gpio.setup(room_air_sensor, gpio.IN)
# gpio.setup(outgoing_air_sensor, gpio.IN)
# gpio.setup(flame_sensor, gpio.IN)

button = 0
running = None

class RndGui:

    def __init__(self, root, auger_running):

        self.auger_running = auger_running

        root.title("PELLET STOVE R+D")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

############### Main Frame

        #Main Frame
        settings_frame = ttk.Frame(root, padding="15 15 15 15")
        settings_frame.grid(column=0, row=0, sticky=(N, S, E, W))


        #Auger Test
        auger_label = ttk.Label(settings_frame, text='Augers:')
        auger_label.grid(column=0, row=0, sticky=W)

        self.auger_low = ttk.Button(settings_frame, text="Low", command=lambda: [self.afterkill(self.auger_running), self.auger_modes(4000, False)])
        self.auger_low.grid(column=1, row=0, padx=5, sticky=(W,E))

        self.auger_medium = ttk.Button(settings_frame, text="Medium", command=lambda: [self.afterkill(self.auger_running), self.auger_modes(3000, False)])
        self.auger_medium.grid(column=2, row=0, padx=5, sticky=W)

        auger_off = ttk.Button(settings_frame, text="Off", command=lambda: self.auger_modes(0, "OFF"))
        auger_off.grid(column=1, row=1, padx=5, sticky=W)

        auger_high = ttk.Button(settings_frame, text="High", command=lambda: [self.afterkill(self.auger_running), self.auger_modes(2000, False)])
        auger_high.grid(column=2, row=1, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=2, pady=8, columnspan=3, sticky=(E,W))

        #Combustion Blower Test
        combustion_blower_label = ttk.Label(settings_frame, text="Combustion Blower:")
        combustion_blower_label.grid(column=0, row=3, sticky=W)

        combustion_blower_off = ttk.Button(settings_frame, text="Off", command=lambda: self.gpio_toggle("out", combustion_blower, False))
        combustion_blower_off.grid(column=1, row=3, padx=5, sticky=W)

        combustion_blower_on = ttk.Button(settings_frame, text="On", command=lambda: self.gpio_toggle("out", combustion_blower, True))
        combustion_blower_on.grid(column=2, row=3, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=4, pady=8, columnspan=3, sticky=(E,W))

        #Starter Test
        starter_run_time = IntVar()
        starter_label = ttk.Label(settings_frame, text="Starter Time Test:")
        starter_label.grid(column=0, row=5, sticky=W)

        starter_time = ttk.Entry(settings_frame, width=11, textvariable=starter_run_time)
        starter_time.grid(column=1, row=5, padx=5, sticky=(W,E))

        starter_button = ttk.Button(settings_frame, text="Run", command=lambda: self.starter_timer(starter_run_time.get()))
        starter_button.grid(column=2, row=5, padx=5, sticky=W)

        starter_off_button = ttk.Button(settings_frame, text="Off", command=lambda: self.gpio_toggle("out", starter, False))
        starter_off_button.grid(column=1, row=6, padx=5, sticky=W)

        starter_on_button = ttk.Button(settings_frame, text="On", command=lambda: self.gpio_toggle("out", starter, True))
        starter_on_button.grid(column=2, row=6, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=7, pady=8, columnspan=3, sticky=(E,W))


        #Convection Blower Test
        convection_blower_label = ttk.Label(settings_frame, text="Convection Blower:")
        convection_blower_label.grid(column=0, row=8, sticky=W)

        convection_blower_off = ttk.Button(settings_frame, text="Off", command=lambda: self.gpio_toggle("out", convection_blower, False))
        convection_blower_off.grid(column=1, row=8, padx=5, sticky=W)

        convection_blower_on = ttk.Button(settings_frame, text="On", command=lambda: self.gpio_toggle("out", convection_blower, True))
        convection_blower_on.grid(column=2, row=8, padx=5, sticky=W)


        ttk.Separator(settings_frame, orient=VERTICAL).grid(column=3, row=0, rowspan=9, padx=10, sticky=(N,S))

############### Stats Frame

        #Stats Frame
        stats_frame = ttk.Frame(root, padding="15 15 15 15")
        stats_frame.grid(column=1, row=0, sticky=(N, S, E, W))

        #Read Room Temp
        self.room_air_temp = StringVar()
        self.room_air_temp.set(f"Room Temperature: {self.read_temp()}")
        room_temp_label = ttk.Label(stats_frame, textvariable=self.room_air_temp)        
        room_temp_label.grid(column=0, row=0, sticky=W)

        read_temp_button = ttk.Button(stats_frame, text="Read Temp", command=self.read_temp)
        read_temp_button.grid(column=1, row=0, sticky=W, padx=5)

        auto_graph_button = ttk.Button(stats_frame, text="Auto Graph", command=None)##Add command
        auto_graph_button.grid(column=1, row=1, sticky=W, padx=5)

        ttk.Separator(stats_frame, orient=HORIZONTAL).grid(column=0, row=2, pady=8, columnspan=2, sticky=(W,E))

        #Auger Status

        self.auger_state = StringVar()
        self.auger_state.set(f"Auger Speed: Off")
        auger_speed = ttk.Label(stats_frame, textvariable=self.auger_state)
        auger_speed.grid(column=0, row=3, sticky=E)

        #Combustion Blower Status

        self.combustion_blower_state = StringVar()
        self.combustion_blower_state.set("Combustion Blower: Off")
        combustion_blower_status = ttk.Label(stats_frame, textvariable=self.combustion_blower_state)
        combustion_blower_status.grid(column=0, row=4, sticky=E)

        #Starter Status

        self.starter_state = StringVar()
        self.starter_state.set("Starter: Off")
        starter_status = ttk.Label(stats_frame, textvariable=self.starter_state)
        starter_status.grid(column=0, row=5, sticky=E)

        #Convection Blower Status

        self.convection_blower_state = StringVar()
        self.convection_blower_state.set("Convection Blower: Off")
        convection_blower_status = ttk.Label(stats_frame, textvariable=self.convection_blower_state)
        convection_blower_status.grid(column=0, row=6, sticky=E)

#     def auger_timer(self, sec):
#         start_time = time.time()
#         gpio.output(augers, True)
#         if start_time > time.time() + sec:
#             gpio.output(augers, False)


    def gpio_toggle(self, dir, pin, state):
        if dir == "in":
            #gpio.input(pin, state)
            ...
        elif dir == "out":
            #gpio.output(pin, state)
            self.status_check(pin, state)

    
    def status_check(self, pin, state):
        cur_state = ""
        if state == True:
            cur_state = "On"
        elif state == False:
            cur_state = "Off"
          
        if pin == starter:
            self.starter_state.set(f"Starter: {cur_state}")
        elif pin == combustion_blower:
            self.combustion_blower_state.set(f"Combustion Blower: {cur_state}")
        elif pin == convection_blower:
            self.convection_blower_state.set(f"Convection Blower: {cur_state}")


    def starter_timer(self, sec):
        start_time = time.time()
        gpio.output(starter, True)
        if start_time > time.time() + sec:
            gpio.output(starter, False)


    def auger_modes(self, time, power):
        if not power:
            self.auger_state_check(time)
            if power == "OFF":
                print("OOOOOOFFFFFF")
                self.afterkill(self.auger_running)
                return None
            print("auger on")
            print(time)
            power = True
            ms = 5000 - time
            self.auger_running = root.after(ms, self.auger_modes, time, power)
        elif power:
            self.auger_state_check(time)
            if power == "OFF":
                print("OOOOOOFFFFFF")
                self.afterkill(self.auger_running)
                return None
            print('auger off')
            print(time)
            power = False
            self.auger_running = root.after(time, self.auger_modes, time, power)


    def auger_state_check(self, time):
        mode = "Off"
        if time == 2000:
            mode = "High"
        elif time == 3000:
            mode = "Med"
        elif time == 4000:
            mode = "Low"
        self.auger_state.set(f"Auger Speed: {mode}")


    def afterkill(self, function):
        try:
            root.after_cancel(function)
        except(ValueError):
            print("Function doesn't exsist in memory. Yet...")


    def read_temp(self):
        #REPLACE PATH WITH PI PATH TO
        temp_file = open("TestingEnvironment/temptest.txt")
        lines = temp_file.readlines()
        p = re.compile(r"[t][=](\d*)")
        result = p.search(lines[1])
        room_air = result.group(1)
        room_air = int(room_air) / 1000
        room_air = 9 / 5 * room_air + 32
        self.room_air_temp.set(f"Room Temperature: {room_air}")
        return room_air
        


root = Tk()
RndGui(root, None)
root.mainloop()


