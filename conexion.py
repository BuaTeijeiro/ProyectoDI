import os
from idlelib.query import Query

from PyQt6 import QtSql, QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QVariant

import eventos
import var

class Conexion:
    '''

    método de una clase que no depende de una instancia específica de esa clase.
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase.
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.

    '''

    @staticmethod
    def db_conexion():
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    """
    GESTIÓN PROVINCIAS Y MUNICIPIOS
    """

    @staticmethod
    def listaProv():
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov


    @staticmethod
    def listaMunicipios(provincia):
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT municipio FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(0))
            return listamunicipios
        except Exception as e:
            print("Error al abrir el archivo")

    """
    GESTIÓN CLIENTES
    """

    @staticmethod
    def altaCliente(nuevocli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT into clientes (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli) values (:dnicli, :altacli, :apelcli, :nomecli, :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevocli[0]))
            query.bindValue(":altacli", str(nuevocli[1]))
            query.bindValue(":apelcli", str(nuevocli[2]))
            query.bindValue(":nomecli", str(nuevocli[3]))
            query.bindValue(":emailcli", str(nuevocli[4]))
            query.bindValue(":movilcli", str(nuevocli[5]))
            query.bindValue(":dircli", str(nuevocli[6]))
            query.bindValue(":provcli", str(nuevocli[7]))
            query.bindValue(":municli", str(nuevocli[8]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error alta cliente", e)

    @staticmethod
    def listadoClientes():
        try:
            listado = []
            historico = var.ui.chkHistoriacli.isChecked()
            if (historico):
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes order by apelcli, nomecli ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes where bajacli is null order by apelcli, nomecli ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error al abrir el archivo")

    @staticmethod
    def datosOneCliente(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM clientes where dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                query.next()
                registro = [query.value(i) for i in range(query.record().count())]
            return registro
        except Exception as error:
            print("Error al abrir el archivo")

    @staticmethod
    def modifCliente(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE clientes SET altacli = :altacli, apelcli = :apelcli, nomecli = :nomecli, emailcli = :emailcli, movilcli =:movilcli, dircli =:dircli, provcli = :provcli, municli = :municli, bajacli =:bajacli where dnicli = :dni")
            query.bindValue(":dni", str(registro[0]))
            query.bindValue(":altacli", str(registro[1]))
            query.bindValue(":apelcli", str(registro[2]))
            query.bindValue(":nomecli", str(registro[3]))
            query.bindValue(":emailcli", str(registro[4]))
            query.bindValue(":movilcli", str(registro[5]))
            query.bindValue(":dircli", str(registro[6]))
            query.bindValue(":provcli", str(registro[7]))
            query.bindValue(":municli", str(registro[8]))
            if registro[9] == "":
                query.bindValue(":bajacli", QtCore.QVariant())
            else:
                query.bindValue(":bajacli", str(registro[9]))
            if query.exec() and query.numRowsAffected() == 1:
                return True
            else:
                return False
        except Exception as error:
            print("Error al modificar cliente en la base de datos")

    @staticmethod
    def bajaCliente(dni, fecha):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Select bajacli from clientes where dnicli = :dni")
            query.bindValue(":dni", str(dni))
            query.exec()
            if query.next() and query.value(0) == "" :
                print(query.value(0))
                query.prepare("UPDATE clientes SET bajacli = :bajacli where dnicli = :dni")
                query.bindValue(":dni", str(dni))
                query.bindValue(":bajacli", str(fecha))
                if query.exec() and query.numRowsAffected() == 1:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as exec:
            print("Error al registrar la baja del cliente")

    """
    GESTIÓN PROPIEDADES
    """

    @staticmethod
    def listadoTipoprop():
        tipos = []
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT tipo FROM tipoprop order by tipo asc")
            query.exec()
            while query.next():
                tipos.append(query.value(0))
            return tipos

        except Exception as error:
            print("Error al cargar los tipos de propiedades")

    @staticmethod
    def anadirTipoprop(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Insert into tipoprop (tipo) values (:tipo) ")
            query.bindValue(":tipo", str(tipo))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error al guardar el tipo de vivienda en la base de datos")

    @staticmethod
    def eliminarTipoprop(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM tipoprop WHERE tipo = :tipo")
            query.bindValue(":tipo", str(tipo).title())
            if query.exec() and query.numRowsAffected() == 1:
                return True
            else:
                return False
        except Exception as error:
            print("Error al eliminar el tipo de propiedad")

    @staticmethod
    def altaPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Insert into propiedades (fecha_publicacion, codigo_postal, direccion, provincia, municipio, tipo_propiedad, num_habitaciones, num_banos, superficie, precio_alquiler, precio_venta, observaciones, tipo_operacion, estado, nombre_propietario, movil) values (:fecha_publicacion, :codigo_postal, :direccion, :provincia, :municipio, :tipo_propiedad, :num_habitaciones, :num_banos, :superficie, :precio_alquiler, :precio_venta, :observaciones, :tipo_operacion, :estado, :nombre_propietario, :movil)")
            query.bindValue(":fecha_publicacion", str(propiedad[0]))
            query.bindValue(":codigo_postal", str(propiedad[1]))
            query.bindValue(":direccion", str(propiedad[2]))
            query.bindValue(":provincia", str(propiedad[3]))
            query.bindValue(":municipio", str(propiedad[4]))
            query.bindValue(":tipo_propiedad", str(propiedad[5]))
            query.bindValue(":num_habitaciones", str(propiedad[6]))
            query.bindValue(":num_banos", str(propiedad[7]))
            query.bindValue(":superficie", str(propiedad[8]))
            query.bindValue(":precio_alquiler", str(propiedad[9]))
            query.bindValue(":precio_venta", str(propiedad[10]))
            query.bindValue(":observaciones", str(propiedad[11]))
            query.bindValue(":tipo_operacion", ",".join(propiedad[14]))
            query.bindValue(":estado", str(propiedad[15]))
            query.bindValue(":nombre_propietario", str(propiedad[12]))
            query.bindValue(":movil", str(propiedad[13]))
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error al guardar la propiedad en la base de datos")

    @staticmethod
    def listadoPropiedades():
        try:
            listado = []
            query = QtSql.QSqlQuery()
            if var.ui.btnBuscaprop.isChecked():
                query.prepare("SELECT codigo, municipio, tipo_propiedad, num_habitaciones, num_banos, precio_alquiler, precio_venta, tipo_operacion, fechabaja FROM propiedades where tipo_propiedad = :tipo_propiedad order by municipio")
                query.bindValue(":tipo_propiedad", var.ui.cmbTipoprop.currentText())
            else:
                query.prepare("SELECT codigo, municipio, tipo_propiedad, num_habitaciones, num_banos, precio_alquiler, precio_venta, tipo_operacion, fechabaja FROM propiedades order by municipio")
            if query.exec():
                while query.next():
                    listado.append([query.value(i) for i in range(query.record().count())])

            if not var.ui.chkHistoriprop.isChecked():
                listado = [registro for registro in listado if registro[8] == ""]
            return listado
        except Exception as error:
            print("Error al cargar las propiedades", error)

    @staticmethod
    def datosOnePropiedad(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades where codigo = :codigo")
            query.bindValue(":codigo", codigo)
            if query.exec() and query.next():
                registro = [query.value(i) for i in range(query.record().count())]
            return registro
        except Exception as error:
            print("Error al cargar los datos de la propiedad", error)

    @staticmethod
    def modifPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "Update propiedades set fecha_publicacion = :fecha_publicacion,fechabaja =:fechabaja, codigo_postal = :codigo_postal, direccion = :direccion, provincia= :provincia, municipio = :municipio, tipo_propiedad =:tipo_propiedad, num_habitaciones = :num_habitaciones, num_banos = :num_banos, superficie =:superficie, precio_alquiler=:precio_alquiler, precio_venta = :precio_venta, observaciones =:observaciones, tipo_operacion = :tipo_operacion, estado = :estado, nombre_propietario = :nombre_propietario, movil=:movil where codigo = :codigo")
            query.bindValue(":fecha_publicacion", str(propiedad[0]))
            query.bindValue(":codigo_postal", str(propiedad[1]))
            query.bindValue(":direccion", str(propiedad[2]))
            query.bindValue(":provincia", str(propiedad[3]))
            query.bindValue(":municipio", str(propiedad[4]))
            query.bindValue(":tipo_propiedad", str(propiedad[5]))
            query.bindValue(":num_habitaciones", str(propiedad[6]))
            query.bindValue(":num_banos", str(propiedad[7]))
            query.bindValue(":superficie", str(propiedad[8]))
            query.bindValue(":precio_alquiler", str(propiedad[9]))
            query.bindValue(":precio_venta", str(propiedad[10]))
            query.bindValue(":observaciones", str(propiedad[11]))
            query.bindValue(":tipo_operacion", ",".join(propiedad[14]))
            query.bindValue(":estado", str(propiedad[15]))
            query.bindValue(":nombre_propietario", str(propiedad[12]))
            query.bindValue(":movil", str(propiedad[13]))
            query.bindValue(":fechabaja", str(propiedad[16]))
            query.bindValue(":codigo", str(propiedad[17]))
            if query.exec() and query.numRowsAffected() == 1:
                print(query.lastError().text())
                return True
            else:
                print(query.lastError().text())
                return False
        except Exception as error:
            print("Error al guardar la propiedad en la base de datos")

    @staticmethod
    def bajaPropiedad(codigo, fechabaja):
        query = QtSql.QSqlQuery()
        query.prepare("Update propiedades set fechabaja = :fechabaja where codigo = :codigo")
        query.bindValue(":fechabaja", fechabaja)
        query.bindValue(":codigo", codigo)
        if query.exec() and query.numRowsAffected() == 1:
            return True
        else:
            return False

    @staticmethod
    def deletePropiedad(codigo):
        query = QtSql.QSqlQuery()
        query.prepare("DELETE from propiedades where codigo = :codigo")
        query.bindValue(":codigo", codigo)
        if query.exec():
            return True
        else:
            return False
