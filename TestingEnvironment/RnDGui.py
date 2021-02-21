# import RPi.GPIO as gpio
import time, os, sys
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

    def __init__(self, root, running):

        self.running = running

        root.title("PELLET STOVE R+D")
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

        self.auger_low = ttk.Button(
                settings_frame, 
                text="Low", 
                command=lambda: [self.afterkill(self.running), self.auger_modes(4000, False)]
                )
        self.auger_low.grid(
                column=1, 
                row=0, 
                padx=5, 
                sticky=(W,E))

        self.auger_medium = ttk.Button(
                settings_frame, 
                text="Medium", 
                command=lambda: [self.afterkill(self.running), self.auger_modes(3000, False)])
        self.auger_medium.grid(
                column=2, 
                row=0, 
                padx=5, 
                sticky=W)

        auger_off = ttk.Button(
                settings_frame, 
                text="Off", 
                command=lambda: self.auger_modes(0, "OFF"))
        auger_off.grid(column=1, 
                row=1, 
                padx=5, 
                sticky=W)

        auger_high = ttk.Button(
                settings_frame, 
                text="High", 
                command=lambda: [self.afterkill(self.running), self.auger_modes(2000, False)])
        auger_high.grid(
                column=2, 
                row=1, 
                padx=5, 
                sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=2, pady=8, columnspan=3, sticky=(E,W))

        #Combustion Blower Test
        combustion_blower_label = ttk.Label(settings_frame, text="Combustion Blower:")
        combustion_blower_label.grid(column=0, row=3, sticky=W)

        combustion_blower_off = ttk.Button(settings_frame, text="Off", command=lambda: gpio.output(combustion_blower, False))
        combustion_blower_off.grid(column=1, row=3, padx=5, sticky=W)

        combustion_blower_on = ttk.Button(settings_frame, text="On", command=lambda: gpio.output(combustion_blower, True))
        combustion_blower_on.grid(column=2, row=3, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=4, pady=8, columnspan=3, sticky=(E,W))

        #Starter Test
        starter_run_time = IntVar()
        starter_label = ttk.Label(settings_frame, 
            text="Starter Time Test:")
        starter_label.grid(column=0, 
                row=5, 
                sticky=W)

        starter_time = ttk.Entry(settings_frame, 
                width=11, 
                textvariable=starter_run_time)
        starter_time.grid(column=1, 
                row=5, 
                padx=5, 
                sticky=(W,E))

        starter_button = ttk.Button(settings_frame, text="Run", command=lambda: self.starter_timer(starter_run_time.get()))
        starter_button.grid(column=2, row=5, padx=5, sticky=W)

        starter_off_button = ttk.Button(settings_frame, text="Off", command=lambda: gpio.output(starter, False))
        starter_off_button.grid(column=1, row=6, padx=5, sticky=W)

        starter_on_button = ttk.Button(settings_frame, text="On", command=lambda: gpio.output(starter, True))
        starter_on_button.grid(column=2, row=6, padx=5, sticky=W)

        ttk.Separator(settings_frame, orient=HORIZONTAL).grid(row=7, pady=8, columnspan=3, sticky=(E,W))


        #Convection Blower Test
        convection_blower_label = ttk.Label(settings_frame, text="Convection Blower:")
        convection_blower_label.grid(column=0, row=8, sticky=W)

        convection_blower_off = ttk.Button(settings_frame, text="Off", command=lambda: gpio.output(convection_blower, False))
        convection_blower_off.grid(column=1, row=8, padx=5, sticky=W)

        convection_blower_on = ttk.Button(settings_frame, text="On", command=lambda: gpio.output(convection_blower, True))
        convection_blower_on.grid(column=2, row=8, padx=5, sticky=W)


        ttk.Separator(settings_frame, orient=VERTICAL).grid(column=3, row=0, rowspan=9, padx=10, sticky=(N,S))

        #Read Room Temp
        self.room_air_temp = StringVar()
        self.room_air_temp.set(f"Room Temperature: {self.read_temp()}")
        room_temp_label = ttk.Label(stats_frame, textvariable=self.room_air_temp)        
        room_temp_label.grid(column=0, row=0, sticky=W)

        read_temp_button = ttk.Button(stats_frame, text="Read Temp", command=self.read_temp)
        read_temp_button.grid(column=1, row=0, sticky=W, padx=5)


    def auger_timer(self, sec):
            start_time = time.time()
            gpio.output(augers, True)
            if start_time > time.time() + sec:
                gpio.output(augers, False)

    
    def starter_timer(self, sec):
            start_time = time.time()
            gpio.output(starter, True)
            if start_time > time.time() + sec:
                gpio.output(starter, False)


    def auger_modes(self, time, power):
            if not power:
                if power == "OFF":
                    print("OOOOOOFFFFFF")
                    self.afterkill(self.running)
                    return None
                print("auger on")
                print(time)
                power = True
                ms = 5000 - time
                self.running = root.after(ms, self.auger_modes, time, power)
            elif power:
                if power == "OFF":
                    print("OOOOOOFFFFFF")
                    self.afterkill(self.running)
                    return None
                print('auger off')
                print(time)
                power = False
                self.running = root.after(time, self.auger_modes, time, power)


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


