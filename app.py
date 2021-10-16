from WinChat import *


def main():
    app = QApplication([])
    window = WinChat()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
