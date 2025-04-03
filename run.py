
from Layout import MainWindow
from PySide6.QtWidgets import (
    QApplication, 
)

def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

main()