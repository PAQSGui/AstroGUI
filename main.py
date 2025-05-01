
from MainWindow import MainWindow
from PySide6.QtWidgets import QApplication

app = QApplication([])
window = MainWindow(app)
window.show()
app.exec()