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
            file_log()
            timer_1s.stop()
            self.ui.counter_lb.setStyleSheet("color:#BF616A;")
        else:
            timer_1s.start()
            self.ui.counter_lb.setStyleSheet("color:#8FBCBB;")
            


class Dialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(Dialog, self).__init__(*args, **kwargs)
        self.ui = QUiLoader().load(QFile("ui/dialog form.ui"))
        self.setWindowTitle("Config Form")

        self.ui.ok_bt.clicked.connect(self.ok_clicked)
        self.ui.cancel_bt.clicked.connect(self.cancel_clicked)

        #Get the actual text
        self.ui.project_le.setText(app_window.ui.project_lb.text())
        self.ui.ticket_le.setText("")
        self.ui.task_le.setText("")

    def ok_clicked(self):
        app_window.ui.task_lb.setText( self.ui.task_le.text() )
        app_window.ui.project_lb.setText( self.ui.project_le.text() )
        app_window.ui.ticket_lb.setText(self.ui.ticket_le.text())
        self.ui.hide()
        

    def cancel_clicked(self):
        self.ui.hide()

def file_log():
    with open("Report.txt", "a") as file_object:
        file_object.write("Time: {} \tTask: {}\n".format(app_window.ui.counter_lb.text(), app_window.ui.task_lb.text() ))

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
    
    global loop_time_sec

    #Get foreground window ID
    foreground_window = user32.GetForegroundWindow() 
    #Get foreground window text 
    window_text_len = user32.GetWindowTextLengthW(foreground_window)
    window_text = ctypes.create_unicode_buffer(window_text_len + 1)
    user32.GetWindowTextW(foreground_window, window_text, window_text_len + 1)

    #Evaluate if the PC is locked and then increase the right timer
    if (foreground_window == 0)  or (window_text.value == "Windows Default Lock Screen"):
        time_log_on, time_log_off = clock_add_sec("log_off", loop_time_sec)
    else:
        time_log_on , time_log_off = clock_add_sec("log_on", loop_time_sec)



    #time_log_on = str(time_logged_on_hr) + ":" + str(time_logged_on_min) + "m : " + str(time_logged_on_sec) + "s"
    #time_log_off = "LOG OFF: " + str(time_logged_off_hr) + "h : " + str(time_logged_off_min) + "m : " + str(time_logged_off_sec) + "s"

    app_window.ui.counter_lb.setText(time_log_on.strftime("%H:%M:%S"))

    # app_window.ui.counter_lb.setText(time_log_on.strftime("%H:%M:%S"))
    # app_window.ui.counter_lb.repaint()
    # app_window.ui.time_cnt_lbl_log_off.setText(time_log_off.strftime("%H:%M:%S"))
    # app_window.ui.time_cnt_lbl_log_off.repaint()

def clock_add_sec(clock, plus_seconds):

    global time_logged_on_sec
    global time_logged_on_min
    global time_logged_on_hr

    global time_logged_off_sec
    global time_logged_off_min
    global time_logged_off_hr

    time_log_on = datetime.time()
    time_log_off = datetime.time()

    if(clock == "log_on"):
        
        time_logged_on_sec = time_logged_on_sec + plus_seconds

        if (time_logged_on_sec == 60):
            time_logged_on_min = time_logged_on_min + 1
            time_logged_on_sec = 0

        if (time_logged_on_min == 60):
            time_logged_on_hr = time_logged_on_hr + 1
            time_logged_on_min = 0

        

    if(clock == "log_off"):

        time_logged_off_sec = time_logged_off_sec + plus_seconds

        if (time_logged_off_sec == 60):
            time_logged_off_min = time_logged_off_min + 1
            time_logged_off_sec = 0

        if (time_logged_off_min == 60):
            time_logged_off_hr = time_logged_off_hr + 1
            time_logged_off_min = 0

    time_log_on = datetime.time(time_logged_on_hr,time_logged_on_min,time_logged_on_sec)
    time_log_off = datetime.time(time_logged_off_hr,time_logged_off_min,time_logged_off_sec)

    return (time_log_on , time_log_off)


if __name__ == '__main__':
    #Init the time counters
    time_logged_on_sec = 0
    time_logged_on_min = 0
    time_logged_on_hr = 0
    time_logged_off_sec = 0
    time_logged_off_min = 0
    time_logged_off_hr = 0

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
    clickable(app_window.ui.project_lb).connect(app_window.show_dialog)
    clickable(app_window.ui.counter_lb).connect(app_window.toggle_timer)

    app_window.ui.show()


    # Run the main Qt loop
    app.exec_()
    sys.exit()
