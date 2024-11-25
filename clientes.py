from datetime import datetime
from importlib.metadata import requires

from PyQt6 import QtWidgets, QtGui, QtCore

import conexionserver
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
    def checkEmail():
        try:
            mail = str(var.ui.txtEmailcli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailcli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailcli.setPlaceholderText("")
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setPlaceholderText("correo no válido")
                var.ui.txtEmailcli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def checkMovil():
        try:
            movil = str(var.ui.txtMovilcli.text())
            if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilcli.setStyleSheet('background-color: rgb(255, 255, 255);')

            else:
                var.ui.txtMovilcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilcli.setText(None)
                var.ui.txtMovilcli.setFocus()

        except Exception as error:
            print("error check cliente", error)


    @staticmethod
    def altaCliente():
        nuevocli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(),var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(), var.ui.cmbMunicli.currentText()]

        camposObligatorios = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text()]

        areFieldsMissing = camposObligatorios.count("") > 0
        areDatesOk = eventos.Eventos.checkFechas(var.ui.txtAltacli.text(), var.ui.txtBajacli.text())
        requirements = not areFieldsMissing and areDatesOk

        #if requirements and conexion.Conexion.altaCliente(nuevocli):
        if requirements and conexionserver.ConexionServer.altaCliente(nuevocli):
            eventos.Eventos.mostrarMensajeOk("Cliente dado de alta en base de datos correctamente")
            Clientes.cargaTablaClientes()
        elif areFieldsMissing:
            eventos.Eventos.mostrarMensajeError('Es necesario rellenar todos los campos obligatorios, marcados con (*)')
        elif not areDatesOk:
            eventos.Eventos.mostrarMensajeError("El formato de la fecha debe ser dd/mm/aaaa")
        else:
            eventos.Eventos.mostrarMensajeError('No se pudo guardar el cliente correctamente, es posible que ya se halle en la base de datos')

    @staticmethod
    def cargaTablaClientes():
        try:
            #listado = conexion.Conexion.listadoClientes()
            listado = conexionserver.ConexionServer.listadoClientes()
            index = 0
            var.ui.tablaClientes.setRowCount(len(listado))
            for registro in listado:
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(registro[0]))
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[3]))
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem("  " + registro[5] + "  "))
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[7]))
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[8]))
                var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem(registro[9]))

                var.ui.tablaClientes.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaClientes.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaClientes.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                index += 1
            eventos.Eventos.resizeTablaClientes()
        except Exception as e:
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def cargaOneCliente():
        try:
            file = var.ui.tablaClientes.selectedItems()
            datos = [dato.text() for dato in file]
            #registro = conexion.Conexion.datosOneCliente(datos[0])
            registro = conexionserver.ConexionServer.datosOneCliente(datos[0])
            registro = [x if x != 'None' else '' for x in registro]
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli, var.ui.cmbMunicli, var.ui.txtBajacli]
            for i in range(len(listado)):
                if i in (7,8):
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
            Clientes.checkDNI(var.ui.txtDnicli.text())
        except Exception as error:
            print("Error")

    @staticmethod
    def cargaClienteBuscado():
        try:
            dni = var.ui.txtDnicli.text()
            #registro = conexion.Conexion.datosOneCliente(dni)
            registro = conexionserver.ConexionServer.datosOneCliente(dni)
            registro = [x if x != 'None' else '' for x in registro]
            if registro:
                listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,
                           var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli,
                           var.ui.cmbMunicli, var.ui.txtBajacli]
                for i in range(len(listado)):
                    if i in (7, 8):
                        listado[i].setCurrentText(registro[i])
                    else:
                        listado[i].setText(registro[i])
            else:
                eventos.Eventos.mostrarMensajeError(f"No existe el cliente con dni = %s en la base de datos" %(dni))
        except Exception as error:
            print("Error: ", error)

    @staticmethod
    def modifCliente():
        try:
            modifcli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(),var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(), var.ui.cmbMunicli.currentText(), var.ui.txtBajacli.text()]

            camposObligatorios = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                                  var.ui.txtNomcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text()]

            areFieldsMissing = camposObligatorios.count("") > 0
            areDatesOk = eventos.Eventos.checkFechas(var.ui.txtAltacli.text(), var.ui.txtBajacli.text())
            requirements = not areFieldsMissing and areDatesOk

            print(modifcli)
            #if requirements and conexion.Conexion.modifCliente(modifcli):
            if requirements and conexionserver.ConexionServer.modifCliente(modifcli):
                eventos.Eventos.mostrarMensajeOk("Datos del cliente modificados correctamente")
                Clientes.cargaTablaClientes()
            elif areFieldsMissing:
                eventos.Eventos.mostrarMensajeError('Es necesario rellenar todos los campos obligatorios, marcados con (*)')
            elif not areDatesOk:
                eventos.Eventos.mostrarMensajeError("Hay algún problema con las fechas, compruebe lo siguiente:\n -Las fechas deben de tener el formato dd/mm/aaaa o estar el campo vacío\n -La fecha de baja no puede ser anterior a la de alta")
                var.ui.txtBajacli.setText("")
            else:
                eventos.Eventos.mostrarMensajeError('No se pudo modificar al cliente correctamente, es posible que no exista en la base de datos')
        except Exception as error:
            print("Error", error)

    @staticmethod
    def bajaCliente():
        try:
            fecha = datetime.now().strftime("%d/%m/%Y")
            dni = var.ui.txtDnicli.text()
            #if fecha != "" and conexion.Conexion.bajaCliente(dni,fecha):
            if fecha != "" and conexionserver.ConexionServer.bajaCliente(dni, fecha):
                eventos.Eventos.mostrarMensajeOk("Cliente dado de baja correctamente")
                Clientes.cargaTablaClientes()
            elif fecha == "":
                eventos.Eventos.mostrarMensajeError('No se pudo dar de baja al cliente correctamente: Es necesario rellenar el campo de fecha de baja')
            else:
                eventos.Eventos.mostrarMensajeError('No se pudo dar de baja al cliente correctamente: Cliente no existe o ya dado de baja')

        except Exception as error:
            print("Error al dar de baja a cliente")

    @staticmethod
    def historicoCli():
        try:
            Clientes.cargaTablaClientes()
        except Exception as error:
            print("Error al actualizar historico")