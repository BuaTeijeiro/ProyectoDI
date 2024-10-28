from datetime import datetime
from dlgCalendar import *
import var
import eventos
import propiedades
from dlgGestionProp import Ui_dlg_Tipoprop


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano,mes,dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)

class dlg_Tipoprop(QtWidgets.QDialog):
    def __init__(self):
        super(dlg_Tipoprop, self).__init__()
        self.interface = Ui_dlg_Tipoprop()
        self.interface.setupUi(self)
        self.interface.btnAnadirtipoprop.clicked.connect(propiedades.Propiedades.altaTipoPropiedad)
        self.interface.btnDeltipoprop.clicked.connect(propiedades.Propiedades.deleteTipoPropiedad)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

