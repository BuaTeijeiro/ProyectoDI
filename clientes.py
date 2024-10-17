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
                var.ui.txtEmailcli.setText(mail.lower())

            else:
                var.ui.txtEmailcli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailcli.setText(None)
                var.ui.txtEmailcli.setText("correo no válido")
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

        missingFields = camposObligatorios.count("")

        if missingFields ==0 and conexion.Conexion.altaCliente(nuevocli):
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowTitle('Aviso')
            mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
            mbox.setText("Cliente dado de alta en base de datos correctamente")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            mbox.exec()
            Clientes.cargaTablaClientes()
        elif missingFields > 0:
            QtWidgets.QMessageBox.critical(None, 'Error', 'ES necesario rellenar todos los campos obligatorios',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo guardar el cliente correctamente, es posible que ya se halle en la base de datos',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)

    @staticmethod
    def cargaTablaClientes():
        try:
            listado = conexion.Conexion.listadoClientes()
            #listado = conexionserver.ConexionServer.listadoClientes()
            index = 0
            for registro in listado:
                var.ui.tablaClientes.setRowCount(index + 1)
                var.ui.tablaClientes.setItem(index, 0, QtWidgets.QTableWidgetItem(registro[0]))
                var.ui.tablaClientes.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tablaClientes.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[3]))
                var.ui.tablaClientes.setItem(index, 3, QtWidgets.QTableWidgetItem("  " + registro[5] + "  "))
                var.ui.tablaClientes.setItem(index, 4, QtWidgets.QTableWidgetItem(registro[7]))
                var.ui.tablaClientes.setItem(index, 5, QtWidgets.QTableWidgetItem(registro[8]))
                var.ui.tablaClientes.setItem(index, 6, QtWidgets.QTableWidgetItem("  " + registro[9] + "  "))

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
            registro = conexion.Conexion.datosOneCliente(datos[0])
            #Clientes.cargarCliente(registro)
            listado = [var.ui.txtDnicli, var.ui.txtAltacli, var.ui.txtApelcli, var.ui.txtNomcli,var.ui.txtEmailcli, var.ui.txtMovilcli, var.ui.txtDircli, var.ui.cmbProvcli, var.ui.cmbMunicli, var.ui.txtBajacli]
            for i in range(len(listado)):
                if i in (7,8):
                    listado[i].setCurrentText(registro[i])
                else:
                    listado[i].setText(registro[i])
        except Exception as error:
            print("Error")

    @staticmethod
    def modifCliente():
        try:
            modifcli = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(), var.ui.txtNomcli.text(),var.ui.txtEmailcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text(), var.ui.cmbProvcli.currentText(), var.ui.cmbMunicli.currentText()]

            camposObligatorios = [var.ui.txtDnicli.text(), var.ui.txtAltacli.text(), var.ui.txtApelcli.text(),
                                  var.ui.txtNomcli.text(), var.ui.txtMovilcli.text(), var.ui.txtDircli.text()]

            missingFields = camposObligatorios.count("")

            if missingFields == 0 and conexion.Conexion.modifCliente(modifcli):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
                mbox.setText("Datos del cliente modificados correctamente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes()
            elif missingFields >0:
                QtWidgets.QMessageBox.critical(None, 'Error',
                                              'ES necesario rellenar todos los campos obligatorios',
                                              QtWidgets.QMessageBox.StandardButton.Cancel)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo modificar al cliente correctamente, es posible que no exista en la base de datos',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
        except Exception as error:
            print("Error")

    @staticmethod
    def bajaCliente():
        try:
            fecha = var.ui.txtBajacli.text()
            dni = var.ui.txtDnicli.text()
            if fecha != "" and conexion.Conexion.bajaCliente(dni,fecha):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Aviso')
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.svg"))
                mbox.setText("Cliente dado de baja correctamente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes()
            elif fecha == "":
                QtWidgets.QMessageBox.critical(None, 'Error',
                                               'No se pudo dar de baja al cliente correctamente: Es necesario rellenar el campo de fecha de baja',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
            else:
                QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo dar de baja al cliente correctamente: Cliente no existe o ya dado de baja',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)

        except Exception as error:
            print("Error al dar de baja a cliente")