from datetime import datetime

import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtCore


class Vendedores:
    @staticmethod
    def checkDNI(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDnivend.setText(str(dni))
            check = eventos.Eventos.validarDNI(dni)
            if check:
                var.ui.txtDnivend.setStyleSheet('background-color: rgb(255, 255, 255)')
            else:
                var.ui.txtDnivend.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDnivend.setText(None)
                var.ui.txtDnivend.setPlaceholderText('DNI no válido')
                var.ui.txtDnivend.setFocus()
        except Exception as e:
            print("error check cliente", e)

    @staticmethod
    def checkEmail():
        try:
            mail = str(var.ui.txtEmailvend.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailvend.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailvend.setPlaceholderText("")
                var.ui.txtEmailvend.setText(mail.lower())

            else:
                var.ui.txtEmailvend.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailvend.setText(None)
                var.ui.txtEmailvend.setPlaceholderText("correo no válido")
                var.ui.txtEmailvend.setFocus()

        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def checkMovil():
        try:
            movil = str(var.ui.txtMovilvend.text())
            if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilvend.setStyleSheet('background-color: rgb(255, 255, 255);')

            else:
                var.ui.txtMovilvend.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilvend.setText(None)
                var.ui.txtMovilvend.setPlaceholderText("móvil no válido")
                var.ui.txtMovilvend.setFocus()

        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def altaVendedor():
        nuevovend = [var.ui.txtDnivend.text(), var.ui.txtNombrevend.text().title(),
                    var.ui.txtAltavend.text(), var.ui.txtMovilvend.text(),
                    var.ui.txtEmailvend.text(), var.ui.cmbProvvend.currentText()]

        camposObligatorios = [var.ui.txtDnivend.text(), var.ui.txtNombrevend.text(), var.ui.txtMovilvend.text()]

        areFieldsMissing = camposObligatorios.count("") > 0
        #areDatesOk = eventos.Eventos.checkFechas(var.ui.txtAltacli.text(), var.ui.txtBajacli.text())
        requirements = not areFieldsMissing #and areDatesOk

        if requirements and conexion.Conexion.altaVendedor(nuevovend):
            # if requirements and conexionserver.ConexionServer.altaCliente(nuevocli):
            eventos.Eventos.mostrarMensajeOk("Vendedor dado de alta en base de datos correctamente")
            Vendedores.buscarVendedor()
            Vendedores.cargaTablaVendedores()
        elif areFieldsMissing:
            eventos.Eventos.mostrarMensajeError(
                'Es necesario rellenar todos los campos obligatorios, marcados con (*)')
        else:
            eventos.Eventos.mostrarMensajeError(
                'No se pudo guardar el vendedor correctamente, es posible que el dni ya exista en la base de datos')

    @staticmethod
    def cargaTablaVendedores():
        try:
            listado = conexion.Conexion.listadoVendedores()
            var.ui.tablaVendedores.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaVendedores.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaVendedores.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tablaVendedores.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[5]))
                var.ui.tablaVendedores.setItem(index, 3, QtWidgets.QTableWidgetItem(registro[7]))

                var.ui.tablaVendedores.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVendedores.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaVendedores.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaVendedores.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                index += 1
            eventos.Eventos.resizeTablaVendedores()
        except Exception as e:
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def cargaOneVendedor(registro):
        try:
            registro = [x if x != 'None' else '' for x in registro]
            listado = [var.ui.lblidvend, var.ui.txtDnivend, var.ui.txtNombrevend,
                    var.ui.txtAltavend, var.ui.txtBajavend, var.ui.txtMovilvend,
                    var.ui.txtEmailvend, var.ui.cmbProvvend]
            for i in range(len(listado)):
                if i == 7:
                    listado[i].setCurrentText(str(registro[i]))
                else:
                    listado[i].setText(str(registro[i]))
            var.ui.btnGrabarvend.setEnabled(False)
            var.ui.txtDnivend.setEnabled(False)
        except Exception as error:
            print("Error", error)

    @staticmethod
    def buscarVendedor():
        movil = var.ui.txtMovilvend.text()
        id = conexion.Conexion.getIdVendedor(movil)
        if id:
            registro = conexion.Conexion.datosOneVendedor(id)
            Vendedores.cargaOneVendedor(registro)
        else:
            eventos.Eventos.mostrarMensajeError("No existe ningún vendedor con ese móvil")

    @staticmethod
    def cargaCurrentVendedor():
        try:
            file = var.ui.tablaVendedores.selectedItems()
            datos = [dato.text() for dato in file]
            registro = conexion.Conexion.datosOneVendedor(datos[0])
            Vendedores.cargaOneVendedor(registro)
        except Exception as error:
            print("Error", error)

    @staticmethod
    def modifVendedor():
        try:
            modifvend = [var.ui.txtNombrevend.text().title(),
                    var.ui.txtAltavend.text(), var.ui.txtBajavend.text(), var.ui.txtMovilvend.text(),
                    var.ui.txtEmailvend.text(), var.ui.cmbProvvend.currentText(), var.ui.lblidvend.text()]

            camposObligatorios = [var.ui.txtNombrevend.text(), var.ui.txtMovilvend.text()]

            areFieldsMissing = camposObligatorios.count("") > 0
            requirements = not areFieldsMissing

            if requirements and conexion.Conexion.modifVendedor(modifvend):
                # if requirements and conexionserver.ConexionServer.modifCliente(modifcli):
                eventos.Eventos.mostrarMensajeOk("Datos del vendedor modificados correctamente")
                Vendedores.cargaTablaVendedores()
            elif areFieldsMissing:
                eventos.Eventos.mostrarMensajeError(
                    'Es necesario rellenar todos los campos obligatorios, marcados con (*)')
            else:
                eventos.Eventos.mostrarMensajeError(
                    'No se pudo modificar al vendedor correctamente')
        except Exception as error:
            print("Error", error)

    @staticmethod
    def bajaVendedor():
        try:
            id = var.ui.lblidvend.text()
            fecha = datetime.now().strftime("%d/%m/%Y")

            areFieldsMissing = fecha == ""
            requirements = not areFieldsMissing

            if requirements and conexion.Conexion.bajaVendedor(id, fecha):
                # if requirements and conexionserver.ConexionServer.modifCliente(modifcli):
                eventos.Eventos.mostrarMensajeOk("Vendedor dado de baja correctamente")
                Vendedores.cargaTablaVendedores()
            elif areFieldsMissing:
                eventos.Eventos.mostrarMensajeError(
                    'Es necesario indicar la fecha de baja para dar de baja')
            else:
                eventos.Eventos.mostrarMensajeError(
                    'No se pudo dar de baja al vendedor correctamente')
            Vendedores.buscarVendedor()
        except Exception as error:
            print("Error", error)