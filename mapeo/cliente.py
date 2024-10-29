import var

class Cliente:
    def __init__(self):
        self.dni = ""
        self.fecha_alta = ""
        self.fecha_baja = ""
        self.apellidos = ""
        self.nombre = ""
        self.email = ""
        self.movil = ""
        self.direccion = ""
        self.provincia = ""
        self.municipio = ""

    def loadFromPanel(self):
        self.dni = var.ui.txtDnicli.text()
        self.fecha_alta = var.ui.txtAltacli.text()
        self.fecha_baja = var.ui.txtBajacli.text()
        self.apellidos = var.ui.txtApelcli.text()
        self.nombre = var.ui.txtNomcli.text()
        self.email = var.ui.txtEmailcli.text()
        self.movil = var.ui.txtMovilcli.text()
        self.direccion = var.ui.txtDircli.text()
        self.provincia = var.ui.cmbProvcli.currentText()
        self.municipio = var.ui.cmbMunicli.currentText()

