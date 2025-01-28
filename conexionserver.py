from os.path import curdir

import mysql.connector
from mysql.connector import Error
import os
from PyQt6 import QtSql, QtWidgets

import var
import eventos


class ConexionServer():
    @staticmethod
    def crear_conexion():

        try:
            conexion = mysql.connector.connect(
            host='192.168.10.66', # Cambia esto a la IP de tu servidor user='dam', # Usuario creado
            user='dam',
            password='dam2425',
            database='bbdd',
            charset="utf8mb4",
            collation="utf8mb4_general_ci"  # Asegúrate de que aquí esté configurado
            # Contraseña del usuario database='bbdd' # Nombre de la base de datos
            )
            if conexion.is_connected():
                pass
                #print("Conexión exitosa a la base de datos")
            return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return None

    @staticmethod
    def listaProv(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()

        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    @staticmethod
    def listadoClientes():
        historico = var.ui.chkHistoriacli.isChecked()
        try:
            conexion = ConexionServer().crear_conexion()
            listadoclientes = []
            cursor = conexion.cursor()
            cursor.execute("SELECT dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli, bajacli FROM clientes ORDER BY apelcli, nomecli ASC")
            resultados = cursor.fetchall()
            # Procesar cada fila de los resultados
            for fila in resultados:
                # Crear una lista con los valores de la fila
                listadoclientes.append(list(fila))  # Convierte la tupla en una lista y la añade a listadoclientes
            if not historico:
                listadoclientes = [x for x in listadoclientes if x[9] is None or x[9] ==""]
            # Cerrar el cursor y la conexión si no los necesitas más
            cursor.close()
            conexion.close()
            return listadoclientes
        except Exception as e:
            print("error listado de clientes en conexión", e)

    @staticmethod
    def listadoTipoprop():
        tipos = []
        try:
            conexion = ConexionServer().crear_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT tipo FROM tipopropiedad order by tipo asc")
            resultados = cursor.fetchall()
            for fila in resultados:
                tipos.append(fila[0])
        except Exception as error:
            print("Error al cargar los tipos de propiedades", error)
        return tipos

    @staticmethod
    def listadoPropiedades():
        historico = var.ui.chkHistoriprop.isChecked()
        try:
            conexion = ConexionServer().crear_conexion()
            listadoPropiedades = []
            cursor = conexion.cursor()
            cursor.execute("SELECT codigo, muniprop, tipoprop, habprop, banprop, prealquiprop, prevenprop, tipooper, bajaprop FROM propiedades ORDER BY muniprop ASC")
            resultados = cursor.fetchall()
            for fila in resultados:
                listadoPropiedades.append(list(fila))
            if not historico:
                listadoPropiedades = [x for x in listadoPropiedades if x[8] is None or x[8] == ""]
            cursor.close()
            conexion.close()
            return listadoPropiedades
        except Exception as e:
            print("error listado de propiedades en conexión", e)

    @staticmethod
    def listadoPropiedadesFiltrado(tipo_propiedad, municipio, provincia):
        listado = []
        try:
            conexion = ConexionServer().crear_conexion()
            cursor = conexion.cursor()
            if var.ui.chkHistoriprop.isChecked():
                query = "SELECT codigo, muniprop, tipoprop, habprop, banprop, prealquiprop, prevenprop, tipooper, bajaprop FROM propiedades where tipoprop = %s and muniprop = %s and provprop = %s"
            else:
                query =" SELECT codigo, muniprop, tipoprop, habprop, banprop, prealquiprop, prevenprop, tipooper, bajaprop FROM propiedades where tipoprop = %s and muniprop = %s and provprop = %s and estadoprop = 'Disponible'"
            cursor.execute(query, (tipo_propiedad, municipio, provincia))
            resultados = cursor.fetchall()
            for fila in resultados:
                listado.append(list(fila))
            return listado
        except Exception as error:
            print("error listado de propiedades filtrado ", error)
            return False

    @staticmethod
    def datosOnePropiedad(codigo):
        registro = []
        try:
            conexion = ConexionServer().crear_conexion()
            cursor = conexion.cursor()
            query = "SELECT codigo, altaprop, bajaprop, cpprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, superprop, prealquiprop, prevenprop, obserprop, tipooper, estadoprop, nomeprop, movilprop FROM propiedades where codigo = %s"
            cursor.execute(query, (codigo,))
            # Recuperar los datos de la consulta
            for row in cursor.fetchall():
                registro.extend([str(col) for col in row])
            return registro
        except Exception as e:
            print("error listado de propiedades en conexión", e)

    @staticmethod
    def altaCliente(cliente):

        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO clientes (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, cliente)          # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()   # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    @staticmethod
    def altaPropiedad(propiedad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = "Insert into propiedades (altaprop, cpprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, superprop, prealquiprop, prevenprop, obserprop, nomeprop, movilprop, tipooper, estadoprop) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(query, propiedad)  # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Exception as error:
            print("Error al guardar la propiedad en la base de datos", error)
            return False



    @staticmethod
    def datosOneCliente(dni):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli, bajacli FROM clientes WHERE dnicli = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (dni,))  # Pasar 'dni' como una tupla
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
            return registro

        except Exception as e:
            print("Error al obtener datos de un cliente:", e)
            return None  # Devolver None en caso de error

    @staticmethod
    def modifCliente(cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                clienteReordenado = cliente[1:] + [cliente [0]]
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                UPDATE clientes 
                set altacli = %s, apelcli = %s, nomecli = %s, emailcli = %s, movilcli = %s, dircli = %s, provcli = %s, municli = %s, bajacli = %s where dnicli = %s
                """
                cursor.execute(query, clienteReordenado)
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Error as e:
            Eventos.mostrarMensajeError(e.msg)
            return False

    @staticmethod
    def bajaCliente(dni, fecha):
        try:
            conexion = ConexionServer.crear_conexion()
            if conexion:
                datos = (fecha, dni)
                cursor = conexion.cursor()
                query = """
                UPDATE clientes set bajacli = %s where dnicli = %s
                """
                cursor.execute(query, datos)
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            return False

    @staticmethod
    def modifPropiedad(propiedad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = "update propiedades set altaprop = %s, cpprop = %s, dirprop = %s, provprop =%s, muniprop = %s, tipoprop =%s, habprop =%s, banprop =%s, superprop =%s, prealquiprop =%s, prevenprop =%s, obserprop = %s, nomeprop = %s, movilprop =%s, tipooper =%s, estadoprop =%s, bajaprop = %s where codigo = %s"
                cursor.execute(query, propiedad)  # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Exception as error:
            print("Error al modificar la propiedad en la base de datos", error)
            return False

    @staticmethod
    def bajaPropiedad(codigo, fechabaja, disponibilidad):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = "update propiedades set bajaprop = %s, estadoprop =%s  where codigo = %s"
                cursor.execute(query, (fechabaja, disponibilidad, codigo))  #
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Exception as error:
            print("Error al dar de baja la propiedad en la base de datos", error)
            return False