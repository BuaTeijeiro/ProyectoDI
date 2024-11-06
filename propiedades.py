from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import var
import eventos


class Propiedades():
    @staticmethod
    def checkMovil():
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
    def altaTipoPropiedad():
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
        try:
            camposObligatorios = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text(), var.ui.txtSuperprop.text(),  var.ui.txtNomeprop.text(),var.ui.txtMovilprop.text()]

            areFieldsMissing = camposObligatorios.count("") > 0


            propiedad = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(), var.ui.cmbTipoprop.currentText(), var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(), var.ui.txtPrecioalquilerprop.text(), var.ui.txtPrecioventaprop.text(), var.ui.txtComentarioprop.toPlainText(), var.ui.txtNomeprop.text(),var.ui.txtMovilprop.text()]
            tipooper = []
            if var.ui.chkAlquilprop.isChecked():
                tipooper.append(var.ui.chkAlquilprop.text())
            if var.ui.chkVentaprop.isChecked():
                tipooper.append(var.ui.chkVentaprop.text())
            if var.ui.chkInterprop.isChecked():
                tipooper.append(var.ui.chkInterprop.text())
            propiedad.append(tipooper)
            if var.ui.rbtDisponprop.isChecked():
                propiedad.append(var.ui.rbtDisponprop.text())
            elif var.ui.rbtAlquilprop.isChecked():
                propiedad.append(var.ui.rbtAlquilprop.text())
            else:
                propiedad.append(var.ui.rbtVentaprop.text())


            if not areFieldsMissing and conexion.Conexion.altaPropiedad(propiedad):
                eventos.Eventos.mostrarMensajeOk("Se ha guardado la propiedad correctamente")
                Propiedades.cargaTablaPropiedades()
            elif areFieldsMissing:
                eventos.Eventos.mostrarMensajeError("Es necesario rellenar todos los campos obligatorios")
            else:
                eventos.Eventos.mostrarMensajeError("Error al guardar la propiedad")
        except Exception as error:
            print("Error al dar de alta la propiedad")

    @staticmethod
    def cargaTablaPropiedades():
        try:
            listado = conexion.Conexion.listadoPropiedades()
            # listado = conexionserver.ConexionServer.listadoClientes()
            Propiedades.setTablaPropiedades(listado)

        except Exception as e:
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def filtrarTablaPropiedades():
        try:
            tipo_propiedad = var.ui.cmbTipoprop.currentText()
            provincia = var.ui.cmbProvprop.currentText()
            municipio = var.ui.cmbMuniprop.currentText()
            listado = conexion.Conexion.listadoPropiedadesFiltrado(tipo_propiedad, municipio, provincia)
            Propiedades.setTablaPropiedades(listado)
        except Exception as e:
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def setTablaPropiedades(listado):
        index = 0
        var.ui.tablaPropiedades.setRowCount(len(listado))
        for registro in listado:
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
    def cargaOnePropiedad():
        try:
            propiedad = var.ui.tablaPropiedades.selectedItems()
            codigo = propiedad[0].text()
            datos = conexion.Conexion.datosOnePropiedad(codigo)

            var.ui.lblProp.setText(str(datos[0]))
            var.ui.txtFechaprop.setText(datos[1])
            var.ui.txtFechabajaprop.setText(datos[2])
            var.ui.txtCPprop.setText(datos[3])
            var.ui.txtDirprop.setText(datos[4])
            var.ui.cmbProvprop.setCurrentText(datos[5])
            var.ui.cmbMuniprop.setCurrentText(datos[6])
            var.ui.cmbTipoprop.setCurrentText(datos[7])
            var.ui.spinHabprop.setValue(datos[8])
            var.ui.spinBanosprop.setValue(datos[9])
            var.ui.txtSuperprop.setText(str(datos[10]))
            var.ui.txtPrecioalquilerprop.setText(str(datos[11]))
            var.ui.txtPrecioventaprop.setText(str(datos[12]))
            var.ui.txtComentarioprop.setText(datos[13])

            tipos_oper = datos[14].rsplit(",")
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
            print("Error al cargar la tabla de clientes", e)

    @staticmethod
    def modifProp():
        camposObligatorios = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text(),
                              var.ui.txtSuperprop.text(), var.ui.txtNomeprop.text(), var.ui.txtMovilprop.text()]

        areFieldsMissing = camposObligatorios.count("") > 0
        isBajaOk = var.ui.rbtDisponprop.isChecked() if not var.ui.txtFechabajaprop.text() else not var.ui.rbtDisponprop.isChecked()
        areRequirementsOK = not areFieldsMissing and isBajaOk

        propiedad = [var.ui.txtFechaprop.text(), var.ui.txtCPprop.text(), var.ui.txtDirprop.text(),
                     var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(),
                     var.ui.cmbTipoprop.currentText(), var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(),
                     var.ui.txtSuperprop.text(), var.ui.txtPrecioalquilerprop.text(), var.ui.txtPrecioventaprop.text(),
                     var.ui.txtComentarioprop.toPlainText(), var.ui.txtNomeprop.text(), var.ui.txtMovilprop.text()]
        tipooper = []
        if var.ui.chkAlquilprop.isChecked():
            tipooper.append(var.ui.chkAlquilprop.text())
        if var.ui.chkVentaprop.isChecked():
            tipooper.append(var.ui.chkVentaprop.text())
        if var.ui.chkInterprop.isChecked():
            tipooper.append(var.ui.chkInterprop.text())
        propiedad.append(tipooper)
        if var.ui.rbtDisponprop.isChecked():
            propiedad.append(var.ui.rbtDisponprop.text())
        elif var.ui.rbtAlquilprop.isChecked():
            propiedad.append(var.ui.rbtAlquilprop.text())
        else:
            propiedad.append(var.ui.rbtVentaprop.text())
        propiedad.append(var.ui.txtFechabajaprop.text())
        propiedad.append(var.ui.lblProp.text())

        if areRequirementsOK and conexion.Conexion.modifPropiedad(propiedad):
            eventos.Eventos.mostrarMensajeOk("Propiedad modificada correctamente")
            Propiedades.cargaTablaPropiedades()
        elif not isBajaOk:
            eventos.Eventos.mostrarMensajeError("No se puede modificar porque la fecha de baja y el estado no son coherentes\n -Las propiedades sin fecha de baja deben estar disponibles\n -Las propiedades con fecha de baja no pueden estar disponibles")
        elif areFieldsMissing:
            eventos.Eventos.mostrarMensajeError("Es necesario rellenar todos los campos obligatorios")
        else:
            eventos.Eventos.mostrarMensajeError("No se pudo modificar la propiedad")

    @staticmethod
    def bajaProp():
        codigo = var.ui.lblProp.text()
        fechabaja = var.ui.txtFechabajaprop.text()
        isDisponible = var.ui.rbtDisponprop.isChecked()
        requirement = fechabaja and not isDisponible
        if requirement and conexion.Conexion.bajaPropiedad(codigo, fechabaja):
            eventos.Eventos.mostrarMensajeOk("Propiedad dada de baja correctamente")
            Propiedades.cargaTablaPropiedades()
        elif isDisponible:
            eventos.Eventos.mostrarMensajeError("Una propiedad no puede estar disponible y darla de baja")
        elif not fechabaja:
            eventos.Eventos.mostrarMensajeError("Debe introducir una fecha para dar de baja a la propiedad")
        else:
            eventos.Eventos.mostrarMensajeError("No se pudo dar de baja a la propiedad")

    @staticmethod
    def deleteProp():
        codigo = var.ui.lblProp.text()
        if conexion.Conexion.deletePropiedad(codigo):
            eventos.Eventos.mostrarMensajeOk("Propiedad eliminada correctamente")
            Propiedades.cargaTablaPropiedades()
        else:
            eventos.Eventos.mostrarMensajeError("Propiedad no pudo ser eliminada")