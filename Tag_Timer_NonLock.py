import ctypes
import time
import sched, time

user32 = ctypes.windll.User32
s = sched.scheduler(time.time, time.sleep)



def one_sec():
    global time_logged_in

    if (user32.GetForegroundWindow() % 10 != 0):
        time_logged_in = time_logged_in + 1

    #print(time_logged_in)
    s.enter(1, 1, one_sec)

def get_input():
    global time_logged_in
    cmd = input("Comando ?")
    print("Time Log {}".format(time_logged_in))
    print("Input: {}".format(cmd) )
    s.enter(1, 1, get_input)


time_logged_in = 0

s.enter(1, 1, one_sec)
s.enter(1, 3, get_input)
s.run()
