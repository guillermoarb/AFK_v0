import sys
import ctypes
import datetime
from PySide6.QtUiTools import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


import json_report

class Window(QWidget):


    def __init__(self):
        super(Window, self).__init__()
        self.ui = QUiLoader().load(QFile("window simple.ui"))

        #Set window icon
        app_icon = QIcon("app_icon.png")
        self.ui.setWindowIcon(app_icon)

        self.window_geometry = self.ui.geometry()
 
        screen_geometry = QGuiApplication.primaryScreen().geometry()

        self.window_cords = (screen_geometry.width() - self.window_geometry.width() , screen_geometry.height() - self.window_geometry.height())

        #Set frame less
        self.ui.setWindowFlags(Qt.FramelessWindowHint)

        #Move to righ down corner
        self.ui.move(self.window_cords[0] , self.window_cords[1] - 50 )

        #Variable to indicate if menu is open
        self.menu_open = False

    def show_dialog(self):
        self.window_cords = self.ui.pos().toTuple()
        dialog.ui.show()
        dialog.ui.move( self.window_cords[0] , self.window_cords[1] +  self.window_geometry.height() - dialog.ui.geometry().height() - 80 )

    def toggle_timer(self):
        if timer_1s.isActive() == True:
            update_report()
            timer_1s.stop()
            self.ui.counter_lb.setStyleSheet("color:#BF616A;")
        else:
            timer_1s.start()
            self.ui.counter_lb.setStyleSheet("color:#ECEFF4;")
    
    def show_menu(self):

        if (self.menu_open == False):
            self.menu_open = True
            self.window_cords = self.ui.pos().toTuple()
            menu.ui.show()
            menu.ui.move( self.window_cords[0] + self.window_geometry.width() - menu.ui.geometry().width()   , self.window_cords[1] +  self.window_geometry.height() - menu.ui.geometry().height() - 80 )

        else:
            self.menu_open = False
            menu.menu_self_close()


class Menu(QDialog):

    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        self.ui = QUiLoader().load(QFile("menu.ui"))
        self.setWindowTitle("Menu")

        #Set window icon
        app_icon = QIcon("app_icon.png")
        self.ui.setWindowIcon(app_icon)

        #Set frame less
        self.ui.setWindowFlags(Qt.FramelessWindowHint)

        
        clickable(self.ui.menu_close).connect(self.menu_close)
        clickable(self.ui.menu_save).connect(self.menu_save)
        clickable(self.ui.menu_edit_activity).connect(self.menu_edit_activity)
        clickable(self.ui.menu_open_json_report).connect(self.menu_open_json_report)
        clickable(self.ui.menu_generate_week_report).connect(self.menu_generate_week_report)

    def menu_close(self):
        QCoreApplication.quit()

    def menu_save(self):
        #Update report information
        update_report()
        self.ui.hide()
        
    def menu_edit_activity(self):
        app_window.show_dialog()
        self.ui.hide()

    def menu_open_json_report(self):
        report.json_report_open()
        self.ui.hide()

    def menu_generate_week_report(self):
        report.report_generate_report()
        self.ui.hide()

    def menu_self_close(self):
        self.ui.hide()


class Dialog(QDialog):


    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.ui = QUiLoader().load(QFile("dialog form.ui"))
        self.setWindowTitle("Config Form")

        #Set window icon
        app_icon = QIcon("app_icon.png")
        self.ui.setWindowIcon(app_icon)

        self.ui.ok_bt.clicked.connect(self.ok_clicked)
        self.ui.cancel_bt.clicked.connect(self.cancel_clicked)
        self.ui.activity_cb.editTextChanged.connect(self.load_tasks)

        #Get the actual text
        #self.ui.project_le.setText(app_window.ui.project_lb.text())
        #self.ui.ticket_le.setText(app_window.ui.ticket_lb.text())
        #self.ui.task_le.setText("")

        #Set frame less
        self.ui.setWindowFlags(Qt.FramelessWindowHint)

        #Load activities in activity combo box
        self.ui.activity_cb.addItems(report.activity_get_all())
    
    def load_tasks(self):
        print(report.task_get_all(self.ui.activity_cb.currentText()))
        self.ui.task_cb.addItems(report.task_get_all(self.ui.activity_cb.currentText()))



    def ok_clicked(self):
        global activity_log
        global activity_name
        global activity_time
        global project_name

        #Update report information
        update_report()

        activity_log = self.ui.task_cb.currentText()
        app_window.ui.task_lb.setText( activity_log)
        project_name = self.ui.project_le.text()
        activity_name = self.ui.activity_cb.currentText()
        app_window.ui.ticket_lb.setText(activity_name)

        #Clear the activity timer, this is a new activity
        activity_time = update_task(activity_name, activity_log )

        #Update report information
        update_report()

        self.ui.hide()
        

    def cancel_clicked(self):
        self.ui.hide()

def update_report():
    global project_name

    report.report_add_activity(app_window.ui.ticket_lb.text(), project_name)
    
    report.report_update_item(  activity_time.strftime("%H:%M:%S"), 
                                activity_log, 
                                today.strftime("%m/%d/%y"), 
                                app_window.ui.ticket_lb.text() )

    report.report_update_week()
    report.report_update_worked_time()
    report.report_update_day(time_log_on.strftime("%H:%M:%S"))
    report.report_print_json()

    """
    report_file_name = today.strftime("%m%d%y") + "_AFK.txt"

    with open(report_file_name, "a") as file_object:
        file_object.write("{} {} Activity:{} \t\tLog:{}\n".format(today.strftime("%m/%d/%y"),app_window.ui.counter_lb.text(), app_window.ui.ticket_lb.text(), app_window.ui.task_lb.text() ))
    """


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

def update_task(activity_name, task):
    
    task_time = report.report_get_task_time(activity_name, activity_log)

    return task_time


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

def init_timers_from_report(activity_name, activity_log):
    global time_log_on
    global activity_time


    #Init the time log on in case this is not the first time during the day
    time_log_on = report.report_get_today_time()
    activity_time = report.report_get_task_time(activity_name, activity_log)


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
    activity_name = "Activity"
    project_name = "None"

    loop_time_sec = 1

    #ctypes user32 API instance
    user32 = ctypes.windll.User32

    #Create the Qt Application
    app = QApplication(sys.argv)

    # Create a timer and call the task
    timer_1s = QTimer()
    timer_1s.timeout.connect(task_1s)
    timer_1s.start(1000 * loop_time_sec)

    #Create a report object, empty or get the actual report
    report = json_report.Report()

    # Create and show the main window
    app_window = Window()
    menu = Menu()
    dialog = Dialog()

    
  

    #Get and update the date
    today = datetime.datetime.now()
    #app_window.ui.date_lb.setText(today.strftime("%d %b"))

    clickable(app_window.ui.task_lb).connect(app_window.show_dialog)
    clickable(app_window.ui.ticket_lb).connect(app_window.show_dialog)
    #clickable(app_window.ui.project_lb).connect(app_window.show_dialog)
    clickable(app_window.ui.counter_lb).connect(app_window.toggle_timer)
    clickable(app_window.ui.menu_lb).connect(app_window.show_menu)

    app_window.ui.show()


    #Init log_on timer
    init_timers_from_report(activity_name, activity_log)

    # Run the main Qt loop
    app.exec_()
    sys.exit()
