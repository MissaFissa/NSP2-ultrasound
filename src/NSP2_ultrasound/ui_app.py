# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform, QAction)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QComboBox, QLineEdit, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QVBoxLayout, QWidget, QFileDialog)

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from pyqtgraph import PlotWidget

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        if not MainWindow.objectName():

            MainWindow.setObjectName(u"MainWindow")
            
        MainWindow.resize(1200, 800)
        MainWindow.setStyleSheet(u"background-color: b;\n" "border-color: black")      

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: black")

        self.vbox = QVBoxLayout(self.centralwidget)
        self.vbox.setObjectName(u"vbox")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.hbox = QHBoxLayout()
        self.hbox.setObjectName(u"hbox")

        self.vbox.addLayout(self.hbox)

        self.start = QLineEdit(self.centralwidget)
        self.start.setObjectName(u"start")
        self.start.setStyleSheet(u"background-color: black; border-color: white")

        self.hbox.addWidget(self.start)

        self.stop = QLineEdit(self.centralwidget)
        self.stop.setObjectName(u"stop")
        self.stop.setStyleSheet(u"background-color: black; border-color: white")

        self.hbox.addWidget(self.stop)
    
        self.name = QComboBox()
        self.name.setStyleSheet(u"background-color: dimgrey")
        self.name.setObjectName(u"name")
        self.name.addItem("aluminium")
        self.name.addItem("copper")
        self.name.addItem("antikal_spray")

        self.vbox.addWidget(self.name)

        self.plot_button = QPushButton(self.centralwidget)
        self.plot_button.setObjectName(u"plot")
        self.plot_button.setStyleSheet(u"background-color: dimgrey")

        self.vbox.addWidget(self.plot_button)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 37))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):

        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Ultrasoon experiment", None))
        self.plot_button.setText(QCoreApplication.translate("MainWindow", u"plot", None))