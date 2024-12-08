from calendar import Calendar

import clientes
import conexion
import conexionserver
import eventos
import propiedades
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

        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion()
        #conexionserver.ConexionServer.crear_conexion()

        var.uicalendar = Calendar()
        var.dlgabrir = FileDialogAbrir()
        var.dlggestion = dlg_Tipoprop()
        var.dlgabout = dlg_About()
        var.currentindextablacli = 0
        var.currentindextablaprop = 0
        var.ui.btnAnteriorcli.setDisabled(True)
        var.ui.btnAnteriorprop.setDisabled(True)


        eventos.Eventos.cargarProv()
        eventos.Eventos.cargarMunicipioscli()
        eventos.Eventos.cargarMunicipiosprop()
        eventos.Eventos.cargarTiposprop()

        """
        zona de eventos de tablas
        """
        clientes.Clientes.cargaTablaClientes()


        propiedades.Propiedades.cargaTablaPropiedades()
        var.ui.tablaClientes.clicked.connect(clientes.Clientes.cargaOneCliente)
        var.ui.tablaPropiedades.clicked.connect(lambda: propiedades.Propiedades.cargaOnePropiedad())

        """
        zona de eventos del menubar
        """

        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionExportar_Clientes_CSV.triggered.connect(eventos.Eventos.exportarCSVProp)
        var.ui.actionExportar_Clientes_JSON.triggered.connect(eventos.Eventos.exportarJsonProp)
        var.ui.actionTipoPropiedades.triggered.connect(eventos.Eventos.abrirTipoprop)
        var.ui.actionAcerca_de.triggered.connect(eventos.Eventos.abrirAbout)


        """
        zona de eventos del toolbar
        """

        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionGestipoprop.triggered.connect(eventos.Eventos.abrirTipoprop)
        var.ui.actionBuscar.triggered.connect(propiedades.Propiedades.filtrarTablaPropiedades)

        """
        zona de eventos de botones
        """

        var.ui.btnGrabarcli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnBuscarCliente.clicked.connect(clientes.Clientes.cargaClienteBuscado)
        var.ui.btnAltacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnBajacli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))
        var.ui.btnFechaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnFechabajaprop.clicked.connect(lambda: eventos.Eventos.abrirCalendar(1))
        var.ui.btnModifcli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelcli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnGrabarprop.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModifprop.clicked.connect(propiedades.Propiedades.modifProp)
        var.ui.btnDelprop.clicked.connect(propiedades.Propiedades.bajaProp)
        var.ui.btnSiguientecli.clicked.connect(eventos.Eventos.avanzarTablacli)
        var.ui.btnAnteriorcli.clicked.connect(eventos.Eventos.retrocederTablacli)
        var.ui.btnSiguienteprop.clicked.connect(eventos.Eventos.avanzarTablaprop)
        var.ui.btnAnteriorprop.clicked.connect(eventos.Eventos.retrocederTablaprop)


        """
        zona de eventos de cajas de texto
        """

        var.ui.txtDnicli.editingFinished.connect(lambda: clientes.Clientes.checkDNI(var.ui.txtDnicli.text()))
        var.ui.txtEmailcli.editingFinished.connect(clientes.Clientes.checkEmail)
        var.ui.txtMovilcli.editingFinished.connect(clientes.Clientes.checkMovil)
        var.ui.txtMovilprop.editingFinished.connect(propiedades.Propiedades.checkMovil)
        var.ui.txtFechabajaprop.textChanged.connect(propiedades.Propiedades.reloadDisponibility)
        var.ui.txtPrecioventaprop.textChanged.connect(propiedades.Propiedades.reloadTipoOperacion)
        var.ui.txtPrecioalquilerprop.textChanged.connect(propiedades.Propiedades.reloadTipoOperacion)


        """
        combo box
        """
        var.ui.cmbProvcli.currentIndexChanged.connect(eventos.Eventos.cargarMunicipioscli)
        var.ui.cmbProvprop.currentIndexChanged.connect(eventos.Eventos.cargarMunicipiosprop)

        var.ui.cmbMuniprop.setEditable(True)
        var.ui.cmbProvprop.setEditable(True)
        var.ui.cmbMunicli.setEditable(True)
        var.ui.cmbProvcli.setEditable(True)

        completer = QtWidgets.QCompleter(var.provincias, var.ui.cmbProvprop)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbProvprop.setCompleter(completer)

        completer = QtWidgets.QCompleter(var.provincias, var.ui.cmbProvcli)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        var.ui.cmbProvcli.setCompleter(completer)

        var.ui.cmbProvprop.lineEdit().editingFinished.connect(eventos.Eventos.checkProvinciaProp)
        var.ui.cmbMuniprop.lineEdit().editingFinished.connect(eventos.Eventos.checkMunicipioProp)
        var.ui.cmbProvcli.lineEdit().editingFinished.connect(eventos.Eventos.checkProvinciaCli)
        var.ui.cmbMunicli.lineEdit().editingFinished.connect(eventos.Eventos.checkMunicipioCli)

        """
        eventos de checkbox
        """
        var.ui.chkHistoriacli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoriprop.stateChanged.connect(propiedades.Propiedades.historicoProp)
        var.ui.chkVentaprop.stateChanged.connect(propiedades.Propiedades.reloadPrecio)
        var.ui.chkAlquilprop.stateChanged.connect(propiedades.Propiedades.reloadPrecio)

        """
        eventos de spinbox
        """
        var.ui.filastablacli.setValue(var.rowstablacli)
        var.ui.filastablacli.valueChanged.connect(clientes.Clientes.resetFilas)
        var.ui.filastablaprop.setValue(var.rowstablaprop)
        var.ui.filastablaprop.valueChanged.connect(propiedades.Propiedades.resetFilas)

        """
        Radio buttons
        """
        var.ui.rbtAlquilprop.setEnabled(False)
        var.ui.rbtVentaprop.setEnabled(False)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())
