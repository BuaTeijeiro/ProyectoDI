from PyQt6 import QtGui

import conexion
import eventos
import var
from PyQt6 import QtWidgets, QtCore




class Facturas:
    current_cliente = None
    current_propiedad = None
    current_vendedor = None
    @staticmethod
    def altaFactura():
        """

        """
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
        """

        """
        try:
            listado = conexion.Conexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                var.botondel = QtWidgets.QPushButton()
                var.botondel.setFixedSize(30, 20)
                var.botondel.setIcon(QtGui.QIcon("./img/basura_bien.ico"))
                var.botondel.setStyleSheet("background-color: #efefef;")
                var.botondel.clicked.connect(Facturas.deleteFactura)
                layout.addWidget(var.botondel)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaFacturas.setItem(index, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tablaFacturas.setItem(index, 1, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tablaFacturas.setItem(index, 2, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tablaFacturas.setCellWidget(index, 3, container)

                var.ui.tablaFacturas.item(index, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tablaFacturas.item(index, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                index += 1
            eventos.Eventos.resizeTablaFacturas()
        except Exception as e:
            print("Error al cargar la tabla de facturas", e)

    @staticmethod
    def cargaOneFactura():
        """

        """
        try:
            factura = var.ui.tablaFacturas.selectedItems()
            var.ui.lblFactura.setText(str(factura[0].text()))
            var.ui.txtFechaFactura.setText(str(factura[1].text()))
            var.ui.lblDniclifactura.setText(str(factura[2].text()))
            Facturas.cargaClienteVenta()
        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al cargar la factura: " + e)

    @staticmethod
    def cargaClienteVenta():
        try:
            dni = var.ui.lblDniclifactura.text()
            cliente = conexion.Conexion.datosOneCliente(dni)
            var.ui.lblApelCli.setText(str(cliente[2]))
            var.ui.lblNombrecli.setText(str(cliente[3]))
            Facturas.current_cliente = dni
            Facturas.checkDatosFacturas()
        except Exception as e:
            Facturas.current_cliente = None
            Facturas.checkDatosFacturas()
            eventos.Eventos.mostrarMensajeError("Error al cargar el cliente: " + e)

    @staticmethod
    def cargaPropiedadVenta(propiedad):
        try:
            if  "venta" in str(propiedad[14]).lower() and str(propiedad[15]).lower() == "disponible":
                var.ui.lblcodigoprop.setText(str(propiedad[0]))
                var.ui.lblTipoProp.setText(str(propiedad[7]))
                var.ui.lblPrecioProp.setText(str(propiedad[12]) + " €")
                var.ui.lblDireccionprop.setText(str(propiedad[4]).title())
                var.ui.lblMunipropVenta.setText(str(propiedad[6]))
                var.ui.lblMensaje.setText("")
                Facturas.current_propiedad = str(propiedad[0])
                Facturas.checkDatosFacturas()
            else:
                var.ui.lblcodigoprop.setText("")
                var.ui.lblTipoProp.setText("")
                var.ui.lblPrecioProp.setText("")
                var.ui.lblDireccionprop.setText("")
                var.ui.lblMunipropVenta.setText("")
                Facturas.current_propiedad = None
                Facturas.checkDatosFacturas()
                if not "venta" in str(propiedad[14]).lower():
                    var.ui.lblMensaje.setText("(La última propiedad seleccionada no se puede vender)")
                else:
                    var.ui.lblMensaje.setText("(La última propiedad seleccionada ya está vendida)")

        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al cargar el cliente: " + e)

    @staticmethod
    def cargaVendedorVenta(id):
        try:
            var.ui.lblVendedorVenta.setText(str(id))
            Facturas.current_vendedor = str(id)
            Facturas.checkDatosFacturas()
        except Exception as e:
            Facturas.current_vendedor = None
            Facturas.checkDatosFacturas()
            eventos.Eventos.mostrarMensajeError("Error al cargar el cliente: " + e)

    @staticmethod
    def checkDatosFacturas():
        if Facturas.current_vendedor is not None and Facturas.current_propiedad is not None and Facturas.current_cliente is not None:
            var.ui.btnGrabarVenta.setDisabled(False)
        else:
            var.ui.btnGrabarVenta.setDisabled(True)

    @staticmethod
    def deleteFactura():
        try:
            factura = var.ui.tablaFacturas.selectedItems()
            if conexion.Conexion.deleteFactura(factura[0].text()):
                eventos.Eventos.mostrarMensajeOk("Se ha eliminado la factura correctamente")
                Facturas.cargarListaFacturas()
            else:
                eventos.Eventos.mostrarMensajeError("No se ha podido eliminar la factura correctamente")
        except Exception as e:
            print("Error al eliminar la factura: ", e)

    @staticmethod
    def grabarVenta():
        print("Se va a guardar la venta")
