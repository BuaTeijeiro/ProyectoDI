import os.path
import sys
from datetime import datetime

from PyQt6.QtWidgets import QSpinBox

import clientes
import conexion

from PyQt6 import QtWidgets, QtGui
import re

import conexionserver
import eventos
import var
import time
import zipfile
import shutil
import locale


#Establecer configuracion regional

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
locale.setlocale(locale.LC_MONETARY, "es_ES.UTF-8")


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
        #listado = conexionserver.ConexionServer.listaProv()
        var.ui.cmbProvcli.addItems(listado)

        var.ui.cmbProvprop.clear()
        var.ui.cmbProvprop.addItems(listado)

    @staticmethod
    def cargarMunicipioscli():
        var.ui.cmbMunicli.clear()
        provinciaCli = var.ui.cmbProvcli.currentText()
        listadoCli = conexion.Conexion.listaMunicipios(provinciaCli)
        #listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMunicli.addItems(listadoCli)

    @staticmethod
    def cargarMunicipiosprop():
        var.ui.cmbMuniprop.clear()
        provinciaProp = var.ui.cmbProvprop.currentText()
        listadoProp = conexion.Conexion.listaMunicipios(provinciaProp)
        # listado = conexionserver.ConexionServer.listaMuniProv(provincia)
        var.ui.cmbMuniprop.addItems(listadoProp)


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

    @staticmethod
    def validarMail(mail):
        mail = mail.lower()
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        if re.match(regex, mail) or mail == "":
            return True
        else:
            return False

    @staticmethod
    def validarMovil(movil):
        regex = r"[67]\d{8}"
        return re.fullmatch(regex, movil)

    @staticmethod
    def abrirCalendar(btn):
        try:
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    @staticmethod
    def abrirTipoprop():
        try:
            var.dlggestion.show()
        except Exception as error:
            print("error en abrir tipos de propiedades ", error)

    @staticmethod
    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.ui.panPrincipal.currentIndex() == 0 and var.btn == 0:
                var.ui.txtAltacli.setText(str(data))
            if var.ui.panPrincipal.currentIndex() == 0 and var.btn == 1:
                var.ui.txtBajacli.setText(str(data))
            if var.ui.panPrincipal.currentIndex() == 1 and var.btn == 0:
                var.ui.txtFechaprop.setText(str(data))
            if var.ui.panPrincipal.currentIndex() == 1 and var.btn == 1:
                var.ui.txtFechabajaprop.setText(str(data))
            time.sleep(0.2)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    @staticmethod
    def resizeTablaClientes():
        try:
            header = var.ui.tablaClientes.horizontalHeader()
            for i in range(header.count()):
                if i not in (0, 3, 6):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaClientes.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    @staticmethod
    def resizeTablaPropiedades():
        try:
            header = var.ui.tablaPropiedades.horizontalHeader()
            for i in range(header.count()):
                if i in (1, 2):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaPropiedades.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    @staticmethod
    def crearBackup():
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            copia = str(fecha) + "_backup.zip"
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, ".zip")
            if var.dlgabrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, "w")
                fichzip.write("bbdd.sqlite", os.path.basename("bbdd.sqlite"),zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Copia de Seguridad')
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
                mbox.setText("Copia de Seguridad creada correctamente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as error:
            print("error en crear backup: ", error)

    @staticmethod
    def restaurarBackup():
        try:
            filename = var.dlgabrir.getOpenFileName(None, "Restaurar Copia de Seguridad ", "", "*.zip;;All Files(*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, "r") as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Copia de Seguridad')
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
                mbox.setText("Copia de Seguridad Restaurada Correctamente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                conexion.Conexion.db_conexion()
                eventos.Eventos.cargarProv()
                eventos.Eventos.cargarMunicipioscli()
                clientes.Clientes.cargaTablaClientes()
        except Exception as error:
            print("error en restaurar backup: ", error)

    @staticmethod
    def limpiarPanel():
        objetosPanel = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli,
                    var.ui.txtNomcli, var.ui.txtEmailcli, var.ui.txtMovilcli,
                    var.ui.txtDircli, var.ui.txtBajacli, var.ui.lblProp, var.ui.txtFechaprop,
                    var.ui.txtFechabajaprop, var.ui.txtCPprop, var.ui.txtDirprop, var.ui.spinHabprop,
                    var.ui.spinBanosprop, var.ui.txtSuperprop, var.ui.txtPrecioalquilerprop,
                    var.ui.txtPrecioventaprop, var.ui.txtComentarioprop, var.ui.txtNomeprop,
                    var.ui.txtMovilprop]

        var.ui.chkAlquilprop.setChecked(False)
        var.ui.chkVentaprop.setChecked(False)
        var.ui.chkInterprop.setChecked(False)
        var.ui.rbtDisponprop.setChecked(True)


        for i, element in enumerate(objetosPanel):
            if isinstance(element, QSpinBox):
                element.setValue(0)
            else:
                element.setText("")

        eventos.Eventos.cargarProv()
        eventos.Eventos.cargarMunicipioscli()
        eventos.Eventos.cargarTiposprop()

    @staticmethod
    def cargarTiposprop():
        tipos = conexion.Conexion.listadoTipoprop()
        var.ui.cmbTipoprop.clear()
        var.ui.cmbTipoprop.addItems(tipos)

    @staticmethod
    def mostrarMensajeOk(mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
        mbox.setWindowTitle('Aviso')
        mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    @staticmethod
    def mostrarMensajeError(mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowTitle('Error')
        mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()