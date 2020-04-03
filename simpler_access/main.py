import sys
import subprocess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from simple_raccess.gui import Ui_mainWindow
from simple_raccess.addmachine import Ui_addmachine
from simple_raccess.tunnel import Ui_tunnel
from simple_raccess.importmachine import Ui_importmachine
import simple_raccess.app as ulc

class TunnelingWindow(QDialog, Ui_tunnel):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.list_of_tunnels = []

        self.add_button.clicked.connect(lambda state, lot=self.list_of_tunnels: self.add_entry(lot))
        self.browse_button.clicked.connect(self.open_file)
        self.confirm_button.clicked.connect(self.confirm)
        self.clear_button.clicked.connect(self.clear)

    def open_file(self):
        f = QFileDialog.getOpenFileName(self, "Browse...", "","Any (*)")
        if f:
            self.key_line.setText(f[0])

    def clear(self):
        self.name_line.setText("")
        self.port_line.setText("")
        self.host_line.setText("")
        self.user_line.setText("")
        self.password_line.setText("")
        self.key_line.setText("")

    def add_entry(self, lot):
        name = self.name_line.text()
        host = self.host_line.text()
        port = self.port_line.text()
        user = self.user_line.text()
        pwd = self.password_line.text()
        key = self.key_line.text()

        if "" in [name, host, port, user]:
            alert = QMessageBox()
            alert.setText("Please check your input fields")
            alert.setStandardButtons(alert.Ok)
            if alert.exec_() == alert.Ok:
                return

        entries = {
                'name': name, 
                'host': host, 
                'port': port, 
                'username': user, 
                'password': pwd, 
                'key': key
                }

        lot.append(entries)
        self.clear()
        self.update_table(entries)
        self.setDelete()

    def update_table(self, lot):
        row_posit = self.tunnel_entries.rowCount()
        self.tunnel_entries.insertRow(row_posit)
        column = 0
        for entry in lot:
            print(entry)
            val = QTableWidgetItem(lot[entry])
            val.setFlags(Qt.ItemIsEnabled)
            self.tunnel_entries.setItem(row_posit, column, val)
            column += 1 

    def confirm(self):
        self.accept()

    def setDelete(self):
        column = 6

        totalRows = self.tunnel_entries.rowCount()
        for row in range(totalRows):
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda state, row=row: self.removeRow(row))
            self.tunnel_entries.setCellWidget(row, column, remove_button)

    def removeRow(self, row):
        self.tunnel_entries.removeRow(row)
        self.setDelete()
        
class AddMachineDialog(QDialog, Ui_addmachine):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.machine_info = {}
        self.tunnel_configuration = ""

        self.add_button.clicked.connect(self.add_machine)
        self.browse_button.clicked.connect(self.open_file)
        self.clear_button.clicked.connect(self.clear_text)
        self.configure_button.clicked.connect(self.configure_tunnel)
        self.portforward_check.clicked.connect(self.forwarding)

    def forwarding(self):
        if self.portforward_check.isChecked():
            # enable fields
            for i in [self.localhost_line, self.localport_line, self.remotehost_line,
                    self.remoteport_line, self.local_forwarding, self.remote_forwarding]:
                i.setEnabled(True)
        else:
            # clear and disable fields
            for i in [self.localhost_line, self.localport_line, self.remotehost_line,
                    self.remoteport_line, self.local_forwarding, self.remote_forwarding]:
                if type(i) == QLineEdit:
                    i.setText("")
                else:
                    i.setAutoExclusive(False)
                    i.setChecked(False)
                    i.setAutoExclusive(True)
                i.setEnabled(False)

    def add_machine(self):
        if self.portforward_check.isChecked():
            forward = {
                'type': 'remote' if self.remote_forwarding.isChecked() else 'local',
                'localhost': self.localhost_line.text(),
                'localport': self.localport_line.text(),
                'remotehost': self.remotehost_line.text(),
                'remoteport': self.remoteport_line.text()
            }
        else:
            forward = ''
        self.machine_info = {
                'name': self.name_line.text(), 
                'host': self.host_line.text(),
                'port': self.port_line.text(), 
                'forward': forward,
                'username': self.user_line.text(),
                'password': self.password_line.text(), 
                'key': self.key_line.text(),
                'tunnel' :self.tunnel_configuration
                }
        if "" in [self.machine_info['name'], 
                self.machine_info['port'],
                self.machine_info['host'],
                self.machine_info['username']]:
            alert = QMessageBox()
            alert.setText("Please check your input fields")
            alert.setStandardButtons(alert.Ok)
            if alert.exec_() == alert.Ok:
                return
        self.accept()

    def open_file(self):
        f = QFileDialog.getOpenFileName(self, "Browse...", "","Any (*)")
        if f:
            self.key_line.setText(f[0])

    def clear_text(self):
        for line in [self.name_line, self.host_line, self.port_line, self.user_line,
                self.password_line, self.key_line]:
            line.setText("")

    def configure_tunnel(self):
        dialog = TunnelingWindow()
        if dialog.exec_():
            self.tunnel_configuration = dialog.list_of_tunnels


class ImportMachineDialog(QDialog, Ui_importmachine):
    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.browse_button.clicked.connect(self.browse)
        self.confirm_button.clicked.connect(self.addMachine)

    def browse(self):
        f = QFileDialog.getOpenFileName(self, "Browse...", "","Any (*)")
        if f:
            self.file_line.setText(f[0])
    def addMachine(self):
        ulc.add_machine(xml=self.file_line.text())
        self.accept()

class MainWindow(QMainWindow, Ui_mainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.machines = ulc.show_machines()

        self.populateTable()
        self.addmachine_button.clicked.connect(self.addmachineDialog)
        self.importxml_button.clicked.connect(self.importMachine)
        self.show()

    def importMachine(self):
        dialog = ImportMachineDialog()
        if dialog.exec_():
            self.machines = ulc.show_machines()
            self.populateTable()

    def addmachineDialog(self):
        dialog = AddMachineDialog()
        if dialog.exec_():
            print(dialog.machine_info)
            ulc.write_machine(dialog.machine_info)
            self.machines = ulc.show_machines()
            self.populateTable()

    def populateTable(self):
        self.table_view.setRowCount(len(self.machines))
        
        row = 0
        for machine in self.machines:
            column = 0
            for attr in machine:
                val = QTableWidgetItem(machine[column])
                val.setFlags(Qt.ItemIsEnabled)
                self.table_view.setItem(row, column, val)
                column += 1

            connect_button = QPushButton("Connect")

            connect_button.clicked.connect(lambda state, row=row: 
                    subprocess.call("gnome-terminal -- python3 app.py -c {}".format(row+1), shell=True))
            self.table_view.setCellWidget(row, column, connect_button)
            row += 1

        self.setDelete()

    def setDelete(self):
        column = 9

        totalRows = self.table_view.rowCount()
        for row in range(totalRows):
            remove_button = QPushButton("Remove")
            remove_button.clicked.connect(lambda state, row=row: self.removeRow(row))
            self.table_view.setCellWidget(row, column, remove_button)

    def removeRow(self, row):
        cfm = QMessageBox()
        cfm.setText("Are you sure you wish to remove Connection #{}".format(row+1))
        cfm.setStandardButtons(cfm.Yes | cfm.No)
        if cfm.exec_() == cfm.Yes:
            self.table_view.removeRow(row) 
            ulc.delete_machine(m_id=row+1, gui=True)
            self.setDelete()
        self.machines = ulc.show_machines()
        self.populateTable()
 
def run():
    app = QApplication(sys.argv)
    myapp = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MainWindow()
    sys.exit(app.exec_())
