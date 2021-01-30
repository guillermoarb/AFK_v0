import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QDialog
from PySide2.QtCore import QFile

class Window():
    def __init__(self):
        super(Window, self).__init__()
        self.ui = QUiLoader().load(QFile("ui\main_window.ui"))


if __name__ == '__main__':


    #Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the main window
    app_window = Window()

    app_window.ui.show()


    # Run the main Qt loop
    app.exec_()
    sys.exit()
