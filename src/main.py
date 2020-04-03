import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QGridLayout, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import PyQt5 as qt

import pyqtgraph as pg
import numpy as np

import cv2

class ImageCaptureThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.stopRunning = False
        cap = cv2.VideoCapture(0)
        while not self.stopRunning:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        self.stopRunning = True

class DebugImageThread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        self.stopRunning = False
        cap = cv2.VideoCapture(0)
        while not self.stopRunning:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

    def stop(self):
        self.stopRunning = True

class StatisticsWindow():
    def init_ui(self, mainWindow):
        layout = QGridLayout()
        layout.setSpacing(20)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)

        mainTitle = QLabel("Auto Center Tool")
        mainTitle.setFont(QtGui.QFont("Lato", pointSize=20, weight=QtGui.QFont.Bold))

        self.mainLabel = QLabel("Main")
        self.statisticsLabel = QLabel("Statistics")
        self.statisticsLabel.setStyleSheet("background-color: #4a4a4a")
        self.settingsLabel = QLabel("Settings")

        vbox.addWidget(mainTitle)
        vbox.addWidget(self.mainLabel)
        vbox.addWidget(self.statisticsLabel)
        vbox.addWidget(self.settingsLabel)
        vbox.addStretch(1)

        chart = self.totalAcceptedChart()

        layout.addLayout(vbox, 0, 0)
        layout.addWidget(chart, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        mainWindow.setCentralWidget(widget)

    def totalAcceptedChart(self):
        plot = pg.PlotWidget()
        plot.setBackground('w')

        pen = pg.mkPen(color=(255,0,0))
        y1 = np.linspace(0,20, num=2)
        x = np.arange(2)
        barGraph = pg.BarGraphItem(x=x, height=y1, width = 0.5, brush='r', pen=pen)

        plot.addItem(barGraph)
        return plot

class SettingsWindow():
    def init_ui(self, mainWindow):
        layout = QGridLayout()
        layout.setSpacing(20)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)

        mainTitle = QLabel("Auto Center Tool")
        mainTitle.setFont(QtGui.QFont("Lato", pointSize=20, weight=QtGui.QFont.Bold))

        self.mainLabel = QLabel("Main")
        self.statisticsLabel = QLabel("Statistics")
        self.settingsLabel = QLabel("Settings")
        self.settingsLabel.setStyleSheet("background-color: #4a4a4a")

        vbox.addWidget(mainTitle)
        vbox.addWidget(self.mainLabel)
        vbox.addWidget(self.statisticsLabel)
        vbox.addWidget(self.settingsLabel)
        vbox.addStretch(1)

        self.imageLabel = QLabel(mainWindow)

        hbox = QHBoxLayout()

        GLabel = QLabel("G")
        GLabel.setStyleSheet("background-color: #4a4a4a");
        GLabel.setAlignment(Qt.AlignCenter)
        GLabel.setFont(QtGui.QFont("Lato", pointSize=20, weight=QtGui.QFont.Bold))

        NGLabel = QLabel("NG")
        NGLabel.setStyleSheet("background-color: #4a4a4a")
        NGLabel.setAlignment(Qt.AlignCenter)
        NGLabel.setFont(QtGui.QFont("Lato", pointSize=20, weight=QtGui.QFont.Bold))

        hbox.addWidget(GLabel)
        hbox.addWidget(NGLabel)

        rightVBox = QVBoxLayout()
        rightVBox.setSpacing(10)

        xCenterLabel = QLabel('X:   0   ')
        xCenterLabel.setFont(QtGui.QFont("Lato", pointSize=20))

        yCenterLabel = QLabel('Y:   0   ')
        yCenterLabel.setFont(QtGui.QFont("Lato", pointSize=20))

        rightVBox.addStretch(1)
        rightVBox.addWidget(xCenterLabel)
        rightVBox.addWidget(yCenterLabel)
        rightVBox.addStretch(10)

        layout.addLayout(vbox, 0, 0)
        layout.addLayout(hbox, 1, 1)
        layout.addLayout(rightVBox, 0, 2)
        layout.addWidget(self.imageLabel, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        mainWindow.setCentralWidget(widget)

class MainWindow():
    def init_ui(self, mainWindow):
        layout = QGridLayout()
        layout.setSpacing(20)

        vbox = QVBoxLayout()
        vbox.setSpacing(10)

        mainTitle = QLabel("Auto Center Tool")
        mainTitle.setFont(QtGui.QFont("Lato", pointSize=20, weight=QtGui.QFont.Bold))

        self.mainLabel = QLabel("Main")
        self.mainLabel.setStyleSheet("background-color: #4a4a4a")
        self.statisticsLabel = QLabel("Statistics")
        self.settingsLabel = QLabel("Settings")

        vbox.addWidget(mainTitle)
        vbox.addWidget(self.mainLabel)
        vbox.addWidget(self.statisticsLabel)
        vbox.addWidget(self.settingsLabel)
        vbox.addStretch(1)

        self.imageLabel = QLabel(mainWindow)

        hbox = QHBoxLayout()

        GLabel = QLabel("G")
        GLabel.setStyleSheet("background-color: #4a4a4a");
        GLabel.setAlignment(Qt.AlignCenter)
        GLabel.setFont(QtGui.QFont("Lato", pointSize=20, weight=QtGui.QFont.Bold))

        NGLabel = QLabel("NG")
        NGLabel.setStyleSheet("background-color: #4a4a4a")
        NGLabel.setAlignment(Qt.AlignCenter)
        NGLabel.setFont(QtGui.QFont("Lato", pointSize=20, weight=QtGui.QFont.Bold))

        hbox.addWidget(GLabel)
        hbox.addWidget(NGLabel)

        rightVBox = QVBoxLayout()
        rightVBox.setSpacing(10)

        xCenterLabel = QLabel('X:   0   ')
        xCenterLabel.setFont(QtGui.QFont("Lato", pointSize=20))

        yCenterLabel = QLabel('Y:   0   ')
        yCenterLabel.setFont(QtGui.QFont("Lato", pointSize=20))

        rightVBox.addStretch(1)
        rightVBox.addWidget(xCenterLabel)
        rightVBox.addWidget(yCenterLabel)
        rightVBox.addStretch(10)

        layout.addLayout(vbox, 0, 0)
        layout.addLayout(hbox, 1, 1)
        layout.addLayout(rightVBox, 0, 2)
        layout.addWidget(self.imageLabel, 0, 1)

        widget = QWidget()
        widget.setLayout(layout)
        mainWindow.setCentralWidget(widget)

class MasterWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MasterWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Auto Center Tool")

        self.mainWindow = MainWindow()
        self.statsWindow = StatisticsWindow()
        self.settingsWindow = SettingsWindow()

        self.imageCap = ImageCaptureThread(self)
        self.settingsImageCap = DebugImageThread(self)

        self.showMainWindow(None)

    @pyqtSlot(QImage)
    def setImageCap(self,image):
        self.mainWindow.imageLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setSettingsImage(self,image):
        self.settingsWindow.imageLabel.setPixmap(QPixmap.fromImage(image))

    def stopImageSettingsCap(self):
        self.settingsImageCap.stop()
        self.settingsImageCap.wait()

    def stopImageCap(self):
        self.imageCap.stop()
        self.imageCap.wait()

    def showMainWindow(self, event):
        self.stopImageSettingsCap()

        self.mainWindow.init_ui(self)
        self.mainWindow.statisticsLabel.mousePressEvent = self.showStatsMenu
        self.mainWindow.settingsLabel.mousePressEvent = self.showSettingsMenu

        self.imageCap.changePixmap.connect(self.setImageCap)
        self.imageCap.start()

        self.show()

    def showStatsMenu(self, event):
        self.stopImageCap()
        self.stopImageSettingsCap()

        self.statsWindow.init_ui(self)
        self.statsWindow.mainLabel.mousePressEvent = self.showMainWindow
        self.statsWindow.settingsLabel.mousePressEvent = self.showSettingsMenu

        self.show()

    def showSettingsMenu(self, event):
        self.stopImageCap()

        self.settingsWindow.init_ui(self)
        self.settingsWindow.mainLabel.mousePressEvent = self.showMainWindow
        self.settingsWindow.statisticsLabel.mousePressEvent = self.showStatsMenu

        self.settingsImageCap.changePixmap.connect(self.setSettingsImage)
        self.settingsImageCap.start()

        self.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)

    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

    masterWindow = MasterWindow()
    sys.exit(app.exec_())