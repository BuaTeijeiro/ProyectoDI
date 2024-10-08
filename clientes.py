from PyQt6 import QtWidgets, QtGui

import eventos
import var
import conexion

class Clientes:
    @staticmethod
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnicli.setText(str(dni))
            check = eventos.Eventos.validarDNI(dni)
            if check:
                var.ui.txtDnicli.setStyleSheet('background-color: rgb(252, 255, 225)')
            else:
                var.ui.txtDnicli.setStyleSheet('background-color:#FFC0CB;')  # y si no un aspa en color rojo
                var.ui.txtDnicli.setText(None)
                var.ui.txtDnicli.setFocus()
        except Exception as e:
            print("error check cliente", e)

    @staticmethod
    def checkEmail(mail):
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check cliente", error)


    @staticmethod
    def altaCliente():
        nuevocli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(),var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(), var.ui.cmbMunicli.currentText()]

        if conexion.Conexion.altaCliente(nuevocli) == True:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowTitle('Aviso')
            mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
            mbox.setText("Cliente Alta en Base de DAtos")
            mbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo guardar el cliente correctamente.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
