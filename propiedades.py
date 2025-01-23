from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import conexionserver
import facturas
import var
import eventos


class Propiedades():
    @staticmethod
    def checkMovil():
        """

        Método que lee el móvil de la caja de texto correspondiente de propietario de propiedad
        y llama a eventos.Eventos.validarMovil para comprobar si es válido
        Modifica la caja de texto del movil del propietario de propiedad para mostrar el resultado
        la colorea blanca si es válido, borra el contenido, la colorea rojiza y avisa si no lo es

        """
        try:
            movil = str(var.ui.txtMovilprop.text())
            if eventos.Eventos.validarMovil(movil):
                var.ui.txtMovilprop.setStyleSheet('background-color: rgb(255, 255, 255);')

            else:
                var.ui.txtMovilprop.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilprop.setText(None)
                var.ui.txtMovilprop.setFocus()

        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def reloadDisponibility():
        """

        Método que habilita o desabilita los botones de radio de disponibilidad
        según haya fecha de baja en la caja de texto (no puede estar disponible)
        o no (debe estar disponible)

        """
        if var.ui.txtFechabajaprop.text() == "":
            var.ui.rbtDisponprop.setEnabled(True)
            var.ui.rbtAlquilprop.setEnabled(False)
            var.ui.rbtVentaprop.setEnabled(False)
            var.ui.rbtDisponprop.setChecked(True)
        else:
            var.ui.rbtAlquilprop.setChecked(True)
            var.ui.rbtDisponprop.setEnabled(False)
            var.ui.rbtAlquilprop.setEnabled(True)
            var.ui.rbtVentaprop.setEnabled(True)

    @staticmethod
    def reloadTipoOperacion():
        """

        Método que checkea automáticamente los tipos de operación si hay un precio para dicho tipo

        """
        var.ui.chkAlquilprop.setChecked(var.ui.txtPrecioalquilerprop.text()!="")
        var.ui.chkVentaprop.setChecked(var.ui.txtPrecioventaprop.text() != "")

    @staticmethod
    def reloadPrecio():
        """

        Método que borra los precios para un tipo de operación si se desmarca la opción de dicho tipo de operación

        """
        if not var.ui.chkAlquilprop.isChecked():
            var.ui.txtPrecioalquilerprop.setText("")
        if not var.ui.chkVentaprop.isChecked():
            var.ui.txtPrecioventaprop.setText("")

    @staticmethod
    def altaTipoPropiedad():
        """

        Método que lee el nombre del tipo de propiedad de la interfaz
        y llama a Conexion.anadirTipoprop para guardar la información en la base de datos
        mostrando un mensaje con el resultado de la operación

        """
        try:
            tipo = var.dlggestion.interface.txtGestipoprop.text().title()
            var.dlggestion.interface.txtGestipoprop.setText("")
            if conexion.Conexion.anadirTipoprop(tipo):
                eventos.Eventos.mostrarMensajeOk("Tipo de propiedad registrado correctamente")
                eventos.Eventos.cargarTiposprop()
            else:
                eventos.Eventos.mostrarMensajeError("No se pudo registrar el tipo de propiedad, ya existe")
        except Exception as error:
            print(error)

    @staticmethod
    def deleteTipoPropiedad():
        """

        Método que lee el nombre del tipo de propiedad de la interfaz
        y llama a Conexion.eliminarTipoprop para eliminar la información de la base de datos
        mostrando un mensaje con el resultado de la operación

        """
        try:
            tipo = var.dlggestion.interface.txtGestipoprop.text().title()
            var.dlggestion.interface.txtGestipoprop.setText("")
            if conexion.Conexion.eliminarTipoprop(tipo):
                eventos.Eventos.mostrarMensajeOk("Tipo de propiedad eliminada correctamente")
                eventos.Eventos.cargarTiposprop()
            else:
                eventos.Eventos.mostrarMensajeError("No se pudo eliminar el tipo de propiedad, no existe")
        except Exception as error:
            print("error al eliminar el tipo de propiedad")

    @staticmethod
    def altaPropiedad():
        """

        Método que lee los datos de la propiedad de la interfaz
        comprueba si se verifican las restricciones necesarias
        y llama a Conexion.altaPropiedad para guardar la información en la base de datos
        mostrando un mensaje con el resultado de la operación

        """
        try:
            camposObligatorios = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text(), var.ui.txtSuperprop.text(),  var.ui.txtNomeprop.text(),var.ui.txtMovilprop.text()]

            areFieldsMissing = camposObligatorios.count("") > 0

            isAlquilerOk = (var.ui.txtPrecioalquilerprop.text() and var.ui.chkAlquilprop.isChecked()) or (
                        not var.ui.txtPrecioalquilerprop.text() and not var.ui.chkAlquilprop.isChecked())
            isVentaOk = (var.ui.txtPrecioventaprop.text() and var.ui.chkVentaprop.isChecked()) or (
                        not var.ui.txtPrecioventaprop.text() and not var.ui.chkVentaprop.isChecked())
            isAltaOk = not var.ui.txtFechabajaprop.text() and var.ui.rbtDisponprop.isChecked()
            areDatesOk = eventos.Eventos.checkFechas(var.ui.txtFechaprop.text(), var.ui.txtFechabajaprop.text())
            areRequirementsOK = not areFieldsMissing and isAlquilerOk and isVentaOk and isAltaOk and areDatesOk

            propiedad = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text().title(),var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(), var.ui.cmbTipoprop.currentText(), var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(), var.ui.txtPrecioalquilerprop.text(), var.ui.txtPrecioventaprop.text(), var.ui.txtComentarioprop.toPlainText(), var.ui.txtNomeprop.text().title(),var.ui.txtMovilprop.text()]
            tipooper = []
            if var.ui.chkAlquilprop.isChecked():
                tipooper.append(var.ui.chkAlquilprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipooper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipooper.append(var.ui.chkInterprop.text())
            propiedad.append(",".join(tipooper))
            if var.ui.rbtDisponprop.isChecked():
                propiedad.append(var.ui.rbtDisponprop.text())
            elif var.ui.rbtAlquilprop.isChecked():
                propiedad.append(var.ui.rbtAlquilprop.text())
            else:
                propiedad.append(var.ui.rbtVentaprop.text())


            if areRequirementsOK and conexion.Conexion.altaPropiedad(propiedad):
            #if areRequirementsOK and conexionserver.ConexionServer.altaPropiedad(propiedad):
                eventos.Eventos.mostrarMensajeOk("Se ha guardado la propiedad correctamente")
                Propiedades.cargaOnePropiedad(var.lastid)
                Propiedades.cargaTablaPropiedades()
            elif not isAltaOk:
                eventos.Eventos.mostrarMensajeError("Al dar de alta una propiedad debe estar disponible y sin fecha de baja")
            elif not isAlquilerOk:
                eventos.Eventos.mostrarMensajeError("Si es alquilable debe tener precio de Alquiler y vicerversa")
            elif not isVentaOk:
                eventos.Eventos.mostrarMensajeError("Si se puede vender debe tener precio de venta y vicerversa")
            elif areFieldsMissing:
                eventos.Eventos.mostrarMensajeError("Es necesario rellenar todos los campos obligatorios")
            elif not areDatesOk:
                eventos.Eventos.mostrarMensajeError(
                    "Las fecha de alta deben de tener el formato dd/mm/aaaa")
                var.ui.txtFechabajaprop.setText("")
            else:
                eventos.Eventos.mostrarMensajeError("Error al guardar la propiedad")
        except Exception as error:
            print("Error al dar de alta la propiedad")


    @staticmethod
    def cargaTablaPropiedades():
        """

        Método que recupera la lista de propiedades mediante Conexion.listadoPropiedades
        y llama a Propiedades.setTablaPropiedades() para cargarlos en la tabla de propiedades

        """
        try:
            listado = conexion.Conexion.listadoPropiedades()
            #listado = conexionserver.ConexionServer.listadoPropiedades()
            var.currentlistapropiedades = listado
            Propiedades.setTablaPropiedades()

        except Exception as e:
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def filtrarTablaPropiedades():
        """

        Método que lee los campos de filtrado de la interfaz
        recupera la lista de propiedades flitrada por ellos mediante Conexion.listadoPropiedadesFiltrado
        y llama a Propiedades.setTablaPropiedades() para cargarlos en la tabla de propiedades

        """
        try:
            var.currentindextablaprop = 0
            tipo_propiedad = var.ui.cmbTipoprop.currentText()
            provincia = var.ui.cmbProvprop.currentText()
            municipio = var.ui.cmbMuniprop.currentText()
            listado = conexion.Conexion.listadoPropiedadesFiltrado(tipo_propiedad, municipio, provincia)
            #listado = conexionserver.ConexionServer.listadoPropiedadesFiltrado(tipo_propiedad, municipio, provincia)
            var.currentlistapropiedades = listado
            Propiedades.setTablaPropiedades()
        except Exception as e:
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def setTablaPropiedades():
        """

        Lee la lista de propiedades guardada en el módulo var
        y muestra su información en la tabla de propiedades

        """
        listado = var.currentlistapropiedades
        eventos.Eventos.setCurrentPageProp()

        if len(listado) == 0:
            var.ui.btnAnteriorprop.setDisabled(True)
            var.ui.btnSiguienteprop.setDisabled(True)
            var.ui.tablaPropiedades.setRowCount(4)
            var.ui.tablaPropiedades.setItem(0, 0, QtWidgets.QTableWidgetItem("No hay propiedades con estos filtros"))
            var.ui.tablaPropiedades.setSpan(0, 0, 4, 9)
            var.ui.tablaPropiedades.item(0, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        else:
            index = 0
            sublistado = listado[var.currentindextablaprop: var.currentindextablaprop + var.rowstablaprop]
            var.ui.tablaPropiedades.setRowCount(len(sublistado))

            if listado[0] == sublistado[0]:
                var.ui.btnAnteriorprop.setDisabled(True)
            else:
                var.ui.btnAnteriorprop.setDisabled(False)

            if listado[-1] == sublistado[-1]:
                var.ui.btnSiguienteprop.setDisabled(True)
            else:
                var.ui.btnSiguienteprop.setDisabled(False)

            for registro in sublistado:
                registro = [x if x != None else '' for x in registro]
                var.ui.tablaPropiedades.clearSpans()
                for j, dato in enumerate(registro):
                    if j in (5, 6):
                        valor = (str(dato) if dato != "" else "-") + " €"
                        var.ui.tablaPropiedades.setItem(index, j, QtWidgets.QTableWidgetItem(valor))
                    else:
                        var.ui.tablaPropiedades.setItem(index, j, QtWidgets.QTableWidgetItem(str(dato)))

                var.ui.tablaPropiedades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaPropiedades.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaPropiedades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaPropiedades.item(index, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaPropiedades.item(index, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                index += 1

            eventos.Eventos.resizeTablaPropiedades()


    @staticmethod
    def cargaOnePropiedad(code = ""):
        """

        :param code: codigo de una propiedad
        :type code: int

        Método que busca la información de la propiedad identificada por el código
        y la carga en los elementos correspondientes de la interfaz
        si se especifica se utiliza ese, si no se lee el elemento seleccionado en la tabla de propiedades

        """
        try:
            if code == "":
                propiedad = var.ui.tablaPropiedades.selectedItems()
                codigo = propiedad[0].text()
            else:
                codigo = code
            datos = conexion.Conexion.datosOnePropiedad(codigo)
            facturas.Facturas.cargaPropiedadVenta(datos)
            #datos = conexionserver.ConexionServer.datosOnePropiedad(codigo)

            datos = [x if x != 'None' else '' for x in datos]

            var.ui.lblProp.setText(str(datos[0]))
            var.ui.txtFechaprop.setText(str(datos[1]))
            var.ui.txtFechabajaprop.setText(str(datos[2]))
            var.ui.txtCPprop.setText(str(datos[3]))
            var.ui.txtDirprop.setText(str(datos[4]))
            var.ui.cmbProvprop.setCurrentText(str(datos[5]))
            var.ui.cmbMuniprop.setCurrentText(str(datos[6]))
            var.ui.cmbTipoprop.setCurrentText(str(datos[7]))
            var.ui.spinHabprop.setValue(int(datos[8]))
            var.ui.spinBanosprop.setValue(int(datos[9]))
            var.ui.txtSuperprop.setText(str(datos[10]))
            var.ui.txtPrecioalquilerprop.setText(str(datos[11]))
            var.ui.txtPrecioventaprop.setText(str(datos[12]))
            var.ui.txtComentarioprop.setText(str(datos[13]))

            tipos_oper = datos[14]
            var.ui.chkAlquilprop.setChecked("Alquiler" in tipos_oper)
            var.ui.chkVentaprop.setChecked("Venta" in tipos_oper)
            var.ui.chkInterprop.setChecked("Intercambio" in tipos_oper)
    
            if datos[15] == "Disponible":
                var.ui.rbtDisponprop.setChecked(True)
            elif datos[15] == "Alquilado":
                var.ui.rbtAlquilprop.setChecked(True)
            elif datos[15] == "Vendido":
                var.ui.rbtVentaprop.setChecked(True)

            var.ui.txtNomeprop.setText(datos[16])
            var.ui.txtMovilprop.setText(datos[17])
        except Exception as e:
            print("Error al cargar a una propiedad", e)

    @staticmethod
    def modifProp():
        """

        Método que lee los datos de la propiedad de la interfaz
        comprueba si se verifican las restricciones necesarias
        y llama a Conexion.modifPropiedad para modificar la información en la base de datos
        mostrando un mensaje con el resultado de la operación

        """
        camposObligatorios = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text(),
                              var.ui.txtSuperprop.text(), var.ui.txtNomeprop.text(), var.ui.txtMovilprop.text()]

        areFieldsMissing = camposObligatorios.count("") > 0
        isBajaOk = var.ui.rbtDisponprop.isChecked() if not var.ui.txtFechabajaprop.text() else not var.ui.rbtDisponprop.isChecked()
        isAlquilerOk = (var.ui.txtPrecioalquilerprop.text() and var.ui.chkAlquilprop.isChecked()) or (not var.ui.txtPrecioalquilerprop.text() and not var.ui.chkAlquilprop.isChecked())
        isVentaOk = (var.ui.txtPrecioventaprop.text() and var.ui.chkVentaprop.isChecked()) or (not var.ui.txtPrecioventaprop.text() and not var.ui.chkVentaprop.isChecked())
        areDatesOk = eventos.Eventos.checkFechas(var.ui.txtFechaprop.text(), var.ui.txtFechabajaprop.text())

        areRequirementsOK = not areFieldsMissing and isBajaOk and isAlquilerOk and isVentaOk and areDatesOk

        propiedad = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text().title(),
                     var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(),
                     var.ui.cmbTipoprop.currentText(), var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(),
                     var.ui.txtSuperprop.text(), var.ui.txtPrecioalquilerprop.text(), var.ui.txtPrecioventaprop.text(),
                     var.ui.txtComentarioprop.toPlainText(), var.ui.txtNomeprop.text().title(), var.ui.txtMovilprop.text()]
        tipooper = []
        if var.ui.chkAlquilprop.isChecked():
            tipooper.append(var.ui.chkAlquilprop.text())
        if var.ui.chkVentaprop.isChecked():
            tipooper.append(var.ui.chkVentaprop.text())
        if var.ui.chkInterprop.isChecked():
            tipooper.append(var.ui.chkInterprop.text())
        propiedad.append(",".join(tipooper))
        if var.ui.rbtDisponprop.isChecked():
            propiedad.append(var.ui.rbtDisponprop.text())
        elif var.ui.rbtAlquilprop.isChecked():
            propiedad.append(var.ui.rbtAlquilprop.text())
        else:
            propiedad.append(var.ui.rbtVentaprop.text())
        propiedad.append(var.ui.txtFechabajaprop.text())
        propiedad.append(var.ui.lblProp.text())

        if areRequirementsOK and conexion.Conexion.modifPropiedad(propiedad):
        #if areRequirementsOK and conexionserver.ConexionServer.modifPropiedad(propiedad):
            eventos.Eventos.mostrarMensajeOk("Propiedad modificada correctamente")
            Propiedades.cargaTablaPropiedades()
        elif areFieldsMissing:
            eventos.Eventos.mostrarMensajeError("Es necesario rellenar todos los campos obligatorios")
        elif not isBajaOk:
            eventos.Eventos.mostrarMensajeError(
            "No se puede modificar porque la fecha de baja y el estado no son coherentes\n -Las propiedades sin fecha de baja deben estar disponibles\n -Las propiedades con fecha de baja no pueden estar disponibles")
        elif not isAlquilerOk:
            eventos.Eventos.mostrarMensajeError("Si es alquilable debe tener precio de Alquiler y vicerversa")
        elif not isVentaOk:
            eventos.Eventos.mostrarMensajeError("Si se puede vender debe tener precio de venta y vicerversa")
        elif not areDatesOk:
            eventos.Eventos.mostrarMensajeError("Hay algún problema con las fechas, compruebe lo siguiente:\n -Las fechas deben de tener el formato dd/mm/aaaa o estar el campo vacío\n -La fecha de baja no puede ser anterior a la de alta")
            var.ui.txtFechabajaprop.setText("")
        else:
            eventos.Eventos.mostrarMensajeError("No se pudo modificar la propiedad")

    @staticmethod
    def bajaProp():
        """

        Método que lee el codigo y la fechabaja de la interfaz de propiedad
        y llama a Conexion.bajaPropiedad para dar a la propiedad correspondiente de baja con la fecha leída
        mostrando un mensaje con el resultado de la operación

        """
        codigo = var.ui.lblProp.text()
        fechabaja = var.ui.txtFechabajaprop.text()
        if var.ui.rbtDisponprop.isChecked():
            disponibilidad = var.ui.rbtDisponprop.text()
        elif var.ui.rbtAlquilprop.isChecked():
            disponibilidad = var.ui.rbtAlquilprop.text()
        else:
            disponibilidad = var.ui.rbtVentaprop.text()

        isDisponible = var.ui.rbtDisponprop.isChecked()
        isBajaOk = (var.ui.rbtAlquilprop.isChecked() and var.ui.chkAlquilprop.isChecked()) or (var.ui.rbtVentaprop.isChecked() and var.ui.chkVentaprop.isChecked())
        areDatesOk = eventos.Eventos.checkFechas(var.ui.txtFechaprop.text(), var.ui.txtFechabajaprop.text())
        requirement = fechabaja and not isDisponible and isBajaOk and areDatesOk
        if requirement and conexion.Conexion.bajaPropiedad(codigo, fechabaja, disponibilidad):
        #if requirement and conexionserver.ConexionServer.bajaPropiedad(codigo, fechabaja, disponibilidad):
            eventos.Eventos.mostrarMensajeOk("Propiedad dada de baja correctamente")
            var.currentindextablaprop = 0
            Propiedades.cargaTablaPropiedades()
        elif isDisponible:
            eventos.Eventos.mostrarMensajeError("Una propiedad no puede estar disponible y darla de baja")
        elif not fechabaja:
            eventos.Eventos.mostrarMensajeError("Debe introducir una fecha para dar de baja a la propiedad")
        elif not isBajaOk:
            eventos.Eventos.mostrarMensajeError("Para que una propiedad se alquile o venda, debe tener esa posibilidad, modifíquela primero")
        elif not areDatesOk:
            eventos.Eventos.mostrarMensajeError("Hay algún problema con las fechas, compruebe lo siguiente:\n -Las fechas deben de tener el formato dd/mm/aaaa o estar el campo vacío\n -La fecha de baja no puede ser anterior a la de alta")
            var.ui.txtFechabajaprop.setText("")
        else:
            eventos.Eventos.mostrarMensajeError("No se pudo dar de baja a la propiedad")

    @staticmethod
    def deleteProp():
        """

        Método que lee el codigo de la interfaz de propiedad
        y llama a Conexion.deletePropiedad para eliminar la propiedad de la base de datos
        mostrando un mensaje con el resultado de la operación
        ESTE MÉTODO NO ES UTILIZADO NUNCA

        """
        codigo = var.ui.lblProp.text()
        if conexion.Conexion.deletePropiedad(codigo):
            eventos.Eventos.mostrarMensajeOk("Propiedad eliminada correctamente")
            var.currentindextablaprop = 0
            Propiedades.cargaTablaPropiedades()
        else:
            eventos.Eventos.mostrarMensajeError("Propiedad no pudo ser eliminada")

    @staticmethod
    def resetFilas():
        """

        Método que reajusta el número de filas que se muestra en cada página de la tabla propiedades
        asegurándose siempre que esté entre un mínimo y un máximo predeterminado
        y seteando de nuevo la página de la tabla propiedades a la primera
        para garantizar el mostrado correcto de los datos

        """
        try:
            if (int(var.ui.filastablaprop.text()) < 1):
                var.ui.filastablaprop.setValue(1)
            if (int(var.ui.filastablaprop.text()) > var.maxrowstablaprop):
                var.ui.filastablaprop.setValue(var.maxrowstablaprop)
            var.rowstablaprop = int(var.ui.filastablaprop.text())
            var.currentindextablaprop = 0
            Propiedades.setTablaPropiedades()
        except Exception as error:
            print("Error al reset filas: ", error)


    @staticmethod
    def historicoProp():
        """

        Método que recarga la tabla de propiedades tras clickar el checkbox de histórico
        reseteando la página de la tabla propiedades a cero para evitar problemas al mostrar datos

        """
        try:
            var.currentindextablaprop = 0
            Propiedades.cargaTablaPropiedades()
        except Exception as error:
            print("Error al actualizar historico")