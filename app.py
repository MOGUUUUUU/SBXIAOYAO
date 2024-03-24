from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import qt5_applications
import sys
import os
import main

import Ui_qt


dirname = os.path.dirname(qt5_applications.__file__)
plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class MyMainWindow(Ui_qt.Ui_MainWindow, QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        
    def click_start_button(self):
        self.textBrowser.setText('start')
    
    def click_analyse_button(self):
        # self.textBrowser.setText('analyse')
        main.main()

def run():
    app = QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    run()