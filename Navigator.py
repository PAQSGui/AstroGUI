
from Model import Model

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    QWidget,
    QListWidget,
    )

from PySide6.QtCore import QSize, Signal

"""
Navigator is responsible for navigating between files
"""
class Navigator(QWidget):

    layout: QHBoxLayout
    model: Model
    navigated = Signal(int)

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.layout = QHBoxLayout()

        whyInput = QPlainTextEdit()
        note = self.model.getNote()
        if note == "":
            whyInput.setPlaceholderText("Write your notes here")
        else:
            whyInput.setPlainText(note)
        whyInput.setMaximumSize(QSize(9999999, 50))
        self.whyInput = whyInput

        backButton = QPushButton("Back")
        backButton.clicked.connect(lambda: self.NavBtn(msg="Back",delta=-1))

        yesButton = QPushButton("Yes")
        yesButton.clicked.connect(lambda: self.NavBtn( msg="Yes",delta=1))

        unsureButton = QPushButton("Unsure")
        unsureButton.clicked.connect(lambda: self.NavBtn(msg="Unsure",delta=1))

        self.layout.addWidget(backButton)
        self.layout.addWidget(yesButton)
        self.layout.addWidget(unsureButton)
        self.layout.addWidget(self.whyInput)

        self.filedisplay=QListWidget(self)
        self.filedisplay.insertItems(0,self.model.getFileList())
        self.filedisplay.itemActivated.connect(self.setSelected)
        
        self.layout.addWidget(self.filedisplay)
    def setSelected(self,item):
        itemIndex=self.filedisplay.indexFromItem(item).row()
        self.model.cursor=itemIndex #update cursor
        note = self.model.getNote()
        self.whyInput.setPlainText(note)
        self.navigated.emit(itemIndex)
 
    def NavBtn (self, msg, delta):
        if msg == "Yes":
            self.model.addDBEntry(True, self.whyInput.toPlainText())
        elif msg == "Unsure":
            self.model.addDBEntry(False, self.whyInput.toPlainText())

        self.model.updateCursor(delta)
        #print(self.model.getState().name)
        self.filedisplay.setCurrentRow(self.model.cursor)

        note = self.model.getNote()
        self.whyInput.setPlainText(note)

        self.navigated.emit(delta)
