from PyQt5.QtWidgets import *
from PyQt5 import uic

class WinChat(QMainWindow):

    def __init__(self):
        super(WinChat, self).__init__()
        uic.loadUi("winChat.ui", self)
        self.show()

        self.pbSendName.clicked.connect(lambda: self.message(self.leName.text()))
        self.pbSendMessage.clicked.connect(lambda: self.tbReceivedMessages.append(self.leMessage.text()))

    def message(self, txt):
        msg = QMessageBox()
        msg.setText(txt)
        msg.exec_()

