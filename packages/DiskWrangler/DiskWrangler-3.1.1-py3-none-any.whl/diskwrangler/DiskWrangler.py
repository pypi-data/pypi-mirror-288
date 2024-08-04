#======================================================================
# DiskWrangler.py
#======================================================================
from jproperties import Properties
import logging
import os
from pathlib import Path
import platform
import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QThread, QMargins
from PyQt6.QtWidgets import (
    QApplication, QStyleFactory, QHeaderView, QDialog, QDialogButtonBox,
    QFileDialog, QMessageBox, QLabel, QScrollArea, QMenu, QStatusBar,
    QVBoxLayout, QHBoxLayout, QAbstractItemView, QWidget, QGridLayout,
    QGroupBox, QMainWindow
)
from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QAction, QActionGroup, QImage, QPixmap, QScreen
from importlib.metadata import version
from DirTableModel import DirTableModel, ModelFields
from HexDialog import HexDialog
from SectorErrorDialog import SectorErrorDialog
from BamDialog import BamDialog
from PlaintextDialog import PlaintextDialog, PlaintextHeight
from FontDialog import FontDialog
from D64Gfx import Palette
from Analyzer import Analyzer
from d64py.Constants import ImageType
from d64py.DirEntry import DirEntry
from d64py.DiskImage import DiskImage
from d64py import Geometry
from d64py.Exceptions import PartialDataException
from d64py.DiskImage import TextLine
from d64py.Constants import FileType, GeosFileType,SectorErrors, CharSet
import D64Gfx
from GeoPaintDialog import GeoPaintDialog
from PhotoScrapDialog import PhotoScrapDialog

#======================================================================

class DiskWrangler(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        logging.debug(f"available Qt styles: {QStyleFactory.keys()}")
        logging.debug(f"current style: {app.style().name()}")
#        self.title = f"Cenbe's Disk Wrangler {version('DiskWrangler')}"
        self.version = "3.1.1"
        self.title = f"Cenbe's Disk Wrangler {self.version}"
        self.setWindowTitle(self.title)
        namesLayout = QVBoxLayout()
        lblPermName = QLabel("Permanent name string:")
        namesLayout.addWidget(lblPermName)
        self.lblPermNameData = QLabel("")
        namesLayout.addWidget(self.lblPermNameData)
        lblParentApp = QLabel("Parent application name:")
        namesLayout.addWidget(lblParentApp)
        self.lblParentAppData = QLabel("")
        namesLayout.addWidget(self.lblParentAppData)
        namesLayout.setContentsMargins(12, 12, 12, 12)

        iconLayout = QHBoxLayout()
        self.lblIcon = QLabel("")
        self.lblIcon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconLayout.addWidget(self.lblIcon)
        iconLayout.addLayout(namesLayout)

        # FIXME lose this hideous mockery of a language
        titleStyle = """
            QGroupBox:title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                margin-left: 3px;
                margin-right: 3px;
            }
             QGroupBox {
                border: 1px ridge grey;
                border-radius: 0px;
                padding-top: 10px;
                margin-top: 5px;
            }
            """

        infoBox = QGroupBox("GEOS info:")
        if app.style().name().lower() == "fusion":
            infoBox.setStyleSheet(titleStyle)
        infoLayout = QVBoxLayout()
        infoLayout.addLayout(iconLayout)

        self.lblInfo = QLabel(" ")
        self.lblInfo.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lblInfo.setWordWrap(True)
        self.lblInfo.setContentsMargins(6, 6, 6, 6)
        scrInfo = QtWidgets.QScrollArea()        
        scrInfo.setWidgetResizable(True)
        scrInfo.setWidget(self.lblInfo)
        infoLayout.addWidget(scrInfo)
        infoBox.setLayout(infoLayout)

        diskDataLayout = QGridLayout()
        diskDataLayout.setSpacing(9)
        lblDiskName = QLabel("Disk name:")
        self.lblDiskNameData = QLabel("")
        lblImageType = QLabel("Image type:")
        self.lblImageTypeData = QLabel("")
        lblIsGeos = QLabel("GEOS disk?")
        self.lblIsGeosData = QLabel("")
        lblFiles = QLabel("Files:")
        self.lblFilesData = QLabel("")
        lblBlocksFree = QLabel("Blocks free:")
        self.lblBlocksFreeData = QLabel("")

        diskDataLayout.addWidget(lblDiskName, 0, 0)
        diskDataLayout.addWidget(self.lblDiskNameData, 0, 1)
        diskDataLayout.addWidget(lblImageType, 1, 0)
        diskDataLayout.addWidget(self.lblImageTypeData, 1, 1)
        diskDataLayout.addWidget(lblIsGeos, 2, 0)
        diskDataLayout.addWidget(self.lblIsGeosData, 2, 1)
        diskDataLayout.addWidget(lblFiles, 3, 0)
        diskDataLayout.addWidget(self.lblFilesData, 3, 1)
        diskDataLayout.addWidget(lblBlocksFree, 4, 0)
        diskDataLayout.addWidget(self.lblBlocksFreeData, 4, 1)

        diskLayout = QVBoxLayout()
        diskLayout.addStretch(1)
        diskLayout.addLayout(diskDataLayout)
        diskLayout.addStretch(1)

        topLayout = QHBoxLayout()
        topLayout.setContentsMargins(12 ,12 ,12 ,12)
        topLayout.addLayout(diskLayout)
        topLayout.addStretch(1)
        topLayout.addWidget(infoBox)

        self.tblDirEntries = QtWidgets.QTableView()
        self.tblDirEntries.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tblDirEntries.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tblDirEntries.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tblDirEntries.customContextMenuRequested.connect(self.showDirContextMenu)
        self.tblDirEntries.doubleClicked.connect(self.doDefaultDirAction)

        self.header = self.tblDirEntries.horizontalHeader()
        self.header.setHighlightSections(False)
        font = self.header.font()
        font.setBold(False)
        self.header.setFont(font)
        self.tblDirEntries.verticalHeader().hide()
        self.model = DirTableModel([])
        self.tblDirEntries.setModel(self.model)
        for i in range(len(ModelFields)):
            self.model.setHeaderData(i, Qt.Orientation.Horizontal, ModelFields.getDescriptionByCode(i))
            if i == ModelFields.FILE_NAME.code:
                self.header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            else:
                self.header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)

        self.sizeTable()
        self.centerWindow()
        self.currentImage = None

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.tblDirEntries, 1) # stretch factor

        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

        self.peptoAction = QAction("P&epto", self)
        self.peptoAction.setCheckable(True)
        self.peptoAction.triggered.connect(self.usePeptoPalette)
        
        self.peptoNtscSonyAction = QAction("Pepto-NTSC-&Sony", self)
        self.peptoNtscSonyAction.setCheckable(True)
        self.peptoNtscSonyAction.triggered.connect(self.usePeptoNtscSonyPalette)
        
        self.colodoreAction = QAction("&Colodore", self)
        self.colodoreAction.setCheckable(True)
        self.colodoreAction.triggered.connect(self.useColodorePalette)
        
        self.palette = Palette.PEPTO # default to Pepto
        self.peptoAction.setChecked(True)
        
        actionGroup = QActionGroup(self)
        actionGroup.addAction(self.peptoAction)
        actionGroup.addAction(self.peptoNtscSonyAction)
        actionGroup.addAction(self.colodoreAction)
        actionGroup.setExclusionPolicy(QActionGroup.ExclusionPolicy.Exclusive)
        
        self.rememberAction = QAction("&Remember directory", self)
        self.rememberAction.setCheckable(True)
        self.rememberAction.triggered.connect(self.rememberDirectory)

        self.confirmAction = QAction("&Confirm exit", self)
        self.confirmAction.setCheckable(True)
        self.confirmAction.triggered.connect(self.confirmExit)

        self.tblDirEntries.installEventFilter(self)
        self.readProps()
        self.doMenu()
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.tblDirEntries.setFocus() # so cursor up/down works at start

        if len(sys.argv) > 1:
            fileName = sys.argv[len(sys.argv) - 1]
            logging.info(f"file name passed: {fileName}")
            try:
                i = DiskImage(Path(fileName))
                i.close()
                self.openImageFile(fileName)
            except Exception as exc:
                logging.error(f"can't open {fileName}:")
                logging.exception(exc)

# ======================================================================

    def doMenu(self):
        openFileAction = QAction("&Open", self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Open Disk Image")
        openFileAction.triggered.connect(self.showOpenDialog)

        self.startAnalysisAction = QAction("&Analyze", self)
        self.startAnalysisAction.setShortcut("Ctrl+A")
        self.startAnalysisAction.setStatusTip("Analyze disk image")
        self.startAnalysisAction.triggered.connect(self.startAnalysis)
        self.startAnalysisAction.setDisabled(True)

        self.errorsAction = QAction("Show &errors", self)
        self.errorsAction.setShortcut("Ctrl+E")
        self.errorsAction.setStatusTip("Show error sectors")
        self.errorsAction.triggered.connect(self.showErrors)
        self.errorsAction.setDisabled(True)

        self.viewDirHeaderAction = QAction("View directory &header", self)
        self.viewDirHeaderAction.setShortcut("Ctrl+H")
        self.viewDirHeaderAction.setStatusTip("View directory header (read-only)")
        self.viewDirHeaderAction.triggered.connect(self.viewDirHeader)
        self.viewDirHeaderAction.setDisabled(True)

        self.viewDirSectorsAction = QAction("View directory &sectors", self)
        self.viewDirSectorsAction.triggered.connect(self.viewDirSectors)
        self.viewDirSectorsAction.setDisabled(True)

        self.viewBamAction = QAction("View &BAM", self)
        self.viewBamAction.setShortcut("Ctrl+B")
        self.viewBamAction.setStatusTip("View Block Availability Map")
        self.viewBamAction.triggered.connect(self.viewBam)
        self.viewBamAction.setDisabled(True)

        self.exportGeoWriteAction = QAction("Export geo&Write files")
        self.exportGeoWriteAction.setShortcut("Ctrl+W")
        self.exportGeoWriteAction.setStatusTip("Save geoWrite files as text")
        self.exportGeoWriteAction.triggered.connect(self.exportGeoWrite)
        self.exportGeoWriteAction.setDisabled(True)

        self.searchGeoWriteAction = QAction("Search in geoWrite files")
        self.searchGeoWriteAction.setShortcut("Ctrl+S")
        self.searchGeoWriteAction.setStatusTip("Search within disk image's geoWrite files")
        self.searchGeoWriteAction.triggered.connect(self.searchGeoWrite)
        self.searchGeoWriteAction.setDisabled(True)

        exitProgramAction = QAction("E&xit", self)
        exitProgramAction.setShortcut("Ctrl+Q")
        exitProgramAction.setStatusTip("Exit Program")
        exitProgramAction.triggered.connect(self.exitProgram)
        app.aboutToQuit.connect(self.windowClosing)

        helpAboutAction = QAction("&About", self)
        helpAboutAction.setStatusTip("About This Program")
        helpAboutAction.triggered.connect(self.helpAbout)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(openFileAction)
        fileMenu.addAction(self.startAnalysisAction)
        fileMenu.addAction(self.errorsAction)
        fileMenu.addAction(self.viewDirHeaderAction)
        fileMenu.addAction(self.viewDirSectorsAction)
        fileMenu.addAction(self.viewBamAction)
        fileMenu.addAction(self.exportGeoWriteAction)
        fileMenu.addAction(self.searchGeoWriteAction)
        fileMenu.addAction(exitProgramAction)

        optionsMenu = menubar.addMenu("O&ptions")
        optionsMenu.addAction(self.rememberAction)
        optionsMenu.addAction(self.confirmAction)
        
        paletteMenu = optionsMenu.addMenu("Color pale&tte")
        paletteMenu.addAction(self.peptoAction)
        paletteMenu.addAction(self.peptoNtscSonyAction)
        paletteMenu.addAction(self.colodoreAction)

        helpMenu = menubar.addMenu("&Help")
        helpMenu.addAction(helpAboutAction)

# ======================================================================

    def showDirContextMenu(self, pos):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        contextMenu = QMenu(self)

        viewGeosHeaderAction = QAction("View GEOS Header", self)
        viewGeosHeaderAction.triggered.connect(self.viewGeosHeader)
        contextMenu.addAction(viewGeosHeaderAction)

        viewRawDataAction = QAction("View raw data", self)
        viewRawDataAction.triggered.connect(self.viewRawData)
        contextMenu.addAction(viewRawDataAction)

        exploreFontAction = QAction("Explore font", self)
        exploreFontAction.triggered.connect(self.exploreFont)
        contextMenu.addAction(exploreFontAction)

        menuSet = False
        if dirEntry.isGeosFile():
            if dirEntry.geosFileHeader.getPermanentNameString().startswith("Text  Scrap"): # note extra space
                viewGeoWriteAction = QAction("View text scrap as text", self)
                viewGeoWriteAction.triggered.connect(self.viewTextScrap)
                menuSet = True
            elif dirEntry.geosFileHeader.getPermanentNameString().startswith("text album"):
                viewGeoWriteAction = QAction("View text album", self)
                viewGeoWriteAction.triggered.connect(self.viewTextAlbum)
                menuSet = True
        if not menuSet:
            viewGeoWriteAction = QAction("View geoWrite file as text", self)
            viewGeoWriteAction.triggered.connect(self.viewGeoWriteFile)
        contextMenu.addAction(viewGeoWriteAction)

        saveGeoWriteAction = QAction("Save geoWrite file as text", self)
        saveGeoWriteAction.triggered.connect(self.saveGeoWriteFile)
        contextMenu.addAction(saveGeoWriteAction)

        viewAsTextAction = QAction("View as text", self)
        viewAsTextAction.triggered.connect(self.viewAsText)
        contextMenu.addAction(viewAsTextAction)

        saveAsTextAction = QAction("Save as text")
        saveAsTextAction.triggered.connect(self.saveAsText)
        contextMenu.addAction(saveAsTextAction)

        viewGeoPaintAction = QAction("View geoPaint image", self)
        viewGeoPaintAction.triggered.connect(self.viewGeoPaintFile)
        contextMenu.addAction(viewGeoPaintAction)

        viewPhotoAlbumAction = QAction("View photo album", self)
        viewPhotoAlbumAction.triggered.connect(self.viewPhotoAlbum)
        contextMenu.addAction(viewPhotoAlbumAction)

        if dirEntry.isGeosFile():
            permString = dirEntry.geosFileHeader.getPermanentNameString()
            viewGeosHeaderAction.setDisabled(False)
            viewAsTextAction.setDisabled(True)
            saveAsTextAction.setDisabled(True)
            if permString.startswith("Write Image"):
                viewGeoWriteAction.setDisabled(False)
                saveGeoWriteAction.setDisabled(False)
            elif permString.startswith("text album"):
                viewGeoWriteAction.setDisabled(False)
                saveGeoWriteAction.setDisabled(True)
            elif permString.startswith("Text  Scrap"):
                viewGeoWriteAction.setDisabled(False)
                saveGeoWriteAction.setDisabled(True)
            else:
                viewGeoWriteAction.setDisabled(True)
                saveGeoWriteAction.setDisabled(True)
            if dirEntry.getGeosFileType() == GeosFileType.FONT:
                exploreFontAction.setDisabled(False)
            else:
                exploreFontAction.setDisabled(True)
            if permString.startswith("Paint Image"):
                viewGeoPaintAction.setDisabled(False)
            else:
                viewGeoPaintAction.setDisabled(True)
            if permString.startswith("photo album"):
                viewPhotoAlbumAction.setDisabled(False)
            else:
                viewPhotoAlbumAction.setDisabled(True)                
        else:
            viewGeosHeaderAction.setDisabled(True)
            exploreFontAction.setDisabled(True)
            viewGeoWriteAction.setDisabled(True)
            saveGeoWriteAction.setDisabled(True)
            viewGeoPaintAction.setDisabled(True)
            if not dirEntry.getFileType() == FileType.FILETYPE_SEQUENTIAL.code:
                viewAsTextAction.setDisabled(True)
                saveAsTextAction.setDisabled(True)
            else:
                viewAsTextAction.setDisabled(False)
                saveAsTextAction.setDisabled(False)
        contextMenu.exec(self.tblDirEntries.mapToGlobal(pos))

    def viewGeosHeader(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f'viewing GEOS header for file "{dirEntry.getDisplayFileName()}"')
        ts = dirEntry. getGeosFileHeaderTrackSector()
        sector = dirEntry.getGeosFileHeader().getRaw()
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, f'GEOS header for file "{dirEntry.getDisplayFileName()}"', sector, ts, True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def viewRawData(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f'viewing raw data for file "{dirEntry.getDisplayFileName()}"')
        ts = dirEntry.getFileTrackSector()
        sector = self.currentImage.readSector(ts)
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, f'Raw data for file "{dirEntry.getDisplayFileName()}"', sector, ts, True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def exploreFont(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f'exploring font "{dirEntry.getDisplayFileName()}"')
        fontDialog = FontDialog(self, Qt.WindowType.Dialog, dirEntry, self.currentImage)
        fontDialog.show()

    def viewAsText(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f'viewing file "{dirEntry.getDisplayFileName()}" as text')
        try :
            # PlaintextDialog starts out unshifted:
            textLines = self.currentImage.getFileAsText(dirEntry, CharSet.PETSCII, False)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                textLines = exc.getPartialData()
            else:
                raise exc

        pages = []
        pages.append(textLines)
        
        try:
            self.plaintextDialog = PlaintextDialog(self, Qt.WindowType.Dialog, pages, CharSet.PETSCII, dirEntry, PlaintextHeight.TALL)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.plaintextDialog.setWindowTitle(f"{self.currentImage.getDirHeader().getDiskName().strip()}  |  {dirEntry.getDisplayFileName()}")
        self.plaintextDialog.show()
        self.plaintextDialog.txtPlaintext.setFocus()

    def saveAsText(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        fileDialog = QFileDialog(self)
        saveFileName = fileDialog.getSaveFileName(self, "Export Filename",
                        str(Path.home()) + os.sep + dirEntry.getDisplayFileName() + ".txt",
                        "*", str(Path.home()))
        if not saveFileName[0]: # user cancelled
            return
        logging.info(f'saving text file "{dirEntry.getDisplayFileName()}" as "{saveFileName[0]}"')

        try :
            # Using unshifted by default at this time. Make sure to request translation.
            lines = self.currentImage.getFileAsText(dirEntry, CharSet.PETSCII, False, True)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                lines = exc.getPartialData()
            else:
                raise exc

        with open(saveFileName[0], "w") as f:
            for line in lines:
                f.write(line.text + "\n")
        f.close()
        QMessageBox.information(self, "Information", f"{dirEntry.getDisplayFileName()} exported to\n{saveFileName[0]}",
                                    QMessageBox.StandardButton.Ok)

    def viewTextAlbum(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        index = self.currentImage.getGeosVlirIndex(dirEntry)
        version = dirEntry.getGeosFileHeader().getPermanentNameVersion()
        logging.info(f"text album {dirEntry.getDisplayFileName()} is version {version}")
        if version == "V2.1": # supports named scraps
            record = 0; namesRecordNo = -1
            while record < 127: # find last record (contains names)
                offset = (record + 1) * 2  # convert VLIR record no. to sector index
                if not index[offset]:
                    if record > 0:
                        namesRecordNo = record - 1 
                        namesRecord = self.currentImage.readVlirRecord(namesRecordNo, dirEntry)
                        break
                record += 1
                
        pages = []; scrapNames = []
        record = 0; scraps = 0
        while record < 127:
            offset = (record + 1) * 2  # convert VLIR record no. to sector index
            if not index[offset]: # empty record
                record += 1
                continue

            data = self.currentImage.readVlirRecord(record, dirEntry) # read text scrap
            if len(data) == 0: # probably a corrupt disk image
                record += 1
                continue
            if version == "V2.1" and record == namesRecordNo:
                record += 1
                continue
            if version == "V2.1":
                try :
                    if len(namesRecord) == 0: #probably a corrupt disk image
                        name = f"text #{record + 1}"
                    elif not namesRecord[0]: # same
                        name = f"text #{record + 1}"
                    else:
                        slicePoint = 1 + (record * 17); i = 0 # one for scrap count
                        while namesRecord[slicePoint + i]: # stop at the null
                            i += 1
                        nameBytes = namesRecord[slicePoint : (slicePoint + i)]
                        name = nameBytes.decode() # It's already ASCII!
                except Exception as exc:
                    logging.debug("Corrupt names record!")
                    name = f"Photo #{record + 1}"
            else:
                name = f"Photo #{record + 1}"
            scrapNames.append(name)

            textBuffer = bytearray()
            i = 2 # past length bytes
            while i < len(data):
                match(data[i]):
                    case 0x0c:  # page break
                        i += 1
                    case 0x10:  # graphics escape
                        i += 4  # 5 bytes
                    case 0x11:  # ruler escape
                        i += 26 # 27 bytes
                    case 0x17:  # font escape
                        i += 3  # 4 bytes
                    case _:
                        textBuffer.append(data[i])
                        i += 1
            try:
                scrapLines = textBuffer.decode(encoding="utf-8", errors="replace").split('\r')
            except Exception as exc:
                logging.exception(exc)
            textLines = []
            for line in scrapLines:
                textLines.append(TextLine(line, False)) # not an error line
            pages.append(textLines)
            record += 1
            
        if len(pages) != len(scrapNames):
            QMessageBox.warning(self, "Error", "Number of scraps != number of names.", QMessageBox.StandardButton.Ok)
            return
        try:
            self.plaintextDialog = PlaintextDialog(self, Qt.WindowType.Dialog, pages, CharSet.ASCII, dirEntry, PlaintextHeight.SHORT, scrapNames)
            self.plaintextDialog.setWindowTitle(dirEntry.getDisplayFileName() + "/" +scrapNames[0])
            self.plaintextDialog.show()
            self.plaintextDialog.txtPlaintext.setFocus()
        except Exception as exc:
            raise exc
 
    def viewTextScrap(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        scrapLines = self.currentImage.getTextScrapAsText(dirEntry)
        pages = []
        pages.append(scrapLines)
        try:
            self.plaintextDialog = PlaintextDialog(self, Qt.WindowType.Dialog, pages, CharSet.ASCII, dirEntry, PlaintextHeight.SHORT)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.plaintextDialog.setWindowTitle(f"{self.currentImage.getDirHeader().getDiskName().strip()}  |  {dirEntry.getDisplayFileName()}")
        self.plaintextDialog.show()
        self.plaintextDialog.txtPlaintext.setFocus()

    def viewGeoWriteFile(self, dirEntry: DirEntry):
        if not isinstance(dirEntry, DirEntry): # can't pass it from a QAction
            dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f'viewing geoWrite file "{dirEntry.getDisplayFileName()}"')
        try:
            pages = self.currentImage.getGeoWriteFileAsLines(dirEntry)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                pages = exc.getPartialData()
            else:
                raise exc

        try:
            self.plaintextDialog = PlaintextDialog(self, Qt.WindowType.Dialog, pages, CharSet.ASCII, dirEntry, PlaintextHeight.TALL)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
                            
        self.plaintextDialog.setWindowTitle(f"{dirEntry.getDisplayFileName()}, page 1")
        self.plaintextDialog.show()
        self.plaintextDialog.txtPlaintext.setFocus()

    def saveGeoWriteFile(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        fileDialog = QFileDialog(self)
        fileName = dirEntry.getDisplayFileName().replace("/", "-")
        saveFileName = fileDialog.getSaveFileName(self, "Export Filename",
                        str(Path.home()) + os.sep + fileName + ".txt",
                        "*.txt", str(Path.home()))
        if not saveFileName[0]: # user cancelled
            return
        logging.info(f'saving geoWrite file "{dirEntry.getDisplayFileName()}" as "{saveFileName[0]}"')
        try:
            pages = self.currentImage.getGeoWriteFileAsLines(dirEntry)
        except Exception as exc:
            logging.error(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            if isinstance(exc, PartialDataException):
                pages = exc.getPartialData()
            else:
                raise exc
        with open(saveFileName[0], "w") as f:
            for page in pages:
                for line in page:
                    f.write(line.text + "\n")
        f.close()
        QMessageBox.information(self, "Information", f"{dirEntry.getDisplayFileName()} exported.", QMessageBox.StandardButton.Ok)

    def viewPhotoAlbum(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f'viewing photo album file "{dirEntry.getDisplayFileName()}"')
        previewer = D64Gfx.ImagePreviewer(self.palette)
        try:
            scraps = previewer.getPhotoAlbumPreviews(dirEntry, self.currentImage)
            if len(scraps) == 0:
                QMessageBox.warning(self, "Warning", "No readable images in this album.", QMessageBox.StandardButton.Ok)
                return
            self.scrapDialog = PhotoScrapDialog(self, Qt.WindowType.Dialog, scraps, dirEntry.getDisplayFileName())
            self.scrapDialog.show()
        except Exception as exc:
            logging.exception(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return

    def viewPhotoScrap(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f"viewing Photo Scrap")
        previewer = D64Gfx.ImagePreviewer(self.palette)
        try:
            scraps = previewer.getPhotoScrapPreview(dirEntry, self.currentImage)
            if len(scraps) == 0:
                QMessageBox.warning(self, "Warning", "No readable images in this album.", QMessageBox.StandardButton.Ok)
                return
            self.scrapDialog = PhotoScrapDialog(self, Qt.WindowType.Dialog, scraps, dirEntry.getDisplayFileName())
            self.scrapDialog.show()
        except Exception as exc:
            logging.exception(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        
    def viewGeoPaintFile(self):
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        logging.info(f'viewing geoPaint file "{dirEntry.getDisplayFileName()}"')
        previewer = D64Gfx.ImagePreviewer(self.palette)
        try:
            # returns it double size:
            pixmap = previewer.getGeoPaintPreview(dirEntry, self.currentImage)
        except Exception as exc:
            logging.exception(exc)
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return

        title = dirEntry.getDisplayFileName()
        match self.palette:
            case Palette.PEPTO:
                title = title + " (Pepto palette)"
            case Palette.PEPTO_NTSC_SONY:
                title = title + " (Pepto-NTSC-Sony palette)"
            case Palette.COLODORE:
                title = title + " (Colodore palette)"
        logging.debug("instantiating geoPaint dialog")
        geoPaintDialog = GeoPaintDialog(self, Qt.WindowType.Dialog, pixmap, title)
        logging.debug("showing geoPaint dialog")
        geoPaintDialog.show()

    # ======================================================================

    def eventFilter(self, obj, event): # overridden
        if obj is self.tblDirEntries and event.type() == QtCore.QEvent.Type.KeyPress:
            if event.key() in (QtCore.Qt.Key.Key_Return, QtCore.Qt.Key.Key_Enter):
                indexes = self.tblDirEntries.selectedIndexes()
                if indexes: # Enter pressed in table
                    row = indexes[0].row() # table is set for single selection
                    dirEntry = self.model.dirEntries[row]
                    self.defaultDirAction(dirEntry)
            elif event.key() == QtCore.Qt.Key.Key_Home:
                self.tblDirEntries.setCurrentIndex(self.model.createIndex(0, 0))
            elif event.key() == QtCore.Qt.Key.Key_End:
                rowCount = self.model.rowCount(self.model.createIndex(0, 0))
                self.tblDirEntries.setCurrentIndex(self.model.createIndex(rowCount - 1, 0))
        return super().eventFilter(obj, event)

    def doDefaultDirAction(self): # item in directory table double-clicked
        dirEntry = self.model.dirEntries[self.tblDirEntries.selectedIndexes()[0].row()]
        self.defaultDirAction(dirEntry)

    def defaultDirAction(self, dirEntry: DirEntry):
        if dirEntry.isGeosFile():
            permString = dirEntry.getGeosFileHeader().getPermanentNameString()
            if dirEntry.getGeosFileType() == GeosFileType.APPL_DATA:                
                if permString.startswith("Write Image"):
                    self.viewGeoWriteFile(dirEntry)
                    return
                elif permString.startswith("Paint Image"):
                    self.viewGeoPaintFile()
                    return
                elif permString.startswith("photo album"):
                    self.viewPhotoAlbum()
                    return
                elif permString.startswith("Photo Scrap"):
                    self.viewPhotoScrap()
                    return
                elif permString.startswith("text album"):
                    self.viewTextAlbum()
                    return
                elif permString.startswith("Text  Scrap"): # note extra space
                    self.viewTextScrap()
                    return
            elif dirEntry.getGeosFileType() == GeosFileType.FONT:
                self.exploreFont()
                return
        if not dirEntry.isGeosFile() or dirEntry.getGeosFileType() == GeosFileType.NOT_GEOS:
            if dirEntry.getFileType() == FileType.FILETYPE_SEQUENTIAL.code:
                self.viewAsText()
                return

        # fall through: view as hex
        self.viewRawData()

    # ======================================================================

    def showOpenDialog(self):
        if self.props["rememberDirectory"].data == "True":
            try:
                self.startingDir = self.props["startingDirectory"].data
            except KeyError as kxc:
                self.startingDir = str(Path.home())
            fileName = QFileDialog.getOpenFileName(self, 'Open file', self.startingDir)
        else:
            fileName = QFileDialog.getOpenFileName(self, 'Open file', str(Path.home()))
        if fileName[0]: # tuple of filename, selection criteria
            self.props["startingDirectory"] = os.path.dirname(fileName[0])
            self.writeProps()
            self.openImageFile(fileName[0])

    def startAnalysis(self):
        self.thread = QThread(self)
        self.analyzer = Analyzer(self.currentImage)
        self.analyzer.moveToThread(self.thread)
        self.thread.started.connect(self.analyzer.run)
        self.analyzer.progress.connect(self.analysisProgress)
        self.analyzer.finished.connect(self.analysisComplete)
        self.startAnalysisAction.setDisabled(True)
        self.statusBar.showMessage("starting analysis...")
        self.thread.start()

    def analysisProgress(self, message: str):
        logging.info(message)

    def analysisComplete(self, output: list):
        self.thread.quit()
        self.thread.wait()
        self.statusBar.clearMessage()
        message = output[len(output) - 1].text # last message is anomaly count
        QMessageBox.information(self, "Information", message, QMessageBox.StandardButton.Ok)
        pages = []
        pages.append(output)
        try:
            self.plaintextDialog = PlaintextDialog(self, Qt.WindowType.Dialog, pages, CharSet.ASCII, None, PlaintextHeight.TALL)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.plaintextDialog.setWindowTitle(f"Analysis of {self.currentImage.getDirHeader().getDiskName().strip()}")
        self.plaintextDialog.show()
        self.plaintextDialog.txtPlaintext.setFocus()
        self.startAnalysisAction.setDisabled(False)

    def viewDirHeader(self):
        ts = Geometry.getDirHeaderTrackSector(self.currentImage.imageType)
        sector = self.currentImage.readSector(ts)
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, None, sector, ts, True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def viewBam(self):
        try:
            self.bamDialog = BamDialog(self, Qt.WindowType.Dialog, self.currentImage)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.bamDialog.show()

    def showErrors(self):
        errorMap = self.currentImage.getSectorErrorMap()
        errors = 0
        for key in errorMap:
            if errorMap[key] in [SectorErrors.NOT_REPORTED.code, SectorErrors.NO_ERROR.code]:
                continue
            errors += 1
        if not errors:
            QMessageBox.information(self, "Information", "All errors on this disk are either\n\"no error\" or \"not reported\".", QMessageBox.StandardButton.Ok)
            return
        self.sectorErrorDialog = SectorErrorDialog(self, Qt.WindowType.Dialog, errorMap)
        self.sectorErrorDialog.show()

    def viewDirSectors(self):
        if self.currentImage is None:
            QMessageBox.warning(self, "Error", "No image loaded!", QMessageBox.StandardButton.Ok)
            return
        ts = Geometry.getFirstDirTrackSector(self.currentImage.imageType)
        sector = self.currentImage.readSector(ts)
        try:
            self.hexDialog = HexDialog(self, Qt.WindowType.Dialog, None, sector, ts,True, True)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.hexDialog.show()

    def exportGeoWrite(self):
        fileDialog = QFileDialog(self)
        outputDir = fileDialog.getExistingDirectory(self, "Directory for Export", str(Path.home()), QFileDialog.Option.ShowDirsOnly)
        if not outputDir: # user cancelled
            return
        logging.info(f"geoWrite export directory: {outputDir}")
        filesConverted = 0
        for dirEntry in self.model.dirEntries:
            if dirEntry.isGeosFile() and dirEntry.geosFileHeader.getParentApplicationName().startswith("geoWrite"):
                logging.info(f"exporting {dirEntry.getDisplayFileName()}")
                try:
                    pages = self.currentImage.getGeoWriteFileAsLines(dirEntry)
                except Exception as exc:
                    logging.error(exc)
                    QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
                    if isinstance(exc, PartialDataException):
                        pages = exc.getPartialData()
                    else:
                        raise exc
                fileName= dirEntry.getDisplayFileName().replace("/", "-")
                with open(outputDir + os.sep + fileName + ".txt", "w") as f:
                    for page in pages:
                        for line in page:
                            f.write(line.text + "\n")
                f.close()
                filesConverted += 1
        logging.info(f"{filesConverted} geoWrite file(s) exported to {outputDir}.")
        QMessageBox.information(self, "Information", f"{filesConverted} geoWrite file(s) exported to {outputDir}.", QMessageBox.StandardButton.Ok)

    def searchGeoWrite(self):
        try:
            # Open dialog with no data, indicating a search of geoWrite files.
            # When search is invoked from the dialog, it asks us to build a report
            # by calling searchWithinGeoWriteFiles().
            self.plaintextDialog = PlaintextDialog(self, Qt.WindowType.Dialog, [], CharSet.ASCII, PlaintextHeight.TALL)
        except Exception as exc:
            QMessageBox.warning(self, "Warning", str(exc), QMessageBox.StandardButton.Ok)
            return
        self.plaintextDialog.setWindowTitle("Search within geoWrite files")
        self.plaintextDialog.show()
        self.plaintextDialog.txtSearch.setFocus()

    def searchWithinGeoWriteFiles(self, searchString: str, caseSensitive: bool) -> list[list[TextLine]]:
        # callback from PlaintextDialog
        report = [] # list of TextLine
        firstTime = True
        for dirEntry in self.model.dirEntries:
            if dirEntry.isGeosFile() and dirEntry.geosFileHeader.getParentApplicationName().startswith("geoWrite"):
                pages = self.currentImage.getGeoWriteFileAsLines(dirEntry)
                pageNumber = 1; foundOne = False
                for page in pages: # list of pages, which are lists of TextLine
                    lineNumber = 1
                    for line in page:
                        if caseSensitive:
                            hit = searchString in line.text
                        else:
                            hit = searchString.lower() in line.text.lower()
                        if hit:
                            if not foundOne:
                                if firstTime:
                                    firstTime = False  # first time through, don't add a blank line
                                else:
                                    report.append(TextLine("", False))
                                # PlaintextDialog's showTextLines() will treat the error as a heading
                                report.append(TextLine(f"in geoWrite file '{dirEntry.getDisplayFileName()}':", True))
                                foundOne = True
                            report.append(TextLine(f"page {pageNumber}, line {lineNumber}:", False))
                            report.append(line)
                        lineNumber += 1
                    pageNumber += 1
        # Note that we return a single list of lines, not a list of lists.
        return report

    # ======================================================================

    def sizeTable(self):
        i = 0; totalWidth = 0
        while (i < self.model.columnCount(-1)):
            if i == 0:
                # 16 chars in filename, but assuming proportional font
                # totalWidth += self.model.getLongestName(self.fontMetrics())
                totalWidth += self.fontMetrics().boundingRect("M" * 14).width() # fudge factor
            else:
                totalWidth += self.header.sectionSize(i)
            i += 1
        self.tblDirEntries.setMinimumWidth(totalWidth)

        totalHeight = 0;
        i = 0; rowCount = 8 # one directory page
        while i < rowCount:
            if not self.tblDirEntries.verticalHeader().isSectionHidden(i):
                totalHeight += self.tblDirEntries.verticalHeader().sectionSize(i)
            i += 1
        if not self.tblDirEntries.horizontalScrollBar().isHidden():
            totalHeight += self.tblDirEntries.horizontalScrollBar().height()
        if not self.tblDirEntries.horizontalHeader().isHidden():
            totalHeight += self.tblDirEntries.horizontalHeader().height()
        frameWidth = self.tblDirEntries.frameWidth() * 2;
        self.tblDirEntries.setMinimumHeight(totalHeight + frameWidth)
        self.tblDirEntries.verticalScrollBar().setPageStep(8) # one directory page

    def centerWindow(self):
        rect = self.frameGeometry()
        center = self.screen().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def usePeptoPalette(self):
        self.palette = Palette.PEPTO
        self.props["palette"] = Palette.PEPTO.name
        self.writeProps()

    def usePeptoNtscSonyPalette(self):
        self.palette = Palette.PEPTO_NTSC_SONY
        self.props["palette"] = Palette.PEPTO_NTSC_SONY.name
        self.writeProps()

    def useColodorePalette(self):
        self.palette = Palette.COLODORE
        self.props["palette"] = Palette.COLODORE.name
        self.writeProps()

    def rememberDirectory(self, remember: bool):
        self.props["rememberDirectory"] = str(self.rememberAction.isChecked())
        self.writeProps()

    def confirmExit(self, confirm: bool):
        self.props["confirmExit"] = str(self.confirmAction.isChecked())
        self.writeProps()

    def helpAbout(self):
        self.aboutBox = QDialog(self)
        layout = QVBoxLayout()
        layout.setContentsMargins(12, 12, 12, 12)
        sysVersion = sys.version_info
        lblTitle = QLabel(f"{self.title}")
        font = lblTitle.font()
        font.setBold(True)
        lblTitle.setFont(font)
        msg = f"\nRunning under Python {sysVersion.major}.{sysVersion.minor}\n" \
            + f"on {platform.system()} {platform.release()}\n\n" \
            + "code: Cenbe\n" \
            + "QA: Wizard The Cat"
        lblMsg = QLabel(msg)

        picPath = str(Path(__file__).parents[0]) + os.sep + "wizard-icon.png"
        pixmap = QPixmap(picPath)
        lblWizard = QLabel(self)
        lblWizard.setPixmap(pixmap)
        
        okButton = QDialogButtonBox.StandardButton.Ok             
        buttonBox = QDialogButtonBox(okButton)
        buttonBox.accepted.connect(self.accept)

        layout.addWidget(lblTitle)
        layout.addWidget(lblMsg)
        layout.addWidget(lblWizard)
        layout.addWidget(buttonBox)
        self.aboutBox.setLayout(layout)

        self.aboutBox.setWindowTitle("About")
        self.aboutBox.exec()

    def accept(self):
        self.aboutBox.accept()

    def exitProgram(self):
        if self.props["confirmExit"].data == "True":
            button = QMessageBox.question(self, "Exit Program?", "Please Confirm")
            if button == QMessageBox.StandardButton.Yes:
                try:
                    self.close()
                    QApplication.exit(0)
                except Exception as exc:
                    logging.exception(exc)
            else:
                return False
        else:
            logging.debug("calling QApplication.exit(0)")
            QApplication.exit(0)

    def closeEvent(self, closeEvent): # close by button or ctrl-W
        if not self.exitProgram():
            closeEvent.ignore()

    def windowClosing(self):
        try:
            self.currentImage.close()
        except:
            pass

    def openImageFile(self, fileName: str):
        try:
            path = Path(fileName)
            imageName = path.name
            logging.info("opening " + str(path))
            image = DiskImage(path)
            logging.info(f'disk name is "{image.getDirHeader().getDiskName()}"')
            image.readBam() # cache it
            logging.info("reading directory...")
            dirEntries = image.getDirectory()
            msg = f"{len(dirEntries)} directory entries read."
            logging.info(msg)
            self.statusBar.showMessage(msg)
            self.model = DirTableModel(dirEntries)
            self.tblDirEntries.setModel(self.model)
            self.tblDirEntries.clicked.connect(self.rowSelected)
            self.tblDirEntries.activated.connect(self.rowSelected) # Enter pressed
            self.selectionModel = self.tblDirEntries.selectionModel()
            self.selectionModel.currentRowChanged.connect(self.rowSelected)
            self.currentPath = path
            self.currentImage = image

            self.startAnalysisAction.setDisabled(False)
            if self.currentImage.imageType == ImageType.D64_ERROR:
                self.errorsAction.setDisabled(False)
            self.viewDirHeaderAction.setDisabled(False)
            self.viewBamAction.setDisabled(False)
            self.viewDirSectorsAction.setDisabled(False)
            self.exportGeoWriteAction.setDisabled(True)
            self.searchGeoWriteAction.setDisabled(True)
            for dirEntry in dirEntries:
                if dirEntry.isGeosFile() and dirEntry.getGeosFileHeader().getParentApplicationName().startswith("geoWrite"):
                    self.exportGeoWriteAction.setDisabled(False)
                    self.searchGeoWriteAction.setDisabled(False)
                    break
            self.lblDiskNameData.setText(self.currentImage.getDirHeader().getDiskName())
            self.lblImageTypeData.setText(self.currentImage.imageType.description)
            self.lblIsGeosData.setText("yes" if self.currentImage.isGeosImage() else "no")
            self.lblFilesData.setText(str(len(self.model.dirEntries)))
            self.lblBlocksFreeData.setText(str(self.currentImage.getBlocksFree()))
            self.sizeTable()
            if dirEntries: # i.e. if not empty
                self.tblDirEntries.selectRow(0) # auto-select first row
            else:
                self.lblPermNameData.setText(" " * 20)
                self.lblParentAppData.setText(" " * 20)
                self.lblInfo.setText(" ")
                self.lblIcon.clear()
            self.setWindowTitle(f"{self.title}  |  {imageName}")
            if self.currentImage.imageType == ImageType.D64_ERROR:
                message = f"This image is a {self.currentImage.imageType.description}."
                response = QMessageBox.question(self, "View Errors?", message)
                if response == QMessageBox.StandardButton.Yes:
                    self.showErrors()
        except Exception as exc:
            logging.exception(exc)
            QMessageBox.critical(self, "Error loading disk image", str(exc), QMessageBox.StandardButton.Ok)

    def rowSelected(self, index):
        dirHeader = self.currentImage.getDirHeader()
        dirEntry = self.model.dirEntries[index.row()]
        geosFileHeader = self.currentImage.getGeosFileHeader(dirEntry)

        if geosFileHeader:
            self.lblPermNameData.setText(geosFileHeader.getPermanentNameString())
            if dirEntry.getGeosFileType() == GeosFileType.FONT:
                self.lblParentAppData.setText(" " * 20) # this field used for font data
            else:
                self.lblParentAppData.setText(geosFileHeader.getParentApplicationName())
            self.lblInfo.setText(geosFileHeader.getInfo())
        else:
            self.lblPermNameData.setText(" " * 20)
            self.lblParentAppData.setText(" " * 20)
            self.lblInfo.setText(" ")

        if dirEntry.getGeosFileType() == GeosFileType.NOT_GEOS:
            self.lblIcon.clear()
        else:
            pixmap = D64Gfx.getGeosIcon(dirEntry)
            self.lblIcon.setPixmap(pixmap)

    def readProps(self):
        self.props = Properties()
        try:
            with open(str(Path.home()) + os.sep + "DiskWrangler.properties", "rb") as f:
                self.props.load(f, "utf-8")
        except Exception as exc:
            logging.info("Properties file not found, creating.")
            self.props["rememberDirectory"] = "False"
            self.props["confirmExit"] = "True"
            self.props["palette"] = "PEPTO"
            self.writeProps()

        if self.props["rememberDirectory"].data == "True":
            self.rememberAction.setChecked(True)
        else:
            self.rememberAction.setChecked(False)

        if self.props["confirmExit"].data == "True":
            self.confirmAction.setChecked(True)
        else:
            self.confirmAction.setChecked(False)

        logging.debug(f"palette: {self.props['palette'].data}")
        if self.props["palette"].data == Palette.PEPTO.name:
            self.palette = Palette.PEPTO
            self.peptoAction.setChecked(True)
        elif self.props["palette"].data == Palette.PEPTO_NTSC_SONY.name:
            self.palette = Palette.PEPTO_NTSC_SONY
            self.peptoNtscSonyAction.setChecked(True)
        elif self.props["palette"].data == Palette.COLODORE.name:
            self.palette = Palette.COLODORE
            self.colodoreAction.setChecked(True)
                
    def writeProps(self):
        try:
            with open(str(Path.home()) + os.sep + "DiskWrangler.properties", "wb") as f:
                self.props.store(f, encoding="utf-8")
        except Exception as exc:
            QMessageBox.critical(self, "Error writing properties file", str(exc), QMessageBox.StandardButton.Ok)

#======================================================================

print("DiskWrangler class running")
logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                    filename=str(Path.home()) + os.sep + "DiskWrangler.log", encoding="utf-8", style="{",
                    format="{asctime} {levelname} {filename}:{lineno}: {message}")
console = logging.StreamHandler()
logging.getLogger().addHandler(console)
logging.info("")
#FIXME
#logTitle = f"Cenbe's Disk Wrangler {version('DiskWrangler')} (Python version)"
logTitle = "Cenbe's Disk Wrangler (Python version)"
logging.info('-' * len(logTitle))
logging.info(logTitle)
logging.info('-' * len(logTitle))
print(f"sys.prefix: {sys.prefix}, sys.base_prefix: {sys.base_prefix}")
if sys.prefix == sys.base_prefix:
    logging.debug("not running in a venv")
else:
    logging.debug("running in a venv")

app = QtWidgets.QApplication(sys.argv)
window = DiskWrangler()
window.show()
app.exec()
