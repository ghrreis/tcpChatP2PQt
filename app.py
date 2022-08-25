from WinChat import *
import sys


def main():
    tg = sys.argv[1] # Variável para receber o IP do servidor que contém lista de usuários on-line
    app = QApplication([])
    window = WinChat(tg)
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
