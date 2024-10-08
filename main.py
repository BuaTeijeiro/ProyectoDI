from calendar import Calendar

import clientes
import conexion
import eventos
import styles
from venPrincipal import *
from venAux import *
import sys
import var

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion()
        eventos.Eventos.cargarProv()
        eventos.Eventos.cargarMunicipioscli()

        """
        zona de eventos del menubar
        """

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        """
        zona de eventos de botones
        """

        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))

        """
        zona de eventos de cajas de texto
        """

        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailcli.text()))


        """
        combo box
        """
        var.ui.cmbProvcli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipioscli)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())
