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
    def cargaTablaPropiedades():
        eventos.Eventos.resizeTablaPropiedades()

    @staticmethod
    def altaTipoPropiedad():
        tipo = var.dlggestion.txtGestipoprop.text()
        print("hola")

    @staticmethod
    def altaPropiedad():
        try:
            propiedad = [var.ui.txtFechaprop.text(), var.ui.txtFechabajaprop.text(), var.ui.txtDirprop.text(),var.ui.cmbProvprop.currentText(), var.ui.cmbMuniprop.currentText(), var.ui.txtCPprop.text(), var.ui.cmbTipoprop.currentText(), var.ui.spinHabprop.text(), var.ui.spinBanosprop.text(), var.ui.txtSuperprop.text(), var.ui.txtPrecioventaprop.text(), var.ui.txtPrecioalquilerprop.text(), var.ui.txtComentarioprop.toPlainText(), var.ui.txtNomeprop.text(),var.ui.txtMovilprop.text()]
            print(propiedad)
        except Exception as error:
            print("Error al dar de alta la propiedad")