

import conexion
import eventos
import var
from conexion import Conexion
from PyQt6 import QtWidgets, QtCore

from model.month import Month


class Alquileres:
    current_cliente = None
    current_propiedad = None
    current_vendedor = None
    current_fecha_inicio = None
    current_fecha_fin = None
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
            if "alquiler" in str(propiedad[14]).lower() and str(propiedad[15]).lower() == "disponible":
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
        if Alquileres.current_propiedad is not None and Alquileres.current_vendedor is not None and Alquileres.current_cliente is not None:
            var.ui.btnGrabarAlquiler.setDisabled(False)
        else:
            var.ui.btnGrabarAlquiler.setDisabled(True)

    @staticmethod
    def grabarAlquiler():
        if (var.ui.txtFechaInicioAlquiler.text()!= "" and var.ui.txtFechaFinAlquiler.text()!= ""):
            alquiler = [Alquileres.current_propiedad, Alquileres.current_cliente, Alquileres.current_vendedor, var.ui.txtFechaInicioAlquiler.text(), var.ui.txtFechaFinAlquiler.text()]
            if (conexion.Conexion.grabarAlquiler(alquiler)):
                eventos.Eventos.mostrarMensajeOk("Alquiler grabado correctamente")

            else:
                eventos.Eventos.mostrarMensajeError("No se ha podido grabar el alquiler")
        else:
            eventos.Eventos.mostrarMensajeError("Las fechas de inicio y de fin son obligatorias")

    @staticmethod
    def generarMensualidades(id):
        alquiler = conexion.Conexion.datosOneAlquiler(id)
        fecha_inicio = eventos.Eventos.convertStringToDate(alquiler[4])
        fecha_fin = eventos.Eventos.convertStringToDate(alquiler[5])
        mes_fin = Month(fecha_fin.year, fecha_fin.month)
        mes = Month(fecha_inicio.year, fecha_inicio.month)
        while (mes <= mes_fin):
            conexion.Conexion.grabarMensualidad(id, mes.get_nombre())
            mes.addmonth()

    @staticmethod
    def cargaOneAlquiler():
        alquiler = var.ui.tablaAlquileres.selectedItems()
        mensualidades = conexion.Conexion.listadoMensualidadesAlquiler(alquiler[0].text())

    @staticmethod
    def cargaTablaMensualidades(listado):
        try:
            var.ui.tablaVentas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tablaFacturas.setItem(index, 3, QtWidgets.QTableWidgetItem(registro[2]))



                index += 1

        except Exception as e:
            print("Error al cargar la tabla de ventas", e)

    @staticmethod
    def cargarTablaAlquileres():
        """

        Método que recupera la lista de alquileres mediante Conexion.listadoAlquileres
        y muestra dicha información en la tabla de alquileres

        """
        try:
            listado = conexion.Conexion.listadoAlquileres()
            print(listado)
            var.ui.tablaAlquileres.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaAlquileres.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaAlquileres.setItem(index, 1, QtWidgets.QTableWidgetItem(str(registro[1])))

                var.ui.tablaAlquileres.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaAlquileres.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
            eventos.Eventos.resizeTablaAlquileres()
        except Exception as e:
            print("Error al cargar la tabla de facturas", e)