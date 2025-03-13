import math
from idlelib import query

from pyexpat import features
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import datetime
from PyQt6 import QtSql
import os, shutil
import traceback

from sphinx.util.exceptions import format_exception_cut_frames

import conexion
import var
from logger import Logger
from model.month import Month


class Informes:
    @staticmethod
    def reportClientes():
        """

        Método que genera un informe con los datos de los clientes existentes

        """
        xdni = 55
        xapelcli = 100
        xnomecli = 220
        xmovilcli = 325
        xprovcli = 405
        xmunicli = 460
        ymax = 630
        ymin = 90
        ystep = 30
        try:
            rootPath = ".\\informes"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            print(pdf_path)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado clientes"
            query = QtSql.QSqlQuery()
            query.prepare("SELECT dnicli, apelcli, nomecli, movilcli, provcli, municli FROM clientes order by apelcli")
            queryCount = QtSql.QSqlQuery()
            queryCount.prepare("Select count(*) from clientes")
            if query.exec() and queryCount.exec() and queryCount.next():
                total_clientes = queryCount.value(0)
                total_pages = Informes.getNumberPages(total_clientes, ymax, ymin, ystep)
                Informes.topInforme(titulo)
                Informes.footInforme(titulo, total_pages)
                items = ["DNI", "APELLIDOS", "NOMBRE", "MOVIL", "PROVINCIA", "MUNICIPIO"]
                var.report.setFont("Helvetica-Bold", size=10)

                var.report.drawString(xdni, 650, str(items[0]))
                var.report.drawString(xapelcli, 650, str(items[1]))
                var.report.drawString(xnomecli, 650, str(items[2]))
                var.report.drawString(xmovilcli, 650, str(items[3]))
                var.report.drawString(xprovcli, 650, str(items[4]))
                var.report.drawString(xmunicli, 650, str(items[5]))
                var.report.line(50, 645, 525, 645)

                y = ymax
                while query.next():
                    if y<= ymin:
                        var.report.drawString(450, 80, "Página siguiente...")
                        var.report.showPage()
                        Informes.footInforme(titulo, total_pages)
                        Informes.topInforme(titulo)
                        var.report.setFont("Helvetica-Bold", size=10)
                        var.report.drawString(xdni, 650, str(items[0]))
                        var.report.drawString(xapelcli, 650, str(items[1]))
                        var.report.drawString(xnomecli, 650, str(items[2]))
                        var.report.drawString(xmovilcli, 650, str(items[3]))
                        var.report.drawString(xprovcli, 650, str(items[4]))
                        var.report.drawString(xmunicli, 650, str(items[5]))
                        var.report.line(50, 645, 525, 645)
                        y = ymax

                    var.report.setFont("Helvetica", size=8)
                    dni = "***" + str(query.value(0))[3:6] + "***"
                    var.report.drawCentredString(xdni + 6, y, str(dni))
                    var.report.drawString(xapelcli, y, str(query.value(1)).title())
                    var.report.drawString(xnomecli, y, str(query.value(2)).title())
                    var.report.drawString(xmovilcli -3, y, str(query.value(3)).title())
                    var.report.drawString(xprovcli, y, str(query.value(4)).title())
                    var.report.drawString(xmunicli, y, str(query.value(5)).title())
                    y -= ystep



            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)

        except Exception as error:
            Logger.log("Error", "Error al generar el informe de clientes" + str(error))

    @staticmethod
    def reportPropiedades(municipio):
        """

        :param municipio: nombre del municipio
        :type municipio: str

        Método que genera un informe con el listado de propiedades del municipio pasado por parámetros

        """
        xcod = 55
        xdireccion = 100
        xtipo= 250
        xoperacion = 325
        xprecioalquiler = 405
        xprecioventa = 475
        ymax = 630
        ymin = 90
        ystep = 30
        try:
            rootPath = ".\\informes"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfcli = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            print(pdf_path)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado propiedades de " + municipio
            queryCount = QtSql.QSqlQuery()
            query = QtSql.QSqlQuery()
            queryCount.prepare("SELECT count(*) FROM propiedades where municipio =:municipio")
            queryCount.bindValue(":municipio", municipio)
            query.prepare("SELECT * FROM propiedades where municipio =:municipio")
            query.bindValue(":municipio", municipio)

            if query.exec() and queryCount.exec() and queryCount.next():
                total_muni = queryCount.value(0)
                total_pages = Informes.getNumberPages(total_muni, ymax, ymin, ystep)
                Informes.topInforme(titulo)
                Informes.footInforme(titulo, total_pages)
                items = ["COD.","Direccion","TIPO","ALQUILER", "VENTA","OPERACIÓN"]
                var.report.setFont("Helvetica-Bold", size=10)

                var.report.drawString(xcod, 650, str(items[0]))
                var.report.drawString(xdireccion, 650, str(items[1]))
                var.report.drawString(xtipo, 650, str(items[2]))
                var.report.drawString(xprecioalquiler, 650, str(items[3]))
                var.report.drawString(xprecioventa, 650, str(items[4]))
                var.report.drawString(xoperacion, 650, str(items[5]))
                var.report.line(50, 645, 525, 645)

                y = ymax
                while query.next():
                    if y <= ymin:
                        var.report.drawString(450, 80, "Página siguiente...")
                        var.report.showPage()
                        Informes.footInforme(titulo, total_pages)
                        Informes.topInforme(titulo)
                        var.report.setFont("Helvetica-Bold", size=10)
                        var.report.drawString(xcod, 650, str(items[0]))
                        var.report.drawString(xdireccion, 650, str(items[1]))
                        var.report.drawString(xtipo, 650, str(items[2]))
                        var.report.drawString(xprecioalquiler, 650, str(items[3]))
                        var.report.drawString(xprecioventa, 650, str(items[4]))
                        var.report.drawString(xoperacion, 650, str(items[5]))
                        var.report.line(50, 645, 525, 645)
                        y = ymax

                    var.report.setFont("Helvetica", size=8)
                    var.report.drawString(xcod + 6, y, str(query.value(0)))
                    var.report.drawString(xdireccion, y, str(query.value(4)))
                    var.report.drawString(xtipo, y, str(query.value(7)))
                    precio_alquiler = "-" if not query.value(11) else str(query.value(11))
                    precio_venta = "-" if not query.value(12) else str(query.value(12))
                    var.report.drawRightString(xprecioalquiler + 50, y, precio_alquiler + " €")
                    var.report.drawRightString(xprecioventa + 33, y, precio_venta + " €")
                    var.report.drawString(xoperacion, y, str(query.value(14)))
                    y -= ystep

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)

        except Exception as error:
            Logger.log("Error", "Error al generar el informe de propiedades" + str(error))

    @staticmethod
    def facturaVenta(id):
        """

        :param id: id de la factura
        :type id: int

        Método que genera la factura de la venta identificada por el id pasado por parámetros

        """
        xidventa = 55
        xidpropiedad = xidventa + 35
        xdireccion = xidpropiedad + 50
        xlocalidad = xdireccion + 150
        xtipo = xlocalidad + 100
        xprecio = xtipo + 50
        ymax = 630
        ymin = 90
        ystep = 30
        try:
            rootPath = ".\\facturas"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfcli = id + "_factura_" + fecha + ".pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            print(pdf_path)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Factura Código " + id
            listado_ventas = conexion.Conexion.listadoVentas(id)
            factura = conexion.Conexion.datosOneFactura(id)
            cliente = conexion.Conexion.datosOneCliente(factura[2])
            Informes.topInforme(titulo)
            Informes.topDatosCliente(cliente, factura[1])
            Informes.footInforme(titulo,1)
            items = ["Venta", "Código", "Direccion", "Localidad", "Tipo", "Precio"]
            var.report.setFont("Helvetica-Bold", size=10)
            var.report.drawString(xidventa, 650, str(items[0]))
            var.report.drawString(xidpropiedad, 650, str(items[1]))
            var.report.drawString(xdireccion, 650, str(items[2]))
            var.report.drawString(xlocalidad, 650, str(items[3]))
            var.report.drawString(xtipo, 650, str(items[4]))
            var.report.drawString(xprecio, 650, str(items[5]))
            var.report.line(50, 645, 525, 645)
            y = ymax
            for registro in listado_ventas:
                var.report.setFont("Helvetica", size=8)
                var.report.drawCentredString(xidventa + 10, y, str(registro[0]))
                var.report.drawCentredString(xidpropiedad + 15, y, str(registro[1]).title())
                var.report.drawString(xdireccion, y, str(registro[2]).title())
                var.report.drawString(xlocalidad, y, str(registro[3]).title())
                var.report.drawString(xtipo, y, str(registro[4]).title())
                var.report.drawCentredString(xprecio + 22, y, str(registro[5]).title() + " €")
                y -= ystep

            xmenuinferior = 400
            xtotal = 450
            var.report.line(50, 170, 525, 170)
            y = 140
            subtotal = int(conexion.Conexion.totalFactura(id))
            iva = 10 * subtotal / 100
            total = subtotal + iva
            var.report.setFont("Helvetica-Bold", size=9)
            var.report.drawString(xmenuinferior, y, "Subtotal")
            var.report.setFont("Helvetica", size=9)
            var.report.drawString(xtotal, y, f"{subtotal:,.2f}" + " €")
            y -= ystep
            var.report.setFont("Helvetica-Bold", size=9)
            var.report.drawString(xmenuinferior, y, "Impuestos")
            var.report.setFont("Helvetica", size=9)
            var.report.drawString(xtotal, y, f"{iva:,.2f}" + " €")
            y -= ystep
            var.report.setFont("Helvetica-Bold", size=9)
            var.report.drawString(xmenuinferior, y, "Total")
            var.report.setFont("Helvetica", size=9)
            var.report.drawString(xtotal, y, f"{total:,.2f}" + " €")
            y -= ystep

            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)

        except Exception as error:
            Logger.log("Error", "Error al generar la factura de la venta" + str(error))

    @staticmethod
    def reciboMensualidad(mensualidad):
        """

        :param mensualidad: id de la mensualidad
        :type mensualidad: int

        Método que genera el recibo de un pago de una mensualidad

        """
        try:
            rootPath = ".\\recibosAlquiler"
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            mes = mensualidad[2]
            anno = mensualidad[3]
            nomepdfcli = "alquiler_" + str(mensualidad[1])  + "_recibo_" + str(mes) + str(anno) + ".pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            print(pdf_path)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Recibo Alquiler Mensualidad"
            alquiler = conexion.Conexion.datosOneAlquiler(mensualidad[1])
            cliente = conexion.Conexion.datosOneCliente(alquiler[2])
            propiedad = conexion.Conexion.datosOnePropiedad(alquiler[1])
            Informes.topInforme(titulo)
            Informes.topDatosCliente(cliente, "")
            Informes.footInforme(titulo, 1)
            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 600, 'Propiedad: ' + str(propiedad[0]))
            var.report.drawString(55, 580, 'Dirección: ' + str(propiedad[4]))
            var.report.drawString(55, 560, 'Localidad: ' + str(propiedad[6]))
            var.report.drawString(55, 540, 'Provincia: ' + str(propiedad[5]))
            var.report.drawString(355, 600, 'Fecha Mensualidad: ' + "1-"+str(mes)+"-"+str(anno))
            var.report.drawString(355, 580, 'Contrato nº: ' + str(alquiler[0]))
            var.report.drawString(355, 560, 'Recibo nº: ' + str(mensualidad[0]))
            var.report.drawString(355, 540, 'Precio Alquiler: ' + str(propiedad[11]) + " €")
            estado = "pagado" if mensualidad[4] else "no pagado"
            var.report.drawString(355, 520, 'Estado: ' + estado)

            var.report.line(50, 170, 525, 170)


            var.report.save()

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)

        except Exception as error:
            Logger.log("Error", "Error al general el recibo de la mensualidad" + str(error))


    @staticmethod
    def getNumberPages(amount, ymax, ymin, ystep):
        """

        :param amount: cantidad total de elementos
        :type amount: int
        :param ymax: posicion inicial de la lista en el informe
        :type ymax: int
        :param ymin: posicion final de la lista en el informe
        :type ymin: int
        :param ystep: tamano de cada elemento de la lista
        :type ystep: int
        :return: numero de paginas necesarias
        :rtype: int

        Método que calcula la cantidad de páginas necesarias en un informe, teniendo en cuenta
        como se muestran por pantalla, según lo recogido en los parámetros.

        """
        number_per_page = math.ceil((ymax - ymin)/ystep)
        return math.ceil(amount / number_per_page)

    @staticmethod
    def footInforme(titulo, pages):
        """

        :param titulo: titulo del informe
        :type titulo: str
        :param pages: numero de paginas necesarias
        :type pages: int

        Método que dibuja el pie de pagina en el informe guardado en var.informe

        """
        try:
            total_pages = 0
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s/%s' % (var.report.getPageNumber(), pages)))

        except Exception as error:
            Logger.log("Error", "Error en el pie del informe" + str(error))

    @staticmethod
    def topInforme(titulo):
        """

        :param titulo: titulo del informe
        :type titulo: str

        Método que dibuja la cabecera del informe

        """
        try:
            ruta_logo = '.\\img\\logo.png'
            logo = Image.open(ruta_logo)

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                var.report.drawCentredString(300, 682, titulo)
                var.report.line(50, 665, 525, 665)

                # Dibuja la imagen en el informe
                var.report.drawImage(ruta_logo, 480, 725, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 770, 'CIF: A12345678')
                var.report.drawString(55, 755, 'Avda. Galicia - 101')
                var.report.drawString(55, 740, 'Vigo - 36216 - España')
                var.report.drawString(55, 725, 'Teléfono: 986 132 456')
                var.report.drawString(55, 710, 'e-mail: cartesteisr@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo}')
        except Exception as error:
            Logger.log("Error", "Error en la cabecera del informe" + str(error))

    @staticmethod
    def topDatosCliente(cliente, fecha):
        """

        :param cliente: datos del cliente
        :type cliente: list
        :param fecha: fecha del informe
        :type fecha: str

        Método que añade la información del cliente a la cabecera del informe

        """
        try:
            var.report.setFont('Helvetica-Bold', size=8)
            var.report.drawString(300, 770, 'DNI Cliente:')
            var.report.drawString(300, 752, 'Nombre:')
            var.report.drawString(300, 734, 'Dirección:')
            var.report.drawString(300, 716, 'Localidad:')
            
            var.report.setFont('Helvetica', size=8)
            var.report.drawString(360, 770, cliente[0])
            var.report.drawString(360, 752, cliente[3] + " " +cliente[2])
            var.report.drawString(360, 734, cliente[6])
            var.report.drawString(360, 716, cliente[8])
            if fecha:
                var.report.drawString(55, 682, "Fecha Factura:")
                var.report.drawString(120, 682, fecha)
        except Exception as error:
            Logger.log("Error", "Error en los datos del cliente en la cabecera del informe" + str(error))

if __name__ == '__main__':
    Informes.reportClientes()