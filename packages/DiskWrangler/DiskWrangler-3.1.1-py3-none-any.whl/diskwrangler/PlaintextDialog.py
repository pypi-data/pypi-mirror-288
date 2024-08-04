#======================================================================
# PlaintextDialog.py
#======================================================================
import logging
import os
from enum import Enum
from pathlib import Path
from PyQt6 import QtGui
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from PyQt6.QtGui import (QAction, QFont, QFontDatabase, QTextDocument,
                         QTextCursor)
from PyQt6.QtWidgets import (QMainWindow, QTextEdit, QLineEdit,
    QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QCheckBox,
    QPushButton, QMessageBox)
from PyQt6.QtGui import QColor
from d64py.DirEntry import DirEntry
from d64py.Constants import CharSet
from d64py.Exceptions import PartialDataException
from d64py import D64Utility
from d64py.DiskImage import TextLine

class PlaintextHeight(Enum):
    TALL  = 35
    SHORT = 20

class PlaintextDialog(QMainWindow):
    """
    General-purpose dialog for displaying lines of text.
    :param pages: List of lists of TextLine.
    :param charSet: Whether to display ASCII or PETSCII (enum).
    :param dirEntry: The DirEntry of the file to be displayed.
    """
    def __init__(self, parent, flags, pages: list[list[TextLine]], charSet: CharSet, dirEntry: DirEntry=None, plaintextHeight: PlaintextHeight=PlaintextHeight.TALL, scrapNames: list[str]=None):
        super().__init__(parent, flags)
        self.parent = parent

        self.pages = pages
        if pages == []:
            self.lines = []
        else:
            self.lines = pages[0]
        self.currentPage = 0
        
        if not self.lines:  # no lines means search within geoWrite files on disk
            self.searchGeoWrite = True
        else:
            self.searchGeoWrite = False
        self.charSet = charSet # PETSCII or ASCII
        self.shifted = False
        self.dirEntry = dirEntry
        self.plaintextHeight = plaintextHeight
        self.scrapNames = scrapNames 
        
        self.setContentsMargins(12, 12, 12, 12)
        self.txtPlaintext = QTextEdit(self) # parent
        self.txtPlaintext.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
          | Qt.TextInteractionFlag.TextSelectableByKeyboard)
        self.plainFont = QFont("Monospace")
        self.plainFont.setStyleHint(QFont.StyleHint.TypeWriter)
        fontPath = str(Path(__file__).parents[0]) + os.sep + "C64_Pro_Mono-STYLE.ttf"
        fontId = QFontDatabase.addApplicationFont(fontPath)
        if fontId == -1:
            raise Exception("Can't load Style's Commodore font!")
        families = QFontDatabase.applicationFontFamilies(fontId)
        self.commodoreFont = QFont(families[0], 10)
        if charSet == CharSet.PETSCII:
            self.txtPlaintext.setFont(self.commodoreFont)
        else:
            self.txtPlaintext.setFont(self.plainFont)

        shiftAction = QAction("use shifted &font", self)
        shiftAction.setShortcut("Ctrl+F")
        shiftAction.setStatusTip("shift font")
        shiftAction.triggered.connect(self.shiftFont)
        self.txtPlaintext.addAction(shiftAction)

        metrics = self.txtPlaintext.fontMetrics()
        width = metrics.boundingRect('n' * 78).width()
        height = (metrics.boundingRect('N').height() + 1) * plaintextHeight.value + 1
        self.txtPlaintext.setMinimumSize(width, height)
        self.plainColor = self.txtPlaintext.textColor()
        self.showTextLines()

        vLayout = QVBoxLayout()
        if self.plaintextHeight == PlaintextHeight.TALL: # not for scraps
            hLayout = QHBoxLayout()
            lblSearch = QLabel("&Search: ")
            self.txtSearch = QLineEdit()
            self.txtSearch.returnPressed.connect(self.doSearch)
            lblSearch.setBuddy(self.txtSearch)
            self.chkCaseSensitive = QCheckBox("&Case-sensitive", self)
            self.lblShift = QLabel("(ctrl-F shifts)")
            hLayout.addWidget(lblSearch)
            hLayout.addWidget(self.txtSearch)
            hLayout.addWidget(self.chkCaseSensitive)
            hLayout.addWidget(self.lblShift)
            # only put the button for C= text files
            if charSet == CharSet.PETSCII:
                self.btnCharSet = QPushButton("&ASCII", self)
                self.btnCharSet.clicked.connect(self.switchCharSet)
                hLayout.addWidget(self.btnCharSet)
                self.lblShift.setDisabled(False)
            else:
                self.lblShift.setDisabled(True)
            vLayout.addLayout(hLayout)
            
        vLayout.addWidget(self.txtPlaintext)

        if len(pages) > 1:
            buttonLayout = QHBoxLayout()
            buttonLayout.addStretch(1)
            self.btnPrev = QPushButton("&Prev")
            self.btnNext = QPushButton("&Next")

            permString = self.dirEntry.geosFileHeader.getPermanentNameString()
            if permString.startswith("Write Image"):
                self.lblPage = QLabel("page:")
                buttonLayout.addWidget(self.lblPage)
                self.cmbPage = QComboBox()
                self.cmbPage.currentIndexChanged.connect(self.gotoPage) # TRIGGERS A CALL
                i = 0
                while i < len(self.pages):
                    self.cmbPage.addItem(str(i + 1))
                    i += 1
                buttonLayout.addWidget(self.cmbPage)
            self.btnPrev.clicked.connect(self.prev)
            self.btnPrev.setEnabled(False)
            buttonLayout.addWidget(self.btnPrev)
            self.btnNext.clicked.connect(self.next)
            buttonLayout.addWidget(self.btnNext)
            vLayout.addLayout(buttonLayout)

            if permString.startswith("text album"):
                menubar = self.menuBar()
                searchMenu = menubar.addMenu("&Search")
                self.searchActions = []
                i = 0
                while i < len(self.scrapNames):
                    self.searchActions.append(QAction(self.scrapNames[i], self))
                    self.searchActions[i].triggered.connect(self.searchScrap)
                    searchMenu.addAction(self.searchActions[i])
                    i += 1
                    
        widget = QWidget()
        widget.setLayout(vLayout)
        self.setCentralWidget(widget)
        self.centerWindow()

    def keyPressEvent(self, evt: QKeyEvent):
        match evt.key():
            case Qt.Key.Key_Escape:
                self.hide()

    def searchScrap(self):
        if len(self.lines) > 1:
            action = self.sender()
            i = 0
            while i < len(self.searchActions):
                if action == self.searchActions[i]:
                    break
                i += 1
            if i < len(self.searchActions): # menu item selected?
                self.currentPage = i
                if self.currentPage == 0:
                    self.btnPrev.setEnabled(False)
                else:
                    self.btnPrev.setEnabled(True)
                if self.currentPage == len(self.searchActions) - 1:
                    self.btnNext.setEnabled(False)
                else:
                    self.btnNext.setEnabled(True)
        self.lines = self.pages[self.currentPage]
        self.setWindowTitle(self.dirEntry.getDisplayFileName() + "/" + self.scrapNames[self.currentPage])
        self.showTextLines()

    def prev(self):
        self.currentPage -= 1
        if self.currentPage == 0:
            self.btnPrev.setEnabled(False)
        self.btnNext.setEnabled(True)
        if self.dirEntry.geosFileHeader.getPermanentNameString().startswith("Write Image"):
            self.cmbPage.setCurrentIndex(self.currentPage)
        self.reshow()
        
    def next(self):
        self.currentPage += 1
        if self.currentPage == len(self.pages) - 1:
            self.btnNext.setEnabled(False)
        self.btnPrev.setEnabled(True)
        if self.dirEntry.geosFileHeader.getPermanentNameString().startswith("Write Image"):
            self.cmbPage.setCurrentIndex(self.currentPage)
        self.reshow()

    def gotoPage(self, index):
        self.currentPage = index
        self.btnPrev.setEnabled(True)
        self.btnNext.setEnabled(True)
        if index == 0:
            self.btnPrev.setEnabled(False)
        if index == len(self.pages) - 1:
            self.btnNext.setEnabled(False)
        self.cmbPage.setCurrentIndex(self.currentPage)
        self.reshow()
        
    def reshow(self):
        self.lines = self.pages[self.currentPage]
        if self.dirEntry.geosFileHeader.getPermanentNameString().startswith("text album"):
            self.setWindowTitle(self.dirEntry.getDisplayFileName() + "/" + self.scrapNames[self.currentPage])
        else:
            self.setWindowTitle(f"{self.dirEntry.getDisplayFileName()}, page {self.currentPage + 1}")
        self.showTextLines()
        
    def centerWindow(self):
        rect = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def showTextLines(self):
        self.txtPlaintext.clear()
        try:
            for line in self.lines:
                if line.isErrorLine():
                    if self.searchGeoWrite:
                        # hijack "ErrorLine" attribute to indicate a heading
                        self.txtPlaintext.setFontWeight(QFont.Weight.Bold)
                        self.txtPlaintext.insertPlainText(line.text + '\r')
                        self.txtPlaintext.setFontWeight(QFont.Weight.Normal)
                    else:
                        self.txtPlaintext.setTextColor(QColor(255, 48, 0))
                        self.txtPlaintext.insertPlainText(line.text + '\r')
                        self.txtPlaintext.setTextColor(self.plainColor)
                else:
                    self.txtPlaintext.insertPlainText(line.text + '\r')
        except Exception as exc:
            logging.exception(exc)
            return
        self.txtPlaintext.moveCursor(QTextCursor.MoveOperation.Start, QTextCursor.MoveMode.MoveAnchor)

    def shiftFont(self):
        if self.charSet == CharSet.ASCII:
            return
        self.shifted = not self.shifted
        self.lines = self.parent.currentImage.getFileAsText(self.dirEntry, self.charSet, self.shifted)
        self.showTextLines()

    def switchCharSet(self):
        match self.charSet:
            case CharSet.ASCII:
                self.txtPlaintext.setFont(self.commodoreFont)
                self.charSet = CharSet.PETSCII
                self.lines = self.parent.currentImage.getFileAsText(self.dirEntry, self.charSet, self.shifted)
                self.lblShift.setDisabled(False)
                self.btnCharSet.setText("&ASCII")
            case CharSet.PETSCII:
                self.txtPlaintext.setFont(self.plainFont)
                self.charSet = CharSet.ASCII
                self.lines = self.parent.currentImage.getFileAsText(self.dirEntry, self.charSet)
                self.lblShift.setDisabled(True)
                self.btnCharSet.setText("&PETSCII")
        self.showTextLines()

    def doSearch(self):
        if not self.txtSearch.text():
            QMessageBox.warning(self, "Warning", "No search text entered.", QMessageBox.StandardButton.Ok)
            return

        if self.searchGeoWrite:
            # Call the Wrangler's searchWithinGeoWriteFiles()
            # to do the search and return a report. Note that
            # this is the one time we aren't passing a list of lists.
            self.lines = self.parent.searchWithinGeoWriteFiles(self.txtSearch.text(), self.chkCaseSensitive.isChecked())
            if self.lines:
                self.showTextLines()
            else:
                QMessageBox.warning(self, "Warning", f"'{self.txtSearch.text()}' not found!", QMessageBox.StandardButton.Ok)
            return

        match self.charSet:
            case CharSet.ASCII:
                if self.chkCaseSensitive.isChecked():
                    result = self.txtPlaintext.find(self.txtSearch.text(), QTextDocument.FindFlag.FindCaseSensitively)
                else:
                    result = self.txtPlaintext.find(self.txtSearch.text())
            case CharSet.PETSCII:
                temp = D64Utility.asciiToPetsciiString(self.txtSearch.text())
                searchTerm = ""
                for char in temp:
                    searchTerm += chr(ord(char) | 0xe100 if self.shifted else ord(char) | 0xe000)
                result = self.txtPlaintext.find(D64Utility.asciiToPetsciiString(searchTerm))
        if not result:
            QMessageBox.warning(self, "Warning", f"'{self.txtSearch.text()}' not found!", QMessageBox.StandardButton.Ok)
