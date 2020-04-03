# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(1321, 619)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(mainWindow.sizePolicy().hasHeightForWidth())
        mainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addmachine_button = QtWidgets.QPushButton(self.centralwidget)
        self.addmachine_button.setGeometry(QtCore.QRect(10, 60, 141, 51))
        self.addmachine_button.setAutoDefault(False)
        self.addmachine_button.setObjectName("addmachine_button")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(150, 0, 20, 601))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.table_view = QtWidgets.QTableWidget(self.centralwidget)
        self.table_view.setGeometry(QtCore.QRect(180, 10, 1131, 581))
        self.table_view.setColumnCount(10)
        self.table_view.setObjectName("table_view")
        self.table_view.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_view.setHorizontalHeaderItem(9, item)
        self.table_view.horizontalHeader().setCascadingSectionResizes(False)
        self.importxml_button = QtWidgets.QPushButton(self.centralwidget)
        self.importxml_button.setGeometry(QtCore.QRect(10, 120, 141, 51))
        self.importxml_button.setAutoDefault(False)
        self.importxml_button.setObjectName("importxml_button")
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)
        mainWindow.setTabOrder(self.addmachine_button, self.importxml_button)
        mainWindow.setTabOrder(self.importxml_button, self.table_view)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "SSH GUI Client"))
        self.addmachine_button.setText(_translate("mainWindow", "Add Machine"))
        item = self.table_view.horizontalHeaderItem(0)
        item.setText(_translate("mainWindow", "Machine"))
        item = self.table_view.horizontalHeaderItem(1)
        item.setText(_translate("mainWindow", "Host"))
        item = self.table_view.horizontalHeaderItem(2)
        item.setText(_translate("mainWindow", "Port"))
        item = self.table_view.horizontalHeaderItem(3)
        item.setText(_translate("mainWindow", "Forwarding"))
        item = self.table_view.horizontalHeaderItem(4)
        item.setText(_translate("mainWindow", "Username"))
        item = self.table_view.horizontalHeaderItem(5)
        item.setText(_translate("mainWindow", "Password"))
        item = self.table_view.horizontalHeaderItem(6)
        item.setText(_translate("mainWindow", "Key"))
        item = self.table_view.horizontalHeaderItem(7)
        item.setText(_translate("mainWindow", "Jumphosts"))
        item = self.table_view.horizontalHeaderItem(9)
        item.setText(_translate("mainWindow", " "))
        self.importxml_button.setText(_translate("mainWindow", "Import from XML"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
