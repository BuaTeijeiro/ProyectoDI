from tabnanny import check

import conexion
import eventos
import informes
import var
from conexion import Conexion
from PyQt6 import QtWidgets, QtCore, QtGui

from logger import Logger
from model.month import Month
from propiedades import Propiedades


class Alquileres:
    current_cliente = None
    current_propiedad = None
    current_vendedor = None
    current_alquiler = None
    isFinalizado = False
    chkPagado = []
    botonesdel = []
    @staticmethod
    def cargaClienteAlquiler(dni):
        var.ui.lblDnicliAlquiler.setText(dni)
        cliente = Conexion.datosOneCliente(dni)
        var.ui.lblApelCliAlquiler.setText(cliente[2])
        var.ui.lblNombrecliAlquiler.setText(cliente[3])
        Alquileres.current_cliente = dni
        Alquileres.checkDatosAlquiler()

    @staticmethod
    def cargaPropiedadAlquiler(propiedad):
        try:
            if "alquiler" in str(propiedad[14]).lower() and str(propiedad[15]).lower() == "disponible" or Alquileres.current_alquiler:
                var.ui.lblcodigopropAlquiler.setText(str(propiedad[0]))
                var.ui.lblTipoPropAlquiler.setText(str(propiedad[7]))
                var.ui.lblPrecioPropAlquiler.setText(str(propiedad[11]) + " €")
                var.ui.lblDireccionprop_alquiler.setText(str(propiedad[4]).title())
                var.ui.lblMunipropAlquiler.setText(str(propiedad[6]))
                var.ui.lblMensajeAlquiler.setText("")
                Alquileres.current_propiedad = propiedad[0]
            else:
                var.ui.lblcodigopropAlquiler.setText("")
                var.ui.lblTipoPropAlquiler.setText("")
                var.ui.lblPrecioPropAlquiler.setText("")
                var.ui.lblDireccionprop_alquiler.setText("")
                var.ui.lblMunipropAlquiler.setText("")
                Alquileres.current_propiedad = None
                if not "alquiler" in str(propiedad[14]).lower():
                    var.ui.lblMensajeAlquiler.setText("(La última propiedad seleccionada no se puede alquilar)")
                else:
                    var.ui.lblMensajeAlquiler.setText("(La última propiedad seleccionada ya está alquilada)")
            Alquileres.checkDatosAlquiler()

        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al cargar la propiedad: " + e)
            Alquileres.checkDatosAlquiler()

    @staticmethod
    def cargaVendedorAlquiler(idVendedor):
        try:
            var.ui.lblGestorAlquiler.setText(str(idVendedor))
            Alquileres.current_vendedor = idVendedor
            Alquileres.checkDatosAlquiler()

        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al cargar la propiedad: " + e)
            Alquileres.checkDatosAlquiler()


    @staticmethod
    def checkDatosAlquiler():
        if Alquileres.current_propiedad is not None and Alquileres.current_vendedor is not None and Alquileres.current_cliente is not None and Alquileres.current_alquiler is None:
            var.ui.btnGrabarAlquiler.setDisabled(False)
        else:
            var.ui.btnGrabarAlquiler.setDisabled(True)

        if Alquileres.current_alquiler and not Alquileres.isFinalizado:
            print("camino 1")
            var.ui.btnModificarAlquiler.setDisabled(False)
            var.ui.btnFechaInicioAlquiler.setDisabled(True)
            var.ui.btnFechaFinAlquiler.setDisabled(False)
            var.ui.chkFinalizado.setDisabled(False)
        elif Alquileres.isFinalizado:
            print("camino 2")
            var.ui.btnModificarAlquiler.setDisabled(True)
            var.ui.btnFechaInicioAlquiler.setDisabled(True)
            var.ui.btnFechaFinAlquiler.setDisabled(True)
            var.ui.chkFinalizado.setDisabled(True)
        else:
            print("camino 3")
            var.ui.btnModificarAlquiler.setDisabled(True)
            var.ui.btnFechaInicioAlquiler.setDisabled(False)
            var.ui.btnFechaFinAlquiler.setDisabled(False)
            var.ui.chkFinalizado.setDisabled(False)

    @staticmethod
    def grabarAlquiler():
        if var.ui.txtFechaInicioAlquiler.text()!= "" and var.ui.txtFechaFinAlquiler.text()!= "":
            alquiler = [Alquileres.current_propiedad, Alquileres.current_cliente, Alquileres.current_vendedor, var.ui.txtFechaInicioAlquiler.text(), var.ui.txtFechaFinAlquiler.text()]
            mes_inicio = Month.ofDateString(var.ui.txtFechaInicioAlquiler.text())
            mes_fin = Month.ofDateString(var.ui.txtFechaFinAlquiler.text())
            if mes_inicio <= mes_fin and conexion.Conexion.grabarAlquiler(alquiler):
                eventos.Eventos.mostrarMensajeOk("Alquiler grabado correctamente")
                conexion.Conexion.alquilarPropiedad(Alquileres.current_propiedad, var.ui.txtFechaInicioAlquiler.text())
                idAlquiler = conexion.Conexion.getLastIdAlquiler()
                Alquileres.generarMensualidades(idAlquiler)
                Alquileres.cargarTablaAlquileres()
                Alquileres.limpiarPanelAlquileres()
                Propiedades.cargaTablaPropiedades()
            elif mes_inicio > mes_fin:
                eventos.Eventos.mostrarMensajeError("El mes de fin de alquiler no puede ser anterior al de inicio de alquiler")
            else:
                eventos.Eventos.mostrarMensajeError("No se ha podido grabar el alquiler")
        else:
            eventos.Eventos.mostrarMensajeError("Las fechas de inicio y de fin son obligatorias")

    @staticmethod
    def generarMensualidades(idAlquiler):
        alquiler = conexion.Conexion.datosOneAlquiler(idAlquiler)
        fecha_inicio = eventos.Eventos.convertStringToDate(alquiler[4])
        fecha_fin = eventos.Eventos.convertStringToDate(alquiler[5])
        mes_fin = Month(fecha_fin.year, fecha_fin.month)
        mes = Month(fecha_inicio.year, fecha_inicio.month)
        while mes <= mes_fin:
            conexion.Conexion.grabarMensualidad(idAlquiler, mes)
            mes.addmonth()

    @staticmethod
    def cargaOneAlquiler():
        if Alquileres.current_propiedad is None:
            alquiler = var.ui.tablaAlquileres.selectedItems()
            Alquileres.current_alquiler = alquiler[0].text()
        datosAlquiler = conexion.Conexion.datosOneAlquiler(Alquileres.current_alquiler)
        Alquileres.cargaClienteAlquiler(datosAlquiler[2])
        Alquileres.cargaVendedorAlquiler(datosAlquiler[3])
        Alquileres.cargaPropiedadAlquiler(conexion.Conexion.datosOnePropiedad(datosAlquiler[1]))
        var.ui.lblAlquiler.setText(str(datosAlquiler[0]))
        var.ui.txtFechaInicioAlquiler.setText(datosAlquiler[4])
        var.ui.txtFechaFinAlquiler.setText(datosAlquiler[5])
        Alquileres.isFinalizado = datosAlquiler[6] == 1
        var.ui.chkFinalizado.setChecked(Alquileres.isFinalizado)
        Alquileres.cargaTablaMensualidades(datosAlquiler[0])
        Alquileres.checkDatosAlquiler()

    @staticmethod
    def setOneAlquiler():
        alquiler = var.ui.tablaAlquileres.selectedItems()
        Alquileres.current_alquiler = alquiler[0].text()
        Alquileres.cargaOneAlquiler()


    @staticmethod
    def modificarContrato():
        try:
            idAlquiler = Alquileres.current_alquiler
            newMonth = Month.ofDateString(var.ui.txtFechaFinAlquiler.text())
            alquiler = conexion.Conexion.datosOneAlquiler(idAlquiler)
            oldMonth = Month.ofDateString(alquiler[5])
            startMonth = Month.ofDateString(var.ui.txtFechaInicioAlquiler.text())
            if newMonth < startMonth:
                eventos.Eventos.mostrarMensajeError("El mes de fin de alquiler no puede ser anterior al de inicio de alquiler")
                return
            if newMonth < oldMonth:
                mensualidadesToDelete = Alquileres.getMensualidadesInPeriodo(idAlquiler, newMonth.addmonth(), oldMonth)
                if Alquileres.checkMensualidadesNoPagadas(mensualidadesToDelete):
                    ids = [x[0] for x in mensualidadesToDelete]
                    if conexion.Conexion.eliminarMensualidades(ids):
                        eventos.Eventos.mostrarMensajeOk(f"Se han borrado %d mensualidades" % len(ids))
                        conexion.Conexion.modificarFechaAlquiler(idAlquiler, var.ui.txtFechaFinAlquiler.text())
                        Alquileres.cargaOneAlquiler()
                else:
                    eventos.Eventos.mostrarMensajeError("No se puede reducir el contrato, porque hay mensualidades ya pagadas")
                    Alquileres.cargaOneAlquiler()

            elif newMonth > oldMonth:
                mensualidadesAdded = Alquileres.ampliarMensualidades(idAlquiler, oldMonth, newMonth)
                conexion.Conexion.modificarFechaAlquiler(idAlquiler, var.ui.txtFechaFinAlquiler.text())
                eventos.Eventos.mostrarMensajeOk(f"Se amplió el contrato en %d mensualidades" %mensualidadesAdded)
                Alquileres.cargaOneAlquiler()

            else:
                eventos.Eventos.mostrarMensajeWarning("No se está modificando el mes de fin de contrato")
        except Exception as error:
            print("Error al reducir el contrato: ", error)

    @staticmethod
    def ampliarMensualidades(idAlquiler, oldMonth, newMonth):
        oldMonth.addmonth()
        mensualidadesAdded = 0
        while oldMonth <= newMonth:
            conexion.Conexion.grabarMensualidad(idAlquiler, oldMonth)
            mensualidadesAdded += 1
            oldMonth.addmonth()
        return mensualidadesAdded

    @staticmethod
    def checkMensualidadesNoPagadas(mensualidades):
        for mensualidad in mensualidades:
            if mensualidad[3]:
                return False
        return True

    @staticmethod
    def setFinalizado():
        try:
            mbox = QtWidgets.QMessageBox()
            if eventos.Eventos.mostrarMensajeConfimarcion(mbox, "Borrar",
                                                          "Cuidado, esta acción finalizará el contrato de alquiler seleccionado de forma irreversible, impidiendo modificaciones salvo el registro de pagos retrasados") == QtWidgets.QMessageBox.StandardButton.Yes:
                idAlquiler = Alquileres.current_alquiler
                if conexion.Conexion.setFinalizado(idAlquiler):
                    eventos.Eventos.mostrarMensajeOk("Se ha registrado el alquiler como terminado")
                    codigo = conexion.Conexion.datosOneAlquiler(idAlquiler)[1]
                    conexion.Conexion.liberarPropiedad(codigo)
                    Alquileres.cargarTablaAlquileres()
                    Propiedades.cargaTablaPropiedades()
                    Alquileres.isFinalizado = True
                    Alquileres.checkDatosAlquiler()

            else:
                var.ui.chkFinalizado.setChecked(False)
                mbox.hide()

        except Exception as e:
            Logger.log("Error al setear el estado finalizado : ", e)


    @staticmethod
    def getMensualidadesInPeriodo(idAlquiler, monthInicio, monthFin):
        listadoMensualidades = conexion.Conexion.listadoMensualidadesAlquiler(idAlquiler)
        listadoFiltrado = []
        for mensualidad in listadoMensualidades:
            mes = Month(int(mensualidad[2]), int(mensualidad[1]))
            if mes >= monthInicio and mes <= monthFin:
                listadoFiltrado.append(mensualidad)
        return listadoFiltrado



    @staticmethod
    def cargaTablaMensualidades(idAlquiler):
        listado = conexion.Conexion.listadoMensualidadesAlquiler(idAlquiler)
        if listado:
            propiedad = conexion.Conexion.datosOnePropiedad(conexion.Conexion.datosOneAlquiler(idAlquiler)[1])
        try:
            var.ui.tablaMensualidades.setRowCount(len(listado))
            index = 0
            Alquileres.chkPagado = []
            for registro in listado:
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                chkbox = QtWidgets.QCheckBox()
                chkbox.setChecked(registro[3] == 1)
                chkbox.stateChanged.connect(
                    lambda checked, idMensualidad=str(registro[0]): Alquileres.pagarMensualidad(idMensualidad, checked))
                Alquileres.chkPagado.append(chkbox)
                layout.addWidget(chkbox)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)

                var.ui.tablaMensualidades.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaMensualidades.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[4])))
                mes = Month(int(registro[2]), int(registro[1]))
                var.ui.tablaMensualidades.setItem(index, 2, QtWidgets.QTableWidgetItem(str(mes)))
                var.ui.tablaMensualidades.setItem(index, 3, QtWidgets.QTableWidgetItem(f"{propiedad[11]:,.2f}" + " €"))
                var.ui.tablaMensualidades.setCellWidget(index, 4, container)

                var.ui.tablaMensualidades.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaMensualidades.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
            eventos.Eventos.resizeTablaMensualidades()

        except Exception as e:
            print("Error al cargar la tabla de ventas", e)

    @staticmethod
    def pagarMensualidad(idMensualidad, pagada):
        if pagada:
            if conexion.Conexion.setMensualidadPagada(idMensualidad, pagada):
                eventos.Eventos.mostrarMensajeOk("Se ha registrado el nuevo estado de pago")
            else:
                eventos.Eventos.mostrarMensajeError("No se ha podido registrar el estado de pago")
        else:
            eventos.Eventos.mostrarMensajeError("No se puede eliminar un pago")
        Alquileres.cargaOneAlquiler()

    @staticmethod
    def generarRecibo():
        mensualidad = var.ui.tablaMensualidades.selectedItems()
        mensualidad = conexion.Conexion.datosOneMensualidad(mensualidad[0].text())
        if mensualidad:
            informes.Informes.reciboMensualidad(mensualidad)
        else:
            eventos.Eventos.mostrarMensajeError("Es necesario seleccionar una mensualidad para generar el recibo")

    @staticmethod
    def cargarTablaAlquileres():
        """

        Método que recupera la lista de alquileres mediante Conexion.listadoAlquileres
        y muestra dicha información en la tabla de alquileres

        """
        try:
            listado = conexion.Conexion.listadoAlquileres()
            var.ui.tablaAlquileres.setRowCount(len(listado))
            index = 0

            Alquileres.botonesdel = []
            for registro in listado:
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                activo = "No" if registro[3] else "Sí"
                Alquileres.botonesdel.append(QtWidgets.QPushButton())
                Alquileres.botonesdel[-1].setFixedSize(30, 20)
                Alquileres.botonesdel[-1].setIcon(QtGui.QIcon("./img/basura_bien.ico"))
                Alquileres.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Alquileres.botonesdel[-1].clicked.connect(
                    lambda checked, idFactura=str(registro[0]): Alquileres.borrarContratoAlquiler(idFactura))
                layout.addWidget(Alquileres.botonesdel[-1])
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaAlquileres.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaAlquileres.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tablaAlquileres.setItem(index, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tablaAlquileres.setItem(index, 3, QtWidgets.QTableWidgetItem(activo))
                var.ui.tablaAlquileres.setCellWidget(index, 4, container)

                var.ui.tablaAlquileres.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaAlquileres.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaAlquileres.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaAlquileres.item(index, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
            eventos.Eventos.resizeTablaAlquileres()
        except Exception as e:
            print("Error al cargar la tabla de facturas", e)

    @staticmethod
    def borrarContratoAlquiler(idAlquiler):
        try:
            mbox = QtWidgets.QMessageBox()
            if eventos.Eventos.mostrarMensajeConfimarcion(mbox, "Borrar", "Esta seguro de que quiere borrar el contrato de alquiler de id " + idAlquiler) == QtWidgets.QMessageBox.StandardButton.Yes:
                codigoPropiedad = conexion.Conexion.datosOneAlquiler(idAlquiler)[1]
                if Alquileres.checkMensualidadesNoPagadas(conexion.Conexion.listadoMensualidadesAlquiler(idAlquiler)) and conexion.Conexion.eliminarAlquiler(idAlquiler):
                    eventos.Eventos.mostrarMensajeOk("Se ha eliminado el alquiler correctamente")
                    Alquileres.cargarTablaAlquileres()
                    Alquileres.limpiarPanelAlquileres()
                    conexion.Conexion.liberarPropiedad(codigoPropiedad)
                    Propiedades.cargaTablaPropiedades()
                else:
                    eventos.Eventos.mostrarMensajeWarning("No se ha podido eliminar el alquiler correctamente. Si tiene recibos ya pagados no se puede borrar")
            else:
                mbox.hide()
        
        except Exception as e:
            print("Error al eliminar el contrato de alquiler: ", e)


    @staticmethod
    def limpiarPanelAlquileres():
        try:
            elementos = [var.ui.lblDnicliAlquiler, var.ui.lblApelCliAlquiler, var.ui.lblNombrecliAlquiler, var.ui.lblcodigopropAlquiler, var.ui.lblTipoPropAlquiler, var.ui.lblPrecioPropAlquiler, var.ui.lblDireccionprop_alquiler, var.ui.lblMunipropAlquiler, var.ui.lblGestorAlquiler, var.ui.lblAlquiler, var.ui.txtFechaInicioAlquiler, var.ui.txtFechaFinAlquiler, var.ui.lblMensajeAlquiler]
            for elemento in elementos:
                elemento.setText("")
            Alquileres.current_propiedad = None
            Alquileres.current_cliente = None
            Alquileres.current_vendedor = None
            Alquileres.current_alquiler = None
            Alquileres.isFinalizado = False
            Alquileres.cargaTablaMensualidades(0)
            Alquileres.checkDatosAlquiler()
        except Exception as e:
            print("Error al limpiar el alquiler: ", e)