import eventos
import var
from conexion import Conexion


class Alquileres:
    current_cliente = None
    current_propiedad = None
    current_vendedor = None
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

