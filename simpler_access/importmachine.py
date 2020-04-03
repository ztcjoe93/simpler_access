# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importmachine.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_importmachine(object):
    def setupUi(self, importmachine):
        importmachine.setObjectName("importmachine")
        importmachine.resize(400, 300)
        self.browse_button = QtWidgets.QPushButton(importmachine)
        self.browse_button.setGeometry(QtCore.QRect(140, 180, 89, 25))
        self.browse_button.setObjectName("browse_button")
        self.file_label = QtWidgets.QLabel(importmachine)
        self.file_label.setGeometry(QtCore.QRect(60, 80, 31, 21))
        self.file_label.setObjectName("file_label")
        self.file_line = QtWidgets.QLineEdit(importmachine)
        self.file_line.setGeometry(QtCore.QRect(140, 80, 221, 25))
        self.file_line.setMaxLength(32765)
        self.file_line.setReadOnly(True)
        self.file_line.setObjectName("file_line")
        self.confirm_button = QtWidgets.QPushButton(importmachine)
        self.confirm_button.setGeometry(QtCore.QRect(280, 250, 89, 25))
        self.confirm_button.setObjectName("confirm_button")

        self.retranslateUi(importmachine)
        QtCore.QMetaObject.connectSlotsByName(importmachine)
        importmachine.setTabOrder(self.file_line, self.browse_button)
        importmachine.setTabOrder(self.browse_button, self.confirm_button)

    def retranslateUi(self, importmachine):
        _translate = QtCore.QCoreApplication.translate
        importmachine.setWindowTitle(_translate("importmachine", "Import Machine"))
        self.browse_button.setText(_translate("importmachine", "Browse"))
        self.file_label.setText(_translate("importmachine", "File"))
        self.confirm_button.setText(_translate("importmachine", "Confirm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    importmachine = QtWidgets.QDialog()
    ui = Ui_importmachine()
    ui.setupUi(importmachine)
    importmachine.show()
    sys.exit(app.exec_())
