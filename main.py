import sys
import os
import cv2
import Ui_wd
import datetime

import qt5_applications
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QImage
from postpro import Vedio

dirname = os.path.dirname(qt5_applications.__file__)
plugin_path = os.path.join(dirname, 'Qt', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MyMainWindow(Ui_wd.Ui_MainWindow, QMainWindow):
        def __init__(self, parent=None):
            super(MyMainWindow, self).__init__(parent)
            self.setupUi(self)
            self.cap = Vedio()
            self.timer_camera = QTimer()
            self.timer_camera.timeout.connect(self.read_cap)
            self.native_img = None
            self.postpro_img = None
            self.pause = False

            
        def clickStart(self):
            if self.timer_camera.isActive() == False:
                success = self.cap.open_cap()
                if not success:
                    self.textBrowser.setText('failed to open cap')
                else:
                    self.timer_camera.start(30)
                    self.startButton.setText('Close')
            else:
                self.timer_camera.stop()
                self.startButton.setText('Start')
            
        def clickPause(self):
            self.textBrowser.setText('pause')
            if self.pause:
                if not self.timer_camera.isActive():
                    self.timer_camera.start()
                    self.pause = False
                    self.pauseButton.setText('pause')
            elif not self.pause:
                if self.timer_camera.isActive():
                    self.timer_camera.stop()
                    self.pause = True
                    self.pauseButton.setText('continue')
        
        def clickSave(self):
            fn = f'{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.jpg'
            bn = fn
            cnt = 0
            while os.path.exists(fn):
                fn = f'{bn}_{cnt}'
                cnt += 1
            if self.postpro_img is not None:
                cv2.imwrite(f'old_{fn}', self.native_img)
                cv2.imwrite(fn, self.postpro_img)
            
        def clickExit(self):
            ok = QPushButton()
            cancel = QPushButton()
            msg = QMessageBox(QMessageBox.Warning, 'Exit', 'Confirm exit!!')
            msg.addButton(ok, QMessageBox.ActionRole)
            msg.addButton(cancel, QMessageBox.RejectRole)
            ok.setText('Yes')
            cancel.setText('No')
            if msg.exec_() == QMessageBox.RejectRole:
                return
            else:
                self.cap.close_cap()
                if self.timer_camera.isActive():
                    self.timer_camera.stop()
                cv2.destroyAllWindows()
                self.close()
        
        def read_cap(self):
            from datetime import datetime
            tt = datetime.now()
            self.textBrowser.setText(f'{tt}')
            self.cap.read_cap(self)
            show_native = QImage(self.native_img.data, 
                                 self.native_img.shape[1], 
                                 self.native_img.shape[0],
                                 QImage.Format_RGB888)
            self.nativeVideo.setPixmap(QPixmap.fromImage(show_native))
            show_postpro = QImage(self.postpro_img.data, 
                                 self.postpro_img.shape[1], 
                                 self.postpro_img.shape[0],
                                 QImage.Format_RGB888)
            self.postproVideo.setPixmap(QPixmap.fromImage(show_postpro))
        
        
def run():
    app = QApplication(sys.argv)
    MainWindow = MyMainWindow()
    MainWindow.show()
    cv2.destroyAllWindows()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    run()