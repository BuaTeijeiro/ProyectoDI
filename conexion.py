import os
from idlelib.query import Query
from time import localtime

from PyQt6 import QtSql, QtWidgets, QtGui, QtCore
from PyQt6.QtCore import QVariant

import var

class Conexion:
    '''

    método de una clase que no depende de una instancia específica de esa clase.
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase.
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.

    '''

    @staticmethod
    def db_conexion():
        """

        :return: conexion exitosa con la base de datos
        :rtype: bool

        Método para establecer conexión con la base de datos.
        Si éxito devuelve true, en caso contrario devuelve false.

        """
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
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
        """

        :return: lista de provincias
        :rtype: list

        Método que realiza query para obtener el listado de provincias en la base de datos

        """
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare("SELECT * FROM provincias")
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))
        return listaprov


    @staticmethod
    def listaMunicipios(provincia):
        """

        :param provincia: nombre provincia
        :type provincia: str
        :return: lista de municipios
        :rtype: bytearray

        Método que devuelve listado de municipios de una provincia

        """
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
        """

        :param nuevocli: datos del nuevo cliente
        :type nuevocli: list
        :return: éxito del registro
        :rtype: bool

        Método que registra en la base de datos un cliente con los datos del parámetro
        Devuelve true si se realiza correctamente, false en caso contrario

        """
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
        """

        :return: listado clientes
        :rtype: list

        Método que devuelve el listado de clientes, ordenados por apellido y nombre
        Filtra los dados de alta cuando corresponda

        """
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
        """

        :param dni: dni del cliente a cargar
        :type dni: str
        :return: datos del cliente
        :rtype: list

        Método que recupera los datos de un cliente a partir de su dni

        """
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
        """

        :param registro: datos del cliente a modificar
        :type registro: list
        :return: éxito de la operación
        :rtype: bool

        Método que actualiza en la base de la datos la información de un cliente que se pasa por parámetros
        Devuelve true si se realiza correctamente, false en caso contrario

        """
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
        """

        :param dni: dni del cliente a dar de baja
        :type dni: str
        :param fecha: fecha de baja del cliente
        :type fecha: str
        :return: éxito de la operación
        :rtype: bool

        Método que da de baja al usuario cuyo dni se pasa como parámetro con la fecha indicada
        No elimina al cliente de la base de datos
        Devuelve true si se realiza correctamente, false en caso contrario


        """
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
        """

        :return: listado de tipos de propiedad
        :rtype: list

        Método que devuelve una lista con los tipos de propiedades almacenados en la base de datos

        """
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
        """

        :param tipo: nombre del tipo de propiedad
        :type tipo: str
        :return: operacion exitosa
        :rtype: bool

        Método que añade el tipo de propiedad pasado por parámetro si no existe, devolviendo true
        Devuelve false si ya existe

        """
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
        """

        :param tipo: tipo de propiedad a eliminar
        :type tipo: str
        :return: operacion exitosa
        :rtype: bool

        Método que elimina el tipo de prop si existe, devolviendo true
        Devuelve false si no existe

        """
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
        """

        :param propiedad: datos de la propiedad a dar de alta
        :type propiedad: list
        :return: operacion exitosa
        :rtype: bool

        Método que da de alta una propiedad con los datos pasados por parámetro
        Devuelve true si la operación tiene lugar correctamente, false en caso contrario

        """
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
        """

        :return: lista de propiedades registradas
        :rtype: list

        Método que devuelve la lista de propiedades que existen en la base de datos
        con la información necesaria para mostrarlas en la tabla

        """
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
        """

        :return: listado de propiedades
        :rtype: list

        Método que devuelve la lista de propiedades que existen en la base de datos con toda su información

        """
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
        """

        :param tipo_propiedad: tipo de propiedad
        :type tipo_propiedad: str
        :param municipio: municipio de la propiedad
        :type municipio: str
        :param provincia: provincia de la propiedad
        :type provincia: str
        :return: listado de propiedades
        :rtype: list

        Método que devuelve la lista de propiedades filtradas por los criterios pasados por parámetro

        """
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
        """

        :param codigo: código identificador de una propiedad
        :type codigo: int
        :return: datos de la propiedad
        :rtype: list

        Método que devuelve la información de una propiedad a partir de su código identificativo

        """
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
        """

        :param propiedad: datos modificados de la propiedad
        :type propiedad: list
        :return: operacion existosa
        :rtype: bool

        Método que modifica los datos de la propiedad pasada por parámetros
        Devuelve true si la operación se realiza correctamente, false en caso contrario

        """
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
        """

        :param codigo: código de la propiedad a dar de baja
        :type codigo: int
        :param fechabaja: fecha de la baja
        :type fechabaja: str
        :param disponibilidad: disponibilidad de la propiedad
        :type disponibilidad: str
        :return: operación exitosa
        :rtype: bool

        Método da de baja a la propiedad del código especificado
        seteando la fecha y la disponibilidad pasado por parámetros
        No elimina al cliente de la base de datos
        devuelve true si la operación se realiza correctamente, false en caso contrario

        """
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
        """

        :param codigo: código de la propiedad a borrar
        :type codigo: int
        :return: operacion exitosa
        :rtype: bool

        Método que elimina de la base de datos la propiedad cuyo código se pasa por parámetro
        Devuelve true si se realiza correctamente, false en caso contrario

        """
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
        """

        :param nuevovend: datos del nuevo vendedor
        :type nuevovend: list
        :return: operacion exitosa
        :rtype: bool

        Método que graba un vendedor en la base de datos con la información del parámetro
        Devuelve true si se realiza correctamente, false en caso contrario

        """
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
        """

        :return: lista de vendedores
        :rtype: list

        Método que devuelve una lista con los datos de los vendedores de la base de datos

        """
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
        """

        :param id: id del vendedor a buscar
        :type id: int
        :return: datos de un vendedor
        :rtype: list

        Método que recupera de la base de datos la información del vendedor cuyo id es el pasado por parámetros

        """
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
        """

        :param movil: móvil del vendedor
        :type movil: str
        :return: id del vendedor
        :rtype: int

        Método que recupera el id de un cliente a partir de su móvil, pasado por parámetro

        """
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
        """

        :param modifvend: datos del vendedor a modificar
        :type modifvend: list
        :return: operacion exitosa
        :rtype: bool

        Método que modifica los datos de un cliente con los pasados por parámetros
        Devuelve true si se realiza correctamente, false en caso contrario

        """
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
        """

        :param id: id del vendedor a dar de baja
        :type id: int
        :param fecha: fecha de la baja del vendedor
        :type fecha: str
        :return: operacion exitosa
        :rtype: bool

        Método que da de baja al cliente especificado, seteando la fecha de baja pasada por parámtetro
        No elimina al cliente de la base de datos
        Devuelve true si se realiza correctamente, false en caso contrario

        """
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

    @staticmethod
    def guardarFActura(factura):
        """

        :param factura: datos de la nueva factura a guardar
        :type factura: list
        :return: operacion exitosa
        :rtype: bool

        Método que registra una nueva factura en la base de datos,
        con el dni del cliente y la fecha que se pasan por parámetros.
        Devuelve true si se realiza correctamente, false en caso contrario

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("insert into facturas(fechaven,dnicli) values (:fecha, :dnicli)")
            query.bindValue(":fecha", factura[0])
            query.bindValue(":dnicli", factura[1])
            if query.exec():
                return True
            else:
                return False
        except Exception as exec:
            print("Error al guardar la factura", exec)

    @staticmethod
    def getLastIdFactura():
        """

        :return: id de la última factura
        :rtype: int

        Método que devuelve el id de la última factura añadida a la base de datos

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select id from facturas order by id desc")
            if query.exec() and query.next():
                return query.value(0)
            else:
                print(query.lastError().text())
        except Exception as exec:
            print("Error al guardar la factura", exec)


    @staticmethod
    def listadoFacturas():
        """

        :return: lista de facturas
        :rtype: list

        Método que devuelve una lista con los datos de las facturas de la base de datos

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas")
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error al recuperar la lista de facturas")

    @staticmethod
    def datosOneFactura(id):
        """

        :param id: id de la factura
        :type id: int
        :return: datos de la factura
        :rtype: list

        Método que recupera una lista con los datos de la factura cuyo id es el pasado por parámetros

        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM facturas where id = :id")
            query.bindValue(":id", str(id))
            if query.exec() and query.next():
                registro = [query.value(i) for i in range(query.record().count())]
            return registro
        except Exception as error:
            print("Error al abrir el archivo")

    @staticmethod
    def deleteFactura(id):
        """

        :param id: id de la factura
        :type id: int
        :return: operacion exitosa
        :rtype: bool

        Método que elimina una factura de la base de datos
        primero llama al método de borrar las ventas asociadas a la factura
        y solo continúa con la operación si esta última es exitoso
        Devuelve true si se realiza correctamente, false en caso contrario

        """
        try:
            if Conexion.deleteVentasFactura(id):
                query = QtSql.QSqlQuery()
                query.prepare("Delete from facturas where id = :id")
                query.bindValue(":id", id)
                if query.exec():
                    return True
                else:
                    return False
            else:
                return False
        except Exception as error:
            return False
            print("Error al eliminar la factura")

    @staticmethod
    def deleteVentasFactura(idFactura):
        """

        :param idFactura: id de la factura
        :type idFactura: int
        :return: operacion exitosa
        :rtype: bool

        Método que elimina las ventas cuya factura es la correspondiente al id pasado por parámetros
        Devuelve true si se realiza correctamente, false en caso contrario

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("Delete from ventas where factura = :idFactura")
            query.bindValue(":idFactura", idFactura)
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error al eliminar las ventas de la factura")
            return False


    @staticmethod
    def grabarVenta(venta):
        """

        :param venta: datos de la venta a registrar
        :type venta: list
        :return: operacion exitosa
        :rtype: bool

        Método que registra una venta en la base de datos con los datos pasados por parámetro
        Devuelve true si se realiza correctamente, false en caso contrario

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("insert into ventas(factura, vendedor, propiedad) values (:idfactura, :idvendedor, :idpropiedad)")
            query.bindValue(":idfactura", venta[0])
            query.bindValue(":idvendedor", venta[1])
            query.bindValue(":idpropiedad", venta[2])
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error al grabar el venta")

    @staticmethod
    def eliminarVenta(idventa):
        """

        :param idventa: id de la venta a eliminar
        :type idventa: int
        :return: operacion exitosa
        :rtype: bool

        Método que elimina la venta de la base de datos cuyo id es el pasado por parámetro
        Devuelve true si se realiza correctamente, false en caso contrario

        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "delete from ventas where id = :idventa")
            query.bindValue(":idventa", idventa)
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error al grabar el venta")

    @staticmethod
    def listadoVentas(idFactura):
        """

        :param idFactura: id de la factura
        :type idFactura: int
        :return: lista de ventas de la factura
        :rtype: list

        Método que recupera la información de todas las ventas cuya factura es
        la identificada por el id pasado por parámetro

        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "select v.id, v.propiedad, p.direccion, p.municipio, p.tipo_propiedad, p.precio_venta from ventas as v inner join propiedades as p on v.propiedad = p.codigo where v.factura = :idFactura")
            query.bindValue(":idFactura", idFactura)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as error:
            print("Error al recuperar el listado de ventas")

    @staticmethod
    def totalFactura(idFactura):
        """

        :param idFactura: id de la Factura
        :type idFactura: int
        :return: precio total de la factura
        :rtype: float

        Método que calcula la suma del precio de todas las ventas asociadas a la factura
        identificada por el id que se pasa por parámetro

        """
        try:
            suma = 0
            query = QtSql.QSqlQuery()
            query.prepare(
                "select sum(p.precio_venta) from ventas as v inner join propiedades as p on v.propiedad = p.codigo where v.factura = :idFactura")
            query.bindValue(":idFactura", idFactura)
            if query.exec() and query.next():
                    return query.value(0)
            else:
                return None
        except Exception as error:
            print("Error al recuperar el costo de la factura: ", error)

    @staticmethod
    def venderPropiedad(codigo, fecha):
        """

        :param codigo: codigo de la propiedad a vender
        :type codigo: int
        :param fecha: fecha en la que se realiza la venta
        :type fecha: str
        :return: operacion exitosa
        :rtype: bool

        Método que actualiza la información de la propiedad identificada por el código pasado por parámetros
        seteando el estado a vendido y la fecha de baja según lo establecido en el parámetro
        Devuelve true si se realiza correctamente, false en caso contrario

        """
        try:
            query = QtSql.QSqlQuery()

            query.prepare("update propiedades set estado = 'Vendido', fechabaja=:fecha where codigo = :codigo")
            query.bindValue(":codigo", codigo)
            query.bindValue(":fecha", fecha)
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error al vender la propiedad:" , error)
            return False

    @staticmethod
    def liberarPropiedad(codigo):
        """

        :param codigo: codigo de la propiedad a liberar
        :type codigo: int
        :return: operacion exitosa
        :rtype: bool

        Método que actualiza la información de la propiedad identificada por el código pasado por parámetros
        seteando el estado a Disponible y la fecha de baja a null.
        Devuelve true si se realiza correctamente, false en caso contrario

        """
        try:
            query = QtSql.QSqlQuery()

            query.prepare("update propiedades set estado = 'Disponible', fechabaja=:fecha where codigo = :codigo")
            query.bindValue(":codigo", codigo)
            query.bindValue(":fecha", QtCore.QVariant())
            if query.exec():
                return True
            else:
                return False
        except Exception as error:
            print("Error al vender la propiedad:", error)
            return False