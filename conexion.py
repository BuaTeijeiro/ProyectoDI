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
            if query.exec() and query.next():
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
            query.bindValue(":tipo_operacion", str(propiedad[14]))
            query.bindValue(":estado", str(propiedad[15]))
            query.bindValue(":nombre_propietario", str(propiedad[12]))
            query.bindValue(":movil", str(propiedad[13]))
            if query.exec():
                var.lastid = query.lastInsertId()
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
    def listadoPropiedadesAllData():
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT * FROM propiedades order by municipio")
            if query.exec():
                while query.next():
                    listado.append([query.value(i) for i in range(query.record().count())])
            return listado
        except Exception as error:
            print("Error al cargar las propiedades", error)

    @staticmethod
    def listadoPropiedadesFiltrado(tipo_propiedad, municipio, provincia):
        listado = []
        query = QtSql.QSqlQuery()
        if var.ui.chkHistoriprop.isChecked():
            query.prepare(
                "SELECT codigo, municipio, tipo_propiedad, num_habitaciones, num_banos, precio_alquiler, precio_venta, tipo_operacion, fechabaja FROM propiedades where tipo_propiedad = :tipo_propiedad and municipio = :municipio and provincia = :provincia")
            query.bindValue(":tipo_propiedad", tipo_propiedad)
            query.bindValue(":municipio", municipio)
            query.bindValue(":provincia", provincia)
        else:
            query.prepare("SELECT codigo, municipio, tipo_propiedad, num_habitaciones, num_banos, precio_alquiler, precio_venta, tipo_operacion, fechabaja FROM propiedades where tipo_propiedad = :tipo_propiedad and municipio = :municipio and provincia = :provincia and estado = :estado")
            query.bindValue(":tipo_propiedad", tipo_propiedad)
            query.bindValue(":municipio", municipio)
            query.bindValue(":provincia", provincia)
            query.bindValue(":estado", "Disponible")
        if query.exec():
            while query.next():
                listado.append([query.value(i) for i in range(query.record().count())])
        return listado


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
            query.bindValue(":tipo_operacion", str(propiedad[14]))
            query.bindValue(":estado", str(propiedad[15]))
            query.bindValue(":nombre_propietario", str(propiedad[12]))
            query.bindValue(":movil", str(propiedad[13]))
            if propiedad[16]=="":
                query.bindValue(":fechabaja", QtCore.QVariant())
            else:
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
    def bajaPropiedad(codigo, fechabaja, disponibilidad):
        query = QtSql.QSqlQuery()
        query.prepare("Update propiedades set fechabaja = :fechabaja, estado =:estado where codigo = :codigo")
        query.bindValue(":fechabaja", fechabaja)
        query.bindValue(":codigo", codigo)
        query.bindValue(":estado", disponibilidad)
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

    #Metodos Examen
    @staticmethod
    def altaVendedor(nuevovend):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT into vendedores (dniVendedor,nombreVendedor, altaVendedor, movilVendedor, mailVendedor,delegacionVendedor) values (:dniVendedor, :nombreVendedor, :altaVendedor, :movilVendedor, :mailVendedor, :delegacionVendedor)")
            query.bindValue(":dniVendedor", str(nuevovend[0]))
            query.bindValue(":nombreVendedor", str(nuevovend[1]))
            if str(nuevovend[2])=="":
                query.bindValue(":altaVendedor", QtCore.QVariant())
            else:
                query.bindValue(":altaVendedor", str(nuevovend[2]))
            query.bindValue(":movilVendedor", str(nuevovend[3]))
            if (str(nuevovend[4])==""):
                query.bindValue(":mailVendedor", QtCore.QVariant())
            else:
                query.bindValue(":mailVendedor", str(nuevovend[4]))
            query.bindValue(":delegacionVendedor", str(nuevovend[5]))

            if query.exec():
                return True
            else:
                return False

        except Exception as e:
            print("Error alta vendedor", e)

    @staticmethod
    def listadoVendedores():
        try:
            listado = []
            historico = var.ui.chkHistoriavend.isChecked()
            if (historico):
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM vendedores order by idVendedor ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            else:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM vendedores where bajaVendedor is null order by idVendedor ASC")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error al abrir el archivo")

    @staticmethod
    def datosOneVendedor(id):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores where idVendedor = :idVendedor")
            query.bindValue(":idVendedor", str(id))
            if query.exec() and query.next():
                registro = [query.value(i) for i in range(query.record().count())]
            return registro
        except Exception as error:
            print("Error al abrir el archivo")

    @staticmethod
    def getIdVendedor(movil):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT idVendedor FROM vendedores where movilVendedor = :movilVendedor")
            query.bindValue(":movilVendedor", str(movil))
            if query.exec() and query.next():
                id = query.value(0)
                return id
            else:
                return False
        except Exception as error:
            print("Error al abrir el archivo")

    @staticmethod
    def modifVendedor(modifvend):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "update vendedores  set nombreVendedor = :nombreVendedor, altaVendedor = :altaVendedor,bajaVendedor =:bajaVendedor, movilVendedor = :movilVendedor, mailVendedor =:mailVendedor, delegacionVendedor =:delegacionVendedor where idVendedor = :idVendedor")
            query.bindValue(":nombreVendedor", str(modifvend[0]))
            if str(modifvend[1]) == "":
                query.bindValue(":altaVendedor", QtCore.QVariant())
            else:
                query.bindValue(":altaVendedor", str(modifvend[1]))
            if str(modifvend[2]) == "":
                query.bindValue(":bajaVendedor", QtCore.QVariant())
            else:
                query.bindValue(":bajaVendedor", str(modifvend[2]))
            query.bindValue(":movilVendedor", str(modifvend[3]))
            if (str(modifvend[4]) == ""):
                query.bindValue(":mailVendedor", QtCore.QVariant())
            else:
                query.bindValue(":mailVendedor", str(modifvend[4]))
            query.bindValue(":delegacionVendedor", str(modifvend[5]))
            query.bindValue(":idVendedor", int(modifvend[6]))

            if query.exec():
                return True
            else:
                print(query.lastError().text())
                return False

        except Exception as e:
            print("Error alta vendedor", e)

    @staticmethod
    def bajaVendedor(id, fecha):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Select bajaVendedor from vendedores where  idVendedor= :idVendedor")
            query.bindValue(":idVendedor", int(id))
            query.exec()
            if query.next() and query.value(0) == "":
                query.prepare("UPDATE vendedores SET bajaVendedor = :bajaVendedor where idVendedor = :idVendedor")
                query.bindValue(":idVendedor", int(id))
                query.bindValue(":bajaVendedor", str(fecha))
                if query.exec() and query.numRowsAffected() == 1:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as exec:
            print("Error al registrar la baja del cliente")
