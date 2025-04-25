
from MainWindow import MainWindow
from PySide6.QtWidgets import (
    QApplication, 
)

def main():
    app = QApplication([])
    window = MainWindow(app)
    window.show()
    app.exec()

main()
