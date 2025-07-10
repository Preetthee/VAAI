import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from record_button import RecordButton
from list_view import RecordingsListView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Audio Recorder")
        self.setGeometry(700, 300, 400, 300)
        self.initUI()

    def initUI(self):
        self.list_view = RecordingsListView(self)
        self.list_view.setGeometry(20, 120, 360, 160)
        self.list_view.setStyleSheet("font-size: 12px;")

        button = RecordButton("Hold to Record", self, list_view=self.list_view)
        button.setGeometry(100, 40, 200, 60)
        button.setStyleSheet("font-size: 18px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
