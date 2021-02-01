from multiprocessing import Process, Pipe
import time, os, sys, re

def read_temp():
    temp_file = open("TestingEnvironment/temptest.txt")
    lines = temp_file.readlines()
    p = re.compile(r"[t][=](\d*)")
    result = p.search(lines[1])
    room_air_temp = result.group(1)
    room_air_temp = int(room_air_temp) / 1000
    room_air_temp = 9 / 5 * room_air_temp + 32
    return room_air_temp

def read_ash():
    pass




def sensor_check(conn):
    running = True
    while running:
        temp = read_temp()
        conn.send(temp)
        
        time.sleep(1)
        break
    while running:
        temp = read_temp()
        temp += 1
        conn.send(temp)
        time.sleep(1)


