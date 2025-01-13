from datetime import datetime

import informes
from dlgAbout import Ui_dlgAbout
from dlgCalendar import *
import var
import eventos
import propiedades
from dlgGestionProp import Ui_dlg_Tipoprop
from dlgSelectMuni import Ui_DlgSelectMuni
from PyQt6 import QtSql


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

class dlg_About(QtWidgets.QDialog):
    def __init__(self):
        super(dlg_About, self).__init__()
        self.interface = Ui_dlgAbout()
        self.interface.setupUi(self)
        self.interface.btnCerrarAbout.clicked.connect(self.close)

class dlg_SelectMuni(QtWidgets.QDialog):
    def __init__(self):
        super(dlg_SelectMuni, self).__init__()
        self.ui = Ui_DlgSelectMuni()
        self.ui.setupUi(self)
        self.ui.btnGenerar.clicked.connect(lambda: dlg_SelectMuni.salir(self))
        self.muni = dlg_SelectMuni.getAllMunicipios()
        self.ui.cmbMunicipio.addItems(self.muni)
        self.ui.cmbMunicipio.setEnabled(True)
        completer = QtWidgets.QCompleter(self.muni, self.ui.cmbMunicipio)
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchFlag.MatchContains)
        self.ui.cmbMunicipio.setCompleter(completer)
        self.ui.cmbMunicipio.lineEdit().editingFinished.connect(lambda: dlg_SelectMuni.checkMunicipio(self))

    @staticmethod
    def getAllMunicipios():
        try:
            listamunicipios = [""]
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT municipio FROM municipios order by municipio")
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(0))
            return listamunicipios
        except Exception as e:
            print("Error al abrir el archivo")

    def checkMunicipio(self):
        if self.ui.cmbMunicipio.currentText() not in self.muni:
            self.ui.cmbMunicipio.setCurrentIndex(0)

    def salir(self):
        municipio = self.ui.cmbMunicipio.currentText()
        informes.Informes.reportPropiedades(municipio)
        self.close()

