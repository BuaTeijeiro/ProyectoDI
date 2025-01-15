import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtCore


class Facturas:
    @staticmethod
    def altaFactura():
        try:
            if (var.ui.txtFechaFactura.text() == "" or var.ui.lblDniclifactura.text() == ""):
                eventos.Eventos.mostrarMensajeError("Es necesario cubrir los datos de fecha y dniCliente")
            else:
                nuevaFactura = [var.ui.txtFechaFactura.text(), var.ui.lblDniclifactura.text()]
                if (conexion.Conexion.guardarFActura(nuevaFactura)):
                    eventos.Eventos.mostrarMensajeOk("Se ha guardado la factura correctamente")
                    var.ui.lblFactura.setText(str(conexion.Conexion.getLastIdFactura()))
                    Facturas.cargarListaFacturas()
                else:
                    eventos.Eventos.mostrarMensajeError("No se ha podido guardar la factura correctamente")
        except Exception as e:
            eventos.Eventos.mostrarMensajeError(e)

    @staticmethod
    def cargarListaFacturas():
        try:
            listado = conexion.Conexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tablaFacturas.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2]))

                var.ui.tablaFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tablaFacturas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                index += 1
            eventos.Eventos.resizeTablaFacturas()
        except Exception as e:
            print("Error al cargar la tabla de facturas", e)

    @staticmethod
    def cargaOneFactura():
        try:
            factura = var.ui.tablaFacturas.selectedItems()
            var.ui.lblFactura.setText(str(factura[0].text()))
            var.ui.txtFechaFactura.setText(str(factura[1].text()))
            var.ui.lblDniclifactura.setText(str(factura[2].text()))
        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al cargar la factura: ", e)