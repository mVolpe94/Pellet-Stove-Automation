import mainprocess, os
from multiprocessing import Process, Pipe

# to use multiple pipes with one function, must define new connection names 
# and call the recieve for each
# must have a pipeline for each sensor used 

if __name__ == '__main__':
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    parent_temp_conn, child_temp_conn = Pipe()
    p = Process(target=mainprocess.sensor_check, args=[child_temp_conn])
    p.start()
    for _ in range(10):
        print(parent_temp_conn.recv())
        print(parent_temp_conn.recv())
    p.join()

