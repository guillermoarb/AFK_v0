import sys
import ctypes
from PySide2.QtCore import *
from PySide2.QtWidgets import *

class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.task_lbl = QLabel("None")
        self.time_cnt_lbl = QLabel("None")
        self.button = QPushButton("Task")
        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(self.task_lbl)
        layout.addWidget(self.time_cnt_lbl)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.get_task_name)

        # 1s Task init
        timer_1s = QTimer(self)
        timer_1s.timeout.connect(self.task_1s)
        timer_1s.start(1000)



    # Greets the user
    def get_task_name(self):
        task_name, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')

        if ok:
            self.task_lbl.setText(task_name)

    def task_1s(self):
            global time_logged_in

            if (user32.GetForegroundWindow() % 10 != 0):
                time_logged_in = time_logged_in + 1

            self.time_cnt_lbl.setText(str(time_logged_in))




if __name__ == '__main__':

    time_logged_in = 0

    #Lock API
    user32 = ctypes.windll.User32

    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())



