import sys
import ctypes
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QWidget, QApplication, QLabel
from PySide2.QtGui import QIcon





def task_1s():
    global time_logged_on
    global time_logged_off

    if (user32.GetForegroundWindow() != 0):
        time_logged_on = time_logged_on + 1
        
    else:
        time_logged_off = time_logged_off + 1

    print("LOG ON {}".format(time_logged_on))
    print("LOG OFF {}".format(time_logged_off))






if __name__ == '__main__':

    time_logged_on = 0
    time_logged_off = 0

    #Lock API
    user32 = ctypes.windll.User32

    #Create the Qt Application
    app = QApplication(sys.argv)


    # Create a timer and call the task
    timer_1s = QTimer()
    timer_1s.timeout.connect(task_1s)
    timer_1s.start(1000)


    # Run the main Qt loop
    app.exec_()
    sys.exit()



