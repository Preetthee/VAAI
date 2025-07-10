import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from record_button import RecordButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Recorder")
        self.setGeometry(700, 300, 400, 300)
        self.initUI()

    def initUI(self):
        button = RecordButton("Hold to Record", self)
        button.setGeometry(100, 100, 200, 60)
        button.setStyleSheet("font-size: 18px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
