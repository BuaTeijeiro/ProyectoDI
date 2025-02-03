import csv
import json
import os.path
import sys
from datetime import datetime
from PyQt6.QtWidgets import QSpinBox

import clientes
import conexion

from PyQt6 import QtWidgets, QtGui, QtCore
import re

import conexionserver
import propiedades
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
        """

        Método que muestra un mensaje de confirmación para salir de la aplicación
        Si se marca si se cierra la aplicación, si no se oculta el mensaje
        """
        mbox = QtWidgets.QMessageBox()
        if Eventos.mostrarMensajeConfimarcion(mbox, 'Salir', "Desea usted salir") == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    @staticmethod
    def cargarProv():
        """

        Método que carga la lista de provincias de la base de datos
        en los combobox de provincias de clientes, propiedades y vendedores
        """
        listado = conexion.Conexion.listaProv()
        #listado = conexionserver.ConexionServer.listaProv()
        var.provincias = listado

        var.ui.cmbProvcli.clear()
        var.ui.cmbProvcli.addItems(listado)

        var.ui.cmbProvprop.clear()
        var.ui.cmbProvprop.addItems(listado)

        var.ui.cmbProvvend.clear()
        var.ui.cmbProvvend.addItems(listado)

    @staticmethod
    def cargarMunicipioscli():
        """

        Método que carga los municipios en el combobox de municipios clientes
        solamente de la provincia seleccionada en el combobox de provincias clientes
        setea también el completer con los municipios cargados

        """
        var.ui.cmbMunicli.clear()
        provinciaCli = var.ui.cmbProvcli.currentText()
        listadoCli = conexion.Conexion.listaMunicipios(provinciaCli)
        #listadoCli = conexionserver.ConexionServer.listaMuniProv(provinciaCli)
        var.ui.cmbMunicli.addItems(listadoCli)
        var.municli = listadoCli

        completer = QtWidgets.QCompleter(var.municli, var.ui.cmbMunicli)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMunicli.setCompleter(completer)

    @staticmethod
    def cargarMunicipiosprop():
        """

        Método que carga los municipios en el combobox de municipios propiedades
        solamente de la provincia seleccionada en el combobox de provincias propiedades
        setea también el completer con los municipios cargados

        """
        var.ui.cmbMuniprop.clear()
        provinciaProp = var.ui.cmbProvprop.currentText()
        listadoProp = conexion.Conexion.listaMunicipios(provinciaProp)
        #listadoProp = conexionserver.ConexionServer.listaMuniProv(provinciaProp)
        var.ui.cmbMuniprop.addItems(listadoProp)
        var.muniprop = listadoProp


        completer = QtWidgets.QCompleter(var.muniprop, var.ui.cmbMuniprop)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbMuniprop.setCompleter(completer)

    @staticmethod
    def checkMunicipioCli():
        """

        Método que comprueba si el municipio inidcado en clientes existe, borrándolo en caso de que no

        """
        if var.ui.cmbMunicli.currentText() not in var.municli:
            var.ui.cmbMunicli.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaCli():
        """

        Método que comprueba si la provincia inidcada en clientes existe, borrándola en caso de que no

        """
        if var.ui.cmbProvcli.currentText() not in var.provincias:
            var.ui.cmbProvcli.setCurrentIndex(0)

    @staticmethod
    def checkMunicipioProp():
        """

        Método que comprueba si el municipio inidcado en propiedades existe, borrándolo en caso de que no

        """
        if var.ui.cmbMuniprop.currentText() not in var.muniprop:
            var.ui.cmbMuniprop.setCurrentIndex(0)

    @staticmethod
    def checkProvinciaProp():
        """

        Método que comprueba si la provincia inidcada en clientes existe, borrándola en caso de que no

        """
        if var.ui.cmbProvprop.currentText() not in var.provincias:
            var.ui.cmbProvprop.setCurrentIndex(0)


    @staticmethod
    def validarDNI(dni):
        """

        :param dni: dni a validar
        :type dni: str
        :return: resultado validación
        :rtype: bool

        Método que comprueba si el formato del dni es el adecuado

        """
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
        """

        :param mail: email a validar
        :type mail: str
        :return: resultado validación
        :rtype: bool

        Método que comprueba si el email sigue un formato válido

        """
        mail = mail.lower()
        regex = r'[a-zA-Z0-9]+([\._][a-zA-Z0-9]+)*[@]\w+[.]\w+'
        if re.fullmatch(regex, mail) or mail == "":
            return True
        else:
            return False

    @staticmethod
    def validarMovil(movil):
        """

        :param movil: móvil a validar
        :type movil: str
        :return: resultado validacion
        :rtype: bool

        Método que comprueba si el móvil sigue un formato válido para España

        """
        regex = r"[67]\d{8}"
        return re.fullmatch(regex, movil)

    @staticmethod
    def convertStringToDate(date):
        """

        :param date: fecha
        :type date: str
        :return: fecha convertida/false
        :rtype: datetime/bool

        Método que transforma una fecha de str a tipo datetime, devolviendo falso si el formato no es válido

        """
        try:
            date = date.split('/')
            day = date[0]
            month = date[1]
            year = date[2]
            date = datetime(year=int(year), month=int(month), day=int(day))
            return date
        except Exception as error:
            return False

    @staticmethod
    def checkFechas(date1, date2):
        """

        :param date1:
        :type date1:
        :param date2:
        :type date2:
        :return:
        :rtype:
        """
        date1 = Eventos.convertStringToDate(date1)
        if date1 and date2 == "":
            return True
        date2 = Eventos.convertStringToDate(date2)
        if date1 and date2:
            return date2 >= date1
        else:
            return False

    @staticmethod
    def abrirCalendar(btn):
        """

        :param btn:
        :type btn:
        """
        try:
            var.btn = btn
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    @staticmethod
    def abrirTipoprop():
        """

        """
        try:
            var.dlggestion.show()
        except Exception as error:
            print("error en abrir tipos de propiedades ", error)

    @staticmethod
    def abrirSelectMuni():
        """

        """
        try:
            var.dlgselectmuni.show()
        except Exception as error:
            print("error en abrir selección de municipios", error)

    @staticmethod
    def abrirAbout():
        """

        """
        try:
            var.dlgabout.show()
        except Exception as error:
            print("error en abrir About ", error)

    @staticmethod
    def cargaFecha(qDate):
        """

        :param qDate:
        :type qDate:
        :return:
        :rtype:
        """
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
            if var.ui.panPrincipal.currentIndex() == 2 and var.btn == 0:
                var.ui.txtAltavend.setText(str(data))
            if var.ui.panPrincipal.currentIndex() == 2 and var.btn == 1:
                var.ui.txtBajavend.setText(str(data))
            if var.ui.panPrincipal.currentIndex() == 3 and var.btn == 0:
                var.ui.txtFechaFactura.setText(str(data))
            if var.ui.panPrincipal.currentIndex() == 4 and var.btn == 0:
                var.ui.txtFechaInicioAlquiler.setText(str(data))
            if var.ui.panPrincipal.currentIndex() == 4 and var.btn == 1:
                var.ui.txtFechaFinAlquiler.setText(str(data))
            time.sleep(0.2)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    @staticmethod
    def avanzarTablacli():
        """

        """
        var.currentindextablacli += var.rowstablacli
        clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def retrocederTablacli():
        """

        """
        var.currentindextablacli -= var.rowstablacli
        clientes.Clientes.cargaTablaClientes()

    @staticmethod
    def setCurrentPageCli():
        """

        """
        currentPage = var.currentindextablacli / var.rowstablacli + 1
        totalpaginascli = var.totalpaginascli
        var.ui.lbl_pagcli.setText(f"Página %i/%i" %(currentPage, totalpaginascli))

    @staticmethod
    def avanzarTablaprop():
        """

        """
        var.currentindextablaprop += var.rowstablaprop
        propiedades.Propiedades.setTablaPropiedades()

    @staticmethod
    def retrocederTablaprop():
        """

        """
        var.currentindextablaprop -= var.rowstablaprop
        propiedades.Propiedades.setTablaPropiedades()

    @staticmethod
    def setCurrentPageProp():
        """

        """
        currentPage = var.currentindextablaprop / var.rowstablaprop + 1
        totalpaginasprop = len (var.currentlistapropiedades) // var.rowstablaprop
        if len(var.currentlistapropiedades) % var.rowstablaprop != 0:
            totalpaginasprop += 1
        var.ui.lbl_pagprop.setText(f"Página %i/%i" % (currentPage, totalpaginasprop))

    @staticmethod
    def resizeTablaClientes():
        """

        """
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
    def resizeTablaFacturas():
        """

        """
        try:
            header = var.ui.tablaFacturas.horizontalHeader()
            for i in range(header.count()):
                if i not in (0,3):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaFacturas.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    @staticmethod
    def resizeTablaAlquileres():
        """

        """
        try:
            header = var.ui.tablaAlquileres.horizontalHeader()
            for i in range(header.count()):
                if i not in (0, 3):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaAlquileres.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    @staticmethod
    def resizeTablaVentas():
        """

        """
        try:
            header = var.ui.tablaVentas.horizontalHeader()
            for i in range(header.count()):
                if i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaVentas.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    @staticmethod
    def resizeTablaVendedores():
        """

        """
        try:
            header = var.ui.tablaVendedores.horizontalHeader()
            for i in range(header.count()):
                if i in (1, 3):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)

                header_item = var.ui.tablaVendedores.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)
        except Exception as e:
            print("error en resize tabla clientes: ", e)

    @staticmethod
    def resizeTablaPropiedades():
        """

        """
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
        """

        """
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
        """

        """
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
                Eventos.cargarProv()
                Eventos.cargarMunicipioscli()
                clientes.Clientes.cargaTablaClientes()
        except Exception as error:
            print("error en restaurar backup: ", error)

    @staticmethod
    def limpiarPanel():
        """

        """
        objetosPanel = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli,
                    var.ui.txtNomcli, var.ui.txtEmailcli, var.ui.txtMovilcli,
                    var.ui.txtDircli, var.ui.txtBajacli, var.ui.lblProp, var.ui.txtFechaprop,
                    var.ui.txtFechabajaprop, var.ui.txtCPprop, var.ui.txtDirprop, var.ui.spinHabprop,
                    var.ui.spinBanosprop, var.ui.txtSuperprop, var.ui.txtPrecioalquilerprop,
                    var.ui.txtPrecioventaprop, var.ui.txtComentarioprop, var.ui.txtNomeprop,
                    var.ui.txtMovilprop, var.ui.lblidvend, var.ui.txtDnivend, var.ui.txtNombrevend,
                    var.ui.txtAltavend, var.ui.txtBajavend, var.ui.txtMovilvend,
                    var.ui.txtEmailvend]

        var.ui.chkAlquilprop.setChecked(False)
        var.ui.chkVentaprop.setChecked(False)
        var.ui.chkInterprop.setChecked(False)
        var.ui.rbtDisponprop.setChecked(True)

        for i, element in enumerate(objetosPanel):
            if isinstance(element, QSpinBox):
                element.setValue(0)
            else:
                element.setText("")

        var.ui.txtDnivend.setPlaceholderText('')
        var.ui.txtMovilvend.setPlaceholderText('')
        var.ui.txtEmailvend.setPlaceholderText('')

        Eventos.cargarProv()
        Eventos.cargarMunicipioscli()
        Eventos.cargarTiposprop()

        var.ui.btnGrabarvend.setEnabled(True)
        var.ui.txtDnivend.setEnabled(True)

        clientes.Clientes.cargaTablaClientes()
        propiedades.Propiedades.cargaTablaPropiedades()

    @staticmethod
    def exportarCSVProp():
        """

        """
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            file = str(fecha) + "_datosPropiedades.csv"
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos Propiedades", file, ".csv")
            if var.dlgabrir.accept and fichero:
                registros = conexion.Conexion.listadoPropiedadesAllData()
                with open(fichero, "w", newline="",encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo","Alta","Baja","Código Postal", "Dirección", "Provincia", "Municipio", "Tipo propiedad", "Num Habitaciones", "Num Baños", "Superficie", "Precio Alquiler", "Precio Venta", "Observaciones", "Tipo operación", "Estado", "Nombre propietario", "Móvil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero, directorio)
            else:
                Eventos.mostrarMensajeError("Error de exportación de Datos de Propiedades a CSV")
        except Exception as error:
            print("error en exportar csv: ", error)

    @staticmethod
    def exportarJsonProp():
        """

        """
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            file = str(fecha) + "_datosPropiedades.json"
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos Propiedades", file, ".json")
            if var.dlgabrir.accept and fichero:
                keys = ["Codigo","Alta","Baja","Código Postal", "Dirección", "Provincia", "Municipio", "Tipo propiedad", "Num Habitaciones", "Num Baños", "Superficie", "Precio Alquiler", "Precio Venta", "Observaciones", "Tipo operación", "Estado", "Nombre propietario", "Móvil"]
                registros = conexion.Conexion.listadoPropiedadesAllData()
                listado = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, "w", newline="", encoding="utf-8") as jsonfile:
                    json.dump(listado, jsonfile, indent=4, ensure_ascii=False)
                shutil.move(fichero, directorio)
            else:
                Eventos.mostrarMensajeError("Error de exportación de Datos de Propiedades a JSON")
        except Exception as error:
            print("error en exportar csv: ", error)

    @staticmethod
    def exportarJsonVend():
        """

        """
        try:
            fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            file = str(fecha) + "_datosVendedores.json"
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Exportar Datos Vendedores", file, ".json")
            if var.dlgabrir.accept and fichero:
                keys = ["idVendedor","dniVendedor", "nombreVendedor", "altaVendedor", "bajaVendedor", "movilVendedor", "mailVendedor","delegacionVendedor"]
                registros = conexion.Conexion.listadoVendedores()
                listado = [dict(zip(keys, registro)) for registro in registros]
                with open(fichero, "w", newline="", encoding="utf-8") as jsonfile:
                    json.dump(listado, jsonfile, indent=4, ensure_ascii=False)
                shutil.move(fichero, directorio)
            else:
                Eventos.mostrarMensajeError("Error de exportación de Datos de Vendedores a JSON")
        except Exception as error:
            print("error en exportar json: ", error)


    @staticmethod
    def cargarTiposprop():
        """

        """
        tipos = conexion.Conexion.listadoTipoprop()
        #tipos = conexionserver.ConexionServer.listadoTipoprop()
        var.ui.cmbTipoprop.clear()
        var.ui.cmbTipoprop.addItems(tipos)

    @staticmethod
    def mostrarMensajeOk(mensaje):
        """

        :param mensaje:
        :type mensaje:
        """
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
        """

        :param mensaje:
        :type mensaje:
        """
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
        mbox.setWindowTitle('Error')
        mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        mbox.exec()

    @staticmethod
    def mostrarMensajeWarning(mensaje):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        mbox.setModal(True)
        mbox.setWindowTitle('Precaución')
        mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
        return mbox.exec()

    @staticmethod
    def mostrarMensajeConfimarcion(mbox, titulo, mensaje):
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setModal(True)
        mbox.setWindowTitle(titulo)
        mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
        mbox.setText(mensaje)
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')
        return mbox.exec()

