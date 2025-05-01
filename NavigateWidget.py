
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
    noteInput: QPlainTextEdit
    fileDisplay: QListWidget
    backButton: QPushButton
    yesButton: QPushButton
    unsureButton: QPushButton

    def __init__(self, model):
        super().__init__()
        self.model = model
        self.model.openedSession[int].connect(self.setupSession)
        self.model.closedSession[int].connect(self.shutDownSession)
        self.layout = QHBoxLayout()

        self.noteInput = QPlainTextEdit()
        self.noteInput.setMaximumSize(QSize(9999999, 50))

        self.backButton = QPushButton('Go Back')
        self.yesButton = QPushButton('Yes')
        self.unsureButton = QPushButton('Unsure')

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.backButton)
        buttonLayout.addWidget(self.yesButton)
        buttonLayout.addWidget(self.unsureButton)

        self.fileDisplay = QListWidget(self)
        
        self.layout.addLayout(buttonLayout)
        self.layout.addWidget(self.noteInput)
        self.layout.addWidget(self.fileDisplay)
        
    @Slot()
    def setupSession(self, _):
        self.backButton.clicked.connect(lambda: self.NavBtn('Go Back', -1))
        self.yesButton.clicked.connect(lambda: self.NavBtn('Yes', 1))
        self.unsureButton.clicked.connect(lambda: self.NavBtn('Unsure', 1))
        note = self.model.getNote()
        if note == '':
            self.noteInput.setPlaceholderText('Write your notes here')
        else:
            self.noteInput.setPlainText(note)
        for obj in self.model.objects:
            self.fileDisplay.insertItem(0, obj.name)
        
        self.fileDisplay.itemActivated.connect(self.setSelected)
        
    @Slot()
    def shutDownSession(self, _):
        self.backButton.clicked.disconnect()
        self.yesButton.clicked.disconnect()
        self.unsureButton.clicked.disconnect()
        self.noteInput.setPlainText('')

        self.fileDisplay.clear()
        self.fileDisplay.itemActivated.disconnect()

    def setSelected(self, item):
        itemIndex = self.fileDisplay.indexFromItem(item).row()
        self.model.cursor = itemIndex
        note = self.model.getNote()
        self.noteInput.setPlainText(note)
        self.navigated.emit(itemIndex)
 
    def NavBtn (self, msg, delta):
        if msg == 'Yes':
            self.model.addDBEntry(True, self.noteInput.toPlainText())
        elif msg == 'Unsure':
            self.model.addDBEntry(False, self.noteInput.toPlainText())

        self.model.updateCursor(delta)
        self.fileDisplay.setCurrentRow(self.model.cursor)

        note = self.model.getNote()
        self.noteInput.setPlainText(note)

        self.navigated.emit(delta)
        note = self.model.getNote()
        if note == 'no-note':
            self.noteInput.setPlaceholderText('Write your notes here')
        else:
            self.noteInput.setPlainText(note)
