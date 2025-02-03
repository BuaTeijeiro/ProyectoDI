from PyQt6 import QtGui

import conexion
import eventos
import informes
import propiedades
import var
from PyQt6 import QtWidgets, QtCore


class Facturas:
    current_cliente = None
    current_propiedad = None
    current_vendedor = None
    current_factura = None
    botones_del = []
    @staticmethod
    def altaFactura():
        """

        Método que lee los datos de la factura de la interfaz
        comprueba si se verifican las restricciones necesarias
        y llama a Conexion.guardarFactura para guardar la información en la base de datos
        mostrando un mensaje con el resultado

        """
        try:
            if (var.ui.txtFechaFactura.text() == "" or var.ui.lblDniclifactura.text() == ""):
                eventos.Eventos.mostrarMensajeError("Es necesario cubrir los datos de fecha y dniCliente")
            else:
                nuevaFactura = [var.ui.txtFechaFactura.text(), var.ui.lblDniclifactura.text()]
                if (conexion.Conexion.guardarFActura(nuevaFactura)):
                    eventos.Eventos.mostrarMensajeOk("Se ha guardado la factura correctamente")
                    Facturas.current_factura = str(conexion.Conexion.getLastIdFactura())
                    var.ui.lblFactura.setText(Facturas.current_factura)
                    Facturas.cargarListaFacturas()
                    Facturas.checkDatosFacturas()
                else:
                    eventos.Eventos.mostrarMensajeError("No se ha podido guardar la factura correctamente")
        except Exception as e:
            eventos.Eventos.mostrarMensajeError(e)

    @staticmethod
    def cargarListaFacturas():
        """

        Método que recupera la lista de facturas mediante Conexion.listadoFacturas
        y muestra dicha información en la tabla de facturas

        """
        try:
            listado = conexion.Conexion.listadoFacturas()
            var.ui.tablaFacturas.setRowCount(len(listado))
            index = 0
            Facturas.botonesdel = []
            for registro in listado:
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                Facturas.botonesdel.append(QtWidgets.QPushButton())
                Facturas.botonesdel[-1].setFixedSize(30, 20)
                Facturas.botonesdel[-1].setIcon(QtGui.QIcon("./img/basura_bien.ico"))
                Facturas.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Facturas.botonesdel[-1].clicked.connect(lambda checked, idFactura=str(registro[0]): Facturas.deleteFactura(idFactura))
                layout.addWidget(Facturas.botonesdel[-1])
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

        Método que lee los datos de la factura seleccionada en la tabla clientes
        y la muestra en los elementos de la interfaz correspondientes
        guarda la información de que hay una factura cargada
        y llama a los métodos que actualizan el resto de la interfaz a partir de ella

        """
        try:
            factura = var.ui.tablaFacturas.selectedItems()
            var.ui.lblFactura.setText(str(factura[0].text()))
            var.ui.txtFechaFactura.setText(str(factura[1].text()))
            var.ui.lblDniclifactura.setText(str(factura[2].text()))
            Facturas.cargaClienteVenta()
            Facturas.cargarTablaVentasFactura()
            Facturas.current_factura = factura[0].text()
            Facturas.limpiarCamposPropiedad()
            Facturas.checkDatosFacturas()
        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al cargar la factura: " + e)

    @staticmethod
    def cargaClienteVenta():
        """

        Método que carga la información del cliente de una factura en los campos de la interfaz correspondientes
        seteando el cliente actual y llamando a los métodos que actualizan información de acuerdo a ello
        en caso de excepción setea el cliente actual a none y llama a los mismo métodos

        """
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
        """

        :param propiedad: propiedad asociada a una venta
        :type propiedad: list

        Método que carga en la interfaz de ventas los datos de la propiedad pasada por parámetros
        setea la propiedad actual y llama a los métodos que la usan para actualizar la interfaz

        """
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
        """

        :param id: id del vendedor
        :type id: int

        Método que carga en la interfaz de ventas el id del vendedor de la Venta
        setea el vendedor actual y llama a los métodos que la usan para actualizar la interfaz

        """
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
        """

        Método que comprueba que todos los campos necesarios para realizar una venta están cargados
        habilitando el botón de grabar venta en caso afirmativo y desahilitándolo en caso negativo

        """
        if Facturas.current_vendedor is not None and Facturas.current_propiedad is not None and Facturas.current_cliente is not None and Facturas.current_factura is not None:
            var.ui.btnGrabarVenta.setDisabled(False)
        else:
            var.ui.btnGrabarVenta.setDisabled(True)
        if Facturas.current_factura is None:
            var.ui.btnGrabarFactura.setDisabled(False)
            var.ui.btnGenerarFactura.setDisabled(True)
        else:
            var.ui.btnGrabarFactura.setDisabled(True)
            var.ui.btnGenerarFactura.setDisabled(False)

    @staticmethod
    def cargarOneVenta():
        try:
            factura = var.ui.tablaVentas.selectedItems()
            var.ui.lblcodigoprop.setText(factura[1].text())
            var.ui.lblTipoProp.setText(factura[4].text())
            var.ui.lblPrecioProp.setText(factura[5].text())
            var.ui.lblDireccionprop.setText(factura[2].text())
            var.ui.lblMunipropVenta.setText(factura[3].text())
            Facturas.current_propiedad = None
            Facturas.checkDatosFacturas()
        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al cargar la factura: " + e)


    @staticmethod
    def limpiarFactura():
        """

        Método que limpia los campos de la interfaz relacionada con una factura
        setea la factura actual a None y llama a los métodos que la usan para actualizar la interfaz

        """
        var.ui.lblFactura.setText("")
        var.ui.txtFechaFactura.setText("")
        var.ui.lblDniclifactura.setText("")
        var.ui.lblApelCli.setText("")
        var.ui.lblNombrecli.setText("")
        var.ui.lblVendedorVenta.setText("")
        Facturas.current_vendedor = None
        Facturas.current_cliente = None
        Facturas.current_factura = None
        Facturas.limpiarCamposPropiedad()
        Facturas.cargarTablaVentasFactura()
        Facturas.checkDatosFacturas()

    @staticmethod
    def deleteFactura(idFactura):
        """

        :param idFactura: id de la Factura
        :type idFactura: int

        Método que tras preguntar confimración para borrar la factura cuyo id es el pasado por parámetros
        llama al método de conexión para borrarla de la base de datos seteando la actual a None
        y llama a los métodos que la usan para actualizar la interfaz

        """
        try:
            mbox = QtWidgets.QMessageBox()
            if eventos.Eventos.mostrarMensajeConfimarcion(mbox, "Borrar", "Esta seguro de que quiere borrar la factura de id " + idFactura) == QtWidgets.QMessageBox.StandardButton.Yes:
                if conexion.Conexion.deleteFactura(idFactura):
                    eventos.Eventos.mostrarMensajeOk("Se ha eliminado la factura correctamente")
                    Facturas.cargarListaFacturas()
                    var.ui.tablaVentas.setRowCount(0)
                    Facturas.current_factura = None
                    Facturas.checkDatosFacturas()
                    Facturas.cargarBottomFactura(idFactura)
                    var.ui.lblFactura.setText("")
                    var.ui.txtFechaFactura.setText("")
                    var.ui.lblDniclifactura.setText("")
                else:
                    #eventos.Eventos.mostrarMensajeError("No se ha podido eliminar la factura correctamente")
                    eventos.Eventos.mostrarMensajeWarning("La factura no se puede eliminar porque tiene asociadas ventas. Bórrelas primero si quiere borrar la factura")
            else:
                mbox.hide()
        except Exception as e:
            print("Error al eliminar la factura: ", e)

    @staticmethod
    def grabarVenta():
        """

        Método que lee los datos de la venta de la interfaz
        llama a Conexion.grabarVenta para guardar la información en la base de datos
        y emplea el método correspondiente para setear la propiedad como vendida
        mostrando un mensaje con el resultado de la operación

        """
        try:
            venta = [Facturas.current_factura, Facturas.current_vendedor, Facturas.current_propiedad]
            if conexion.Conexion.grabarVenta(venta):
                eventos.Eventos.mostrarMensajeOk("Se ha registrado la venta correctamente")
                Facturas.cargarTablaVentasFactura()
                fecha = var.ui.txtFechaFactura.text()
                conexion.Conexion.venderPropiedad(Facturas.current_propiedad, fecha)
                propiedades.Propiedades.cargaTablaPropiedades()
                Facturas.limpiarCamposPropiedad()
            else:
                eventos.Eventos.mostrarMensajeError("No se ha podido registrar la venta correctamente")
        except Exception as e:
            print("Error al grabar venta: ", e)

    @staticmethod
    def eliminarVenta(idVenta, codProp):
        """

        :param idVenta: id de la venta
        :type idVenta: int
        :param codProp: código de la propiedad
        :type codProp: int

        Método que elimina de la base de datos la venta cuyo id se pasa por parámetros
        y actualiza la propiedad con el código pasado por parámetro como disponible

        """
        try:
            mbox = QtWidgets.QMessageBox()
            if eventos.Eventos.mostrarMensajeConfimarcion(mbox, "Borrar",
                                                          "Esta seguro de que quiere borrar la venta de id " + idVenta + " de la propiedad de codigo " + codProp) == QtWidgets.QMessageBox.StandardButton.Yes:
                if conexion.Conexion.liberarPropiedad(codProp) and conexion.Conexion.eliminarVenta(idVenta):
                    eventos.Eventos.mostrarMensajeOk("Venta eliminada correctamente")
                    Facturas.cargarTablaVentasFactura()
                    Facturas.cargarBottomFactura(Facturas.current_factura)
                    propiedades.Propiedades.cargaTablaPropiedades()
                    Facturas.limpiarCamposPropiedad()
                else:
                    eventos.Eventos.mostrarMensajeError("No se pudo eliminar la venta")
            else:
                mbox.hide()

        except Exception as error:
            print("Error al eliminar venta: ", error)

    @staticmethod
    def cargarTablaVentasFactura():
        """

        Método que recupera la lista de ventas cuya factura es la indicada en la interfaz
        y las muestra en la tabla de ventas

        """
        try:
            idFactura = var.ui.lblFactura.text()
            listado = conexion.Conexion.listadoVentas(idFactura)
            var.ui.tablaVentas.setRowCount(len(listado))
            index = 0
            for registro in listado:
                for i, dato in enumerate(registro):
                    if i != 5:
                        var.ui.tablaVentas.setItem(index, i, QtWidgets.QTableWidgetItem(str(dato)))
                    else:
                        var.ui.tablaVentas.setItem(index, i, QtWidgets.QTableWidgetItem(str(dato) + " €"))

                    var.ui.tablaVentas.item(index, i).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                botondel = QtWidgets.QPushButton()
                botondel.setFixedSize(30, 20)
                botondel.setIcon(QtGui.QIcon("./img/menos.ico"))
                botondel.setStyleSheet("background-color: #fff;")
                botondel.clicked.connect(lambda checked, venta=str(registro[0]), prop=str(registro[1]) : Facturas.eliminarVenta(venta, prop))
                layout.addWidget(botondel)
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)
                var.ui.tablaVentas.setCellWidget(index, 6, container)

                index += 1
            eventos.Eventos.resizeTablaVentas()
            Facturas.cargarBottomFactura(idFactura)

        except Exception as e:
            print("Error al cargar la tabla de ventas", e)

    @staticmethod
    def cargarBottomFactura(idFactura):
        """

        :param idFactura: id Factura
        :type idFactura: int

        Método que calcula la parte inferior de la factura, con el subtotal, iva y total

        """
        try:
            subtotal = conexion.Conexion.totalFactura(idFactura)
            if subtotal:
                iva = 10 * subtotal / 100
                total = subtotal + iva
                var.ui.lblSubtotalFactura.setText(f"{subtotal:,.2f}" + " €")
                var.ui.lblImpuestasFacturas.setText(f"{iva:,.2f}" + " €")
                var.ui.lblTotalFactura.setText(f"{total:,.2f}" + " €")
            else:
                var.ui.lblSubtotalFactura.setText("- €")
                var.ui.lblImpuestasFacturas.setText("-%")
                var.ui.lblTotalFactura.setText("- €")
        except Exception as e:
            print("Error al cargar los totales")

    @staticmethod
    def limpiarCamposPropiedad():
        var.ui.lblcodigoprop.setText("")
        var.ui.lblTipoProp.setText("")
        var.ui.lblPrecioProp.setText("")
        var.ui.lblDireccionprop.setText("")
        var.ui.lblMunipropVenta.setText("")
        var.ui.lblMensaje.setText("")
        Facturas.current_propiedad = None

    @staticmethod
    def generarFactura():
        informes.Informes.facturaVenta(Facturas.current_factura)