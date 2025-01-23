from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore

import conexionserver
import eventos
import facturas
import var
import conexion

class Clientes:


    @staticmethod
    def checkDNI(dni):
        """

        :param dni: dni a verificar
        :type dni: str

        Método que llama a eventos.Eventos.validarDNI para validar el dni pasado por parámetros
        Modifica la caja de texto del dni de cliente para mostrar el resultado
        la colorea blanca si es válido, borra el contenido, la colorea rojiza y avisa si no lo es

        """
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
        """

        Método que lee el email de la caja de texto correspondiente de clientes
        y llama a eventos.Eventos.validarMail para comprobar si es válido
        Modifica la caja de texto del email de cliente para mostrar el resultado
        la colorea blanca si es válido, borra el contenido, la colorea rojiza y avisa si no lo es

        """
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
        """

        Método que lee el móvil de la caja de texto correspondiente de clientes
        y llama a eventos.Eventos.validarMovil para comprobar si es válido
        Modifica la caja de texto del movil de cliente para mostrar el resultado
        la colorea blanca si es válido, borra el contenido, la colorea rojiza y avisa si no lo es

        """
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
        """

        Método que lee los datos del cliente de la interfaz
        comprueba si se verifican las restricciones necesarias
        y llama a Conexion.altaCliente para guardar la información en la base de datos
        mostrando un mensaje con el resultado

        """
        nuevocli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text().title(), var.ui.txtNomcli.text().title(),var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text().title(), var.ui.cmbProvcli.currentText(), var.ui.cmbMunicli.currentText()]

        camposObligatorios = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text()]

        areFieldsMissing = camposObligatorios.count("") > 0
        areDatesOk = eventos.Eventos.checkFechas(var.ui.txtAltacli.text(), var.ui.txtBajacli.text())
        requirements = not areFieldsMissing and areDatesOk

        if requirements and conexion.Conexion.altaCliente(nuevocli):
        #if requirements and conexionserver.ConexionServer.altaCliente(nuevocli):
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
        """

        Método que recupera la lista de clientes mediante Conexion.listadoClientes
        y muestra dicha información en la tabla de clientes

        """
        try:
            listado = conexion.Conexion.listadoClientes()
            var.totalpaginascli = len(listado) // var.rowstablacli
            if (len(listado) % var.rowstablacli) != 0:
                var.totalpaginascli += 1
            #listado = conexionserver.ConexionServer.listadoClientes()
            index = 0
            sublistado = listado[var.currentindextablacli: var.currentindextablacli + var.rowstablacli]
            if listado[0] == sublistado[0]:
                var.ui.btnAnteriorcli.setDisabled(True)
            else:
                var.ui.btnAnteriorcli.setDisabled(False)

            if listado[-1] == sublistado[-1]:
                var.ui.btnSiguientecli.setDisabled(True)
            else:
                var.ui.btnSiguientecli.setDisabled(False)

            var.ui.tablaClientes.setRowCount(len(sublistado))
            for registro in sublistado:
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
            eventos.Eventos.setCurrentPageCli()
        except Exception as e:
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def cargaOneCliente():
        """

        Método que lee los datos del cliente seleccionado en la tabla clientes
        busca en la base de datos el resto de la información del cliente
        y la muestra en los elementos de la interfaz correspondientes

        """
        try:
            file = var.ui.tablaClientes.selectedItems()
            datos = [dato.text() for dato in file]
            registro = conexion.Conexion.datosOneCliente(datos[0])
            #registro = conexionserver.ConexionServer.datosOneCliente(datos[0])
            registro = [x if x != 'None' else '' for x in registro]
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli, var.ui.cmbMunicli, var.ui.txtBajacli]
            var.ui.lblDniclifactura.setText(registro[0])
            facturas.Facturas.cargaClienteVenta()
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
        """

        Método que lee el dni escrito en la caja de texto correspondiente de cliente
        busca la información del cliente asociado y la carga en los elementos de la interfaz correspondientes

        """
        try:
            dni = var.ui.txtDnicli.text()
            registro = conexion.Conexion.datosOneCliente(dni)
            #registro = conexionserver.ConexionServer.datosOneCliente(dni)
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
        """

        Método que lee los datos del cliente de la interfaz
        comprueba si se verifican las restricciones necesarias
        y llama a Conexion.modifCliente para modificar la información en la base de datos

        """
        try:
            modifcli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text().title(), var.ui.txtNomcli.text().title(),var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text().title(), var.ui.cmbProvcli.currentText(), var.ui.cmbMunicli.currentText(), var.ui.txtBajacli.text()]

            camposObligatorios = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                                  var.ui.txtNomcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text()]

            areFieldsMissing = camposObligatorios.count("") > 0
            areDatesOk = eventos.Eventos.checkFechas(var.ui.txtAltacli.text(), var.ui.txtBajacli.text())
            requirements = not areFieldsMissing and areDatesOk

            if requirements and conexion.Conexion.modifCliente(modifcli):
            #if requirements and conexionserver.ConexionServer.modifCliente(modifcli):
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
        """

        Método que lee el dni de la interfaz del cliente
        y llama a Conexion.bajaCliente para dar al vendedor de baja con la fecha actual

        """
        try:
            fecha = datetime.now().strftime("%d/%m/%Y")
            dni = var.ui.txtDnicli.text()
            if fecha != "" and conexion.Conexion.bajaCliente(dni,fecha):
            #if fecha != "" and conexionserver.ConexionServer.bajaCliente(dni, fecha):
                eventos.Eventos.mostrarMensajeOk("Cliente dado de baja correctamente")
                var.currentindextablacli = 0
                Clientes.cargaTablaClientes()
            elif fecha == "":
                eventos.Eventos.mostrarMensajeError('No se pudo dar de baja al cliente correctamente: Es necesario rellenar el campo de fecha de baja')
            else:
                eventos.Eventos.mostrarMensajeError('No se pudo dar de baja al cliente correctamente: Cliente no existe o ya dado de baja')

        except Exception as error:
            print("Error al dar de baja a cliente")

    @staticmethod
    def historicoCli():
        """

        Método que recarga la tabla de clientes tras clickar el checkbox de histórico
        reseteando la página de la tabla clientes a cero para evitar problemas al mostrar datos

        """
        try:
            var.currentindextablacli = 0
            Clientes.cargaTablaClientes()
        except Exception as error:
            print("Error al actualizar historico")

    @staticmethod
    def resetFilas():
        """

        Método que reajusta el número de filas que se muestra en cada página de la tabla clientes
        asegurándose siempre que esté entre un mínimo y un máximo predeterminado
        y seteando de nuevo la página de la tabla clientes a la primera
        para garantizar el mostrado correcto de los datos

        """
        try:
            if (int(var.ui.filastablacli.text()) < 1):
                var.ui.filastablacli.setValue(1)
            if (int(var.ui.filastablacli.text()) > var.maxrowstablacli):
                var.ui.filastablacli.setValue(var.maxrowstablacli)
            var.rowstablacli = int(var.ui.filastablacli.text())
            var.currentindextablacli = 0
            Clientes.cargaTablaClientes()
        except Exception as error:
            print("Error al reset filas: ", error)