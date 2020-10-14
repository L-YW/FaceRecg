import sys
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import QObject

class Listener(QObject) :
    index = 0
    user_signal = pyqtSignal(int)

    def run(self):
        self.index = 0 if self.index == 2 else self.index +1
        self.user_signal.emit(self.index)

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.lb_1 = QLabel()

        self.listener = Listener()
        self.listener.user_signal.connect(self.changeImage)

        self.btn1 = QPushButton('Button1', self)
        self.btn1.clicked.connect(self.listener.run)

        self.index = 0
        self.pixmap = QPixmap(".\\img\\teemo.png")
        self.init_ui()

    def init_ui(self):
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        layout = QBoxLayout(QBoxLayout.TopToBottom)
        self.setLayout(layout)
        self.lb_1.setPixmap(self.pixmap)
        layout.addWidget(self.lb_1)


    @pyqtSlot(int)
    def changeImage(self, arg1) :
        print(arg1)
        self.index = arg1
        if self.index == 0 :
            self.pixmap = QPixmap(".\\img\\teemo.png")
            self.lb_1.setPixmap(self.pixmap)
        elif self.index == 1 :
            self.pixmap = QPixmap(".\\img\\nami.png")
            self.lb_1.setPixmap(self.pixmap)
        elif self.index == 2 :
            self.pixmap = QPixmap(".\\img\\blitz.png")
            self.lb_1.setPixmap(self.pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Window()
    form.show()
    exit(app.exec_())