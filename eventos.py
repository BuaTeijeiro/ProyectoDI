import sys

import conexion

from PyQt6 import QtWidgets, QtGui

import var


class Eventos():
    @staticmethod
    def mensajeSalir():
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowTitle('Salir')
        mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
        mbox.setText("Desea usted salir")
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def cargarProv():
        var.ui.cmbProvcli.clear()
        listado = conexion.Conexion.listaProv()
        var.ui.cmbProvcli.addItems(listado)

    @staticmethod
    def cargarMunicipios():
        var.ui.cmbMunicli.clear()
        provincia = var.ui.cmbProvcli.currentText()
        listado = conexion.Conexion.listaMunicipios(provincia)
        var.ui.cmbMunicli.addItems(listado)

    @staticmethod
    def reloadMunicipios():
        var.ui.cmbMunicli.clear()

    @staticmethod
    def validarDNI(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if dni.isdigit() and tabla[int(dni) % 23] == dig_control:
                    return True
                else:
                    return False
            else:
                return False

        except Exception as error:
            print("error en validar dni ", error)