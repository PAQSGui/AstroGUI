
from Model import Model

from PySide6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    QWidget,
    QListWidget,
    )

from PySide6.QtCore import QSize, Signal, Slot

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
        self.model.openedSession[list].connect(self.setupSession)
        self.model.closedSession[list].connect(self.shutDownSession)
        self.layout = QHBoxLayout()

        whyInput = QPlainTextEdit()
        whyInput.setMaximumSize(QSize(9999999, 50))
        self.whyInput = whyInput

        self.backButton = QPushButton("Previous")

        self.yesButton = QPushButton("Next")

        self.layout.addWidget(self.backButton)
        self.layout.addWidget(self.yesButton)
        self.layout.addWidget(self.whyInput)

        self.filedisplay=QListWidget(self)
        
        self.layout.addWidget(self.filedisplay)
        
    @Slot()
    def setupSession(self,files):
        self.backButton.clicked.connect(lambda: self.NavBtn(msg="Previous",delta=-1))
        self.yesButton.clicked.connect(lambda: self.NavBtn( msg="Next",delta=1))
        note = self.model.getNote()
        if note == "":
            self.whyInput.setPlaceholderText("Write your notes here")
        else:
            self.whyInput.setPlainText(note)
        for obj in self.model.objects:
            self.filedisplay.insertItem(0,obj.name)
        
        self.filedisplay.itemActivated.connect(self.setSelected)
    @Slot()
    def shutDownSession(self,files):
        self.backButton.clicked.disconnect(lambda: self.NavBtn(msg="Previous",delta=-1))
        self.yesButton.clicked.disconnect(lambda: self.NavBtn( msg="Next",delta=1))
        self.whyInput.setPlainText("")

        self.filedisplay.clear()
        self.filedisplay.itemActivated.disconnect(self.setSelected)


    def setSelected(self,item):
        itemIndex=self.filedisplay.indexFromItem(item.name).row()
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
        self.filedisplay.setCurrentRow(self.model.cursor)

        note = self.model.getNote()
        self.whyInput.setPlainText(note)

        self.navigated.emit(delta)
        note = self.model.getNote()
        if note == 'no-note':
            self.whyInput.setPlaceholderText("Write your notes here")
        else:
            self.whyInput.setPlainText(note)
