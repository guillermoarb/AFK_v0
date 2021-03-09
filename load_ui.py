import sys
import ctypes
import datetime
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *



class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = QUiLoader().load(QFile("ui/window simple.ui"))

        #Set window icon
        app_icon = QIcon("app_icon.png")
        self.ui.setWindowIcon(app_icon)

        #Frameless window
        #self.ui.setWindowFlags(Qt.FramelessWindowHint)

        # self.label = QLabel(self.ui)
        # pixmap = QPixmap('ui/assets/close_16.png')
        # self.label.setPixmap(pixmap)
        # self.label.setGeometry(500,0,16,16)

    def show_dialog(self):

        dialog = Dialog(self)  # self hace referencia al padre
        dialog.ui.show()

    def toggle_timer(self):
        if timer_1s.isActive() == True:
            update_report()
            timer_1s.stop()
            self.ui.counter_lb.setStyleSheet("color:#BF616A;")
        else:
            timer_1s.start()
            self.ui.counter_lb.setStyleSheet("color:#ECEFF4;")
            


class Dialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.ui = QUiLoader().load(QFile("ui/dialog form.ui"))
        self.setWindowTitle("Config Form")

        self.ui.ok_bt.clicked.connect(self.ok_clicked)
        self.ui.cancel_bt.clicked.connect(self.cancel_clicked)

        #Get the actual text
        #self.ui.project_le.setText(app_window.ui.project_lb.text())
        self.ui.ticket_le.setText(app_window.ui.ticket_lb.text())
        self.ui.task_le.setText("")

    def ok_clicked(self):
        global activity_log
        global activity_name
        global activity_time


        #Update report information
        update_report()

        activity_log = self.ui.task_le.text()
        app_window.ui.task_lb.setText( activity_log)
        #app_window.ui.project_lb.setText( self.ui.project_le.text() )
        activity_name = self.ui.ticket_le.text()
        app_window.ui.ticket_lb.setText(activity_name)

        #Clear the activity timer, this is a new activity
        activity_time = activity_time.replace(0,0,0)

        #Update report information
        update_report()

        self.ui.hide()
        

    def cancel_clicked(self):
        self.ui.hide()

def update_report():

    report_file_name = today.strftime("%m%d%y") + "_AFK.txt"

    with open(report_file_name, "a") as file_object:
        file_object.write("{} {} Activity:{} \t\tLog:{}\n".format(today.strftime("%m/%d/%y"),app_window.ui.counter_lb.text(), app_window.ui.ticket_lb.text(), app_window.ui.task_lb.text() ))

def clickable(widget):
    class Filter(QObject):
        clicked = Signal()
        def eventFilter(self, obj, event):
            if obj == widget:
                if event.type() == QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        return True
            
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked


def task_1s():
    global timer_report_cnt

    #Update the report timer
    timer_report_cnt = timer_report_cnt + 1
    #Every 15 min
    if(timer_report_cnt >= (60 * 15)):
        update_report()
        timer_report_cnt = 0

    update_log_timers()

    #Update log ON time
    app_window.ui.counter_lb.setText(time_log_on.strftime("%H:%M:%S"))

    #Update activity time
    app_window.ui.task_lb.setText("{} {}".format(activity_log, activity_time.strftime("%H:%M:%S")))


def update_log_timers():
    global time_log_on
    global loop_time_sec
    global activity_time
    global time_log_off
    global pause_time

    #Check if screen is not locked
    if (get_lock_status() == False):
        #Update general log ON timer
        updated_clock = clock_add_time_sec(time_log_on, loop_time_sec)
        time_log_on = time_log_on.replace(updated_clock.hour, updated_clock.minute, updated_clock.second)
        #update the activity timer
        updated_clock = clock_add_time_sec(activity_time, loop_time_sec)
        activity_time = time_log_on.replace(updated_clock.hour, updated_clock.minute, updated_clock.second)
    else:
        #Update general log OFF timer
        updated_clock = clock_add_time_sec(time_log_off, loop_time_sec)
        time_log_off = time_log_off.replace(updated_clock.hour, updated_clock.minute, updated_clock.second)
        #update the pause timer
        updated_clock = clock_add_time_sec(pause_time, loop_time_sec)
        pause_time = pause_time.replace(updated_clock.hour, updated_clock.minute, updated_clock.second)



def get_lock_status():
    #Get foreground window ID
    foreground_window = user32.GetForegroundWindow() 
    #Get foreground window text 
    window_text_len = user32.GetWindowTextLengthW(foreground_window)
    window_text = ctypes.create_unicode_buffer(window_text_len + 1)
    
    user32.GetWindowTextW(foreground_window, window_text, window_text_len + 1)
    #Evaluate if the PC is locked and then increase the right timer
    if ((foreground_window == 0) or (window_text.value == "Windows Default Lock Screen")):
        lock_status = True
    else:
        lock_status = False

    return lock_status


def clock_add_time_sec(clock_in, plus_seconds):

    seconds = clock_in.second
    minutes = clock_in.minute
    hours = clock_in.hour

    seconds = seconds + plus_seconds

    if (seconds >= 60):
        minutes = minutes + 1
        seconds = 0

    if (minutes >= 60):
            hours = hours + 1
            minutes = 0

    clock_out = datetime.time(hours,minutes,seconds)

    return clock_out



if __name__ == '__main__':
    #Init the time counters
    time_log_on = datetime.time()
    time_log_off = datetime.time()
    activity_time = datetime.time()
    pause_time = datetime.time()
    today = datetime.datetime.now()

    timer_report_cnt = 0

    time_logged_on_sec = 0
    time_logged_on_min = 0
    time_logged_on_hr = 0
    time_logged_off_sec = 0
    time_logged_off_min = 0
    time_logged_off_hr = 0

    activity_log = "Idle"
    activity_name = "IDLE"

    loop_time_sec = 1

    #ctypes user32 API instance
    user32 = ctypes.windll.User32

    #Create the Qt Application
    app = QApplication(sys.argv)

    # Create a timer and call the task
    timer_1s = QTimer()
    timer_1s.timeout.connect(task_1s)
    timer_1s.start(1000 * loop_time_sec)

    # Create and show the main window
    app_window = Window()

    #Get and update the date
    today = datetime.datetime.now()
    #app_window.ui.date_lb.setText(today.strftime("%d %b"))

    clickable(app_window.ui.task_lb).connect(app_window.show_dialog)
    clickable(app_window.ui.ticket_lb).connect(app_window.show_dialog)
    #clickable(app_window.ui.project_lb).connect(app_window.show_dialog)
    clickable(app_window.ui.counter_lb).connect(app_window.toggle_timer)

    app_window.ui.show()


    # Run the main Qt loop
    app.exec_()
    sys.exit()
