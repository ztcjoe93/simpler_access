# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tunnel.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_tunnel(object):
    def setupUi(self, tunnel):
        tunnel.setObjectName("tunnel")
        tunnel.resize(837, 589)
        self.browse_button = QtWidgets.QPushButton(tunnel)
        self.browse_button.setGeometry(QtCore.QRect(630, 120, 89, 25))
        self.browse_button.setObjectName("browse_button")
        self.port_line = QtWidgets.QLineEdit(tunnel)
        self.port_line.setGeometry(QtCore.QRect(120, 80, 71, 25))
        self.port_line.setObjectName("port_line")
        self.port_label = QtWidgets.QLabel(tunnel)
        self.port_label.setGeometry(QtCore.QRect(40, 80, 67, 17))
        self.port_label.setObjectName("port_label")
        self.key_label = QtWidgets.QLabel(tunnel)
        self.key_label.setGeometry(QtCore.QRect(320, 120, 31, 21))
        self.key_label.setObjectName("key_label")
        self.confirm_button = QtWidgets.QPushButton(tunnel)
        self.confirm_button.setGeometry(QtCore.QRect(640, 530, 89, 25))
        self.confirm_button.setObjectName("confirm_button")
        self.host_line = QtWidgets.QLineEdit(tunnel)
        self.host_line.setGeometry(QtCore.QRect(120, 120, 151, 25))
        self.host_line.setObjectName("host_line")
        self.name_line = QtWidgets.QLineEdit(tunnel)
        self.name_line.setGeometry(QtCore.QRect(120, 40, 151, 25))
        self.name_line.setObjectName("name_line")
        self.host_label = QtWidgets.QLabel(tunnel)
        self.host_label.setGeometry(QtCore.QRect(40, 120, 67, 17))
        self.host_label.setObjectName("host_label")
        self.user_label = QtWidgets.QLabel(tunnel)
        self.user_label.setGeometry(QtCore.QRect(320, 40, 81, 17))
        self.user_label.setObjectName("user_label")
        self.password_label = QtWidgets.QLabel(tunnel)
        self.password_label.setGeometry(QtCore.QRect(320, 80, 67, 17))
        self.password_label.setObjectName("password_label")
        self.password_line = QtWidgets.QLineEdit(tunnel)
        self.password_line.setGeometry(QtCore.QRect(400, 80, 151, 25))
        self.password_line.setObjectName("password_line")
        self.clear_button = QtWidgets.QPushButton(tunnel)
        self.clear_button.setGeometry(QtCore.QRect(620, 170, 89, 25))
        self.clear_button.setObjectName("clear_button")
        self.tunnel_entries = QtWidgets.QTableWidget(tunnel)
        self.tunnel_entries.setGeometry(QtCore.QRect(40, 220, 721, 281))
        self.tunnel_entries.setGridStyle(QtCore.Qt.DotLine)
        self.tunnel_entries.setObjectName("tunnel_entries")
        self.tunnel_entries.setColumnCount(7)
        self.tunnel_entries.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tunnel_entries.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tunnel_entries.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tunnel_entries.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tunnel_entries.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tunnel_entries.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tunnel_entries.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tunnel_entries.setHorizontalHeaderItem(6, item)
        self.name_label = QtWidgets.QLabel(tunnel)
        self.name_label.setGeometry(QtCore.QRect(40, 40, 67, 17))
        self.name_label.setObjectName("name_label")
        self.key_line = QtWidgets.QLineEdit(tunnel)
        self.key_line.setGeometry(QtCore.QRect(400, 120, 221, 25))
        self.key_line.setMaxLength(32765)
        self.key_line.setReadOnly(True)
        self.key_line.setObjectName("key_line")
        self.user_line = QtWidgets.QLineEdit(tunnel)
        self.user_line.setGeometry(QtCore.QRect(400, 40, 151, 25))
        self.user_line.setObjectName("user_line")
        self.add_button = QtWidgets.QPushButton(tunnel)
        self.add_button.setGeometry(QtCore.QRect(520, 170, 89, 25))
        self.add_button.setObjectName("add_button")

        self.retranslateUi(tunnel)
        QtCore.QMetaObject.connectSlotsByName(tunnel)
        tunnel.setTabOrder(self.name_line, self.port_line)
        tunnel.setTabOrder(self.port_line, self.host_line)
        tunnel.setTabOrder(self.host_line, self.user_line)
        tunnel.setTabOrder(self.user_line, self.password_line)
        tunnel.setTabOrder(self.password_line, self.key_line)
        tunnel.setTabOrder(self.key_line, self.browse_button)
        tunnel.setTabOrder(self.browse_button, self.add_button)
        tunnel.setTabOrder(self.add_button, self.clear_button)
        tunnel.setTabOrder(self.clear_button, self.tunnel_entries)
        tunnel.setTabOrder(self.tunnel_entries, self.confirm_button)

    def retranslateUi(self, tunnel):
        _translate = QtCore.QCoreApplication.translate
        tunnel.setWindowTitle(_translate("tunnel", "Tunnel Configuration"))
        self.browse_button.setText(_translate("tunnel", "Browse"))
        self.port_label.setText(_translate("tunnel", "Port"))
        self.key_label.setText(_translate("tunnel", "Key"))
        self.confirm_button.setText(_translate("tunnel", "Confirm"))
        self.host_label.setText(_translate("tunnel", "Host/IP"))
        self.user_label.setText(_translate("tunnel", "Username"))
        self.password_label.setText(_translate("tunnel", "Password"))
        self.clear_button.setText(_translate("tunnel", "Clear"))
        item = self.tunnel_entries.horizontalHeaderItem(0)
        item.setText(_translate("tunnel", "Name"))
        item = self.tunnel_entries.horizontalHeaderItem(1)
        item.setText(_translate("tunnel", "Host"))
        item = self.tunnel_entries.horizontalHeaderItem(2)
        item.setText(_translate("tunnel", "Port"))
        item = self.tunnel_entries.horizontalHeaderItem(3)
        item.setText(_translate("tunnel", "Username"))
        item = self.tunnel_entries.horizontalHeaderItem(4)
        item.setText(_translate("tunnel", "Password"))
        item = self.tunnel_entries.horizontalHeaderItem(5)
        item.setText(_translate("tunnel", "Key"))
        self.name_label.setText(_translate("tunnel", "Name"))
        self.add_button.setText(_translate("tunnel", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    tunnel = QtWidgets.QDialog()
    ui = Ui_tunnel()
    ui.setupUi(tunnel)
    tunnel.show()
    sys.exit(app.exec_())