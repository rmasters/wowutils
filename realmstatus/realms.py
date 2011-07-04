# -*- coding: utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import battlenet
from battlenet import Connection, Realm

class Main(QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        
        # Window options
        self.statusBar().showMessage("Ready")
        self.resize(500, 600)
        self.setWindowTitle("Realm Status")
        
        self.setup_ui()
        self.setup_menubar()
        
    def setup_ui(self):
        # Central widget
        centralWidget = QWidget(self)
        # Container
        self.container = QVBoxLayout(centralWidget)
        # Set layout of central widget
        centralWidget.setLayout(self.container)
        # Set central widget of MainWindow
        self.setCentralWidget(centralWidget)
        
        # Header
        title = QLabel("<b>All realms in Europe</b>")
        self.container.addWidget(title)
        
        # Content view
        realmScroll = QScrollArea(self.container.widget())
        realmScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        realmScroll.setWidgetResizable(True)
        
        realmInner = QWidget()
        realmScroll.setWidget(realmInner)
        
        self.realmLayout = QVBoxLayout(realmInner)
        
        
        #realmScroll.setWidget(self.realmLayout.widget())
        self.container.addWidget(realmScroll)
    
    def add_realm(self, realm):
        rContainer = QWidget(self.realmLayout.widget())
        if realm.is_online():
            rContainer.setStyleSheet("background: rgb(94, 130, 126)")
        else:
            rContainer.setStyleSheet("background: rgb(255, 47, 36)")
        
        rLayout = QHBoxLayout(rContainer)
        
        # Realm info labels
        name = QLabel("<font style='font-size: 15pt; font-weight: bold;'>" + QString(realm.name) + " <sup>(" + realm.type + ")</sup></font>")
        rLayout.addWidget(name)
        
        self.realmLayout.addWidget(rContainer)
    
    def showOptions(self):
        Options().exec_()
    
    def setup_menubar(self):
        # Options entry
        options = QtGui.QAction("Options", self)
        options.setShortcut("Ctrl+O")
        options.setStatusTip("Change your region and favourite realms")
        self.connect(options, QtCore.SIGNAL("triggered()"), self.showOptions)
        
        # Exit entry
        exit = QtGui.QAction("Exit", self)
        exit.setShortcut("Ctrl+Q")
        exit.setStatusTip("Exit application")
        self.connect(exit, QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))
        
        menubar = self.menuBar()
        menu = menubar.addMenu("&Menu")
        menu.addAction(options)
        menu.addAction(exit)
        view = menubar.addMenu("&View")
        view.addAction(QtGui.QAction("All realms", self))
        view.addAction(QtGui.QAction("Favourite realms", self))

class Options(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        
        self.setupUi()
    
    def setupUi(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        group = QGroupBox("Region and favourite realm selection")
        layout.addWidget(group)
        groupLayout = QVBoxLayout(group)
        group.setLayout(groupLayout)
        
        """Region select"""
        region = QComboBox()
        region.addItem("Europe", QVariant(battlenet.EUROPE))
        region.addItem("United States", QVariant(battlenet.UNITED_STATES))
        region.addItem("Korea", QVariant(battlenet.KOREA))
        region.addItem("Taiwan", QVariant(battlenet.TAIWAN))
        self.connect(region, QtCore.SIGNAL("QtSig()"), self.updateRegion)
        
        groupLayout.addWidget(QLabel("Your region"))
        groupLayout.addWidget(region)
        
        """Realm select"""
    
    def updateRegion(self):
        pass

if __name__ == "__main__":
    conn = Connection()
    region = battlenet.EUROPE
    
    app = QApplication(sys.argv)
    main = Main()
    main.show()

    #my_realms = ["Shadowsong", "Skullcrusher"]
    my_realms = []

    if len(my_realms) == 0:
        for realm in conn.get_all_realms(region):
            main.add_realm(realm)
    else:
        for realm in conn.get_realms(region, my_realms):
            main.add_realm(realm)
            
    app.exec_()