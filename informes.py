import math

from reportlab.pdfgen import canvas
from PIL import Image
from datetime import datetime
from PyQt6 import QtSql
import os, shutil
import var


class Informes:
    @staticmethod
    def reportClientes():
        xdni = 55
        xapelcli = 100
        xnomecli = 220
        xmovilcli = 325
        xprovcli = 385
        xmunicli = 450
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
                print(total_clientes)
                total_pages = Informes.getNumberPages(total_clientes, ymax, ymin, ystep)
                print(total_pages)
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
            print(error)

    @staticmethod
    def getNumberPages(amount, ymax, ymin, ystep):
        number_per_page = math.ceil((ymax - ymin)/ystep)
        print(number_per_page)
        return math.ceil(amount / number_per_page)

    @staticmethod
    def footInforme(titulo, pages):
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
            print('Error en pie informe de cualquier tipo: ', error)

    @staticmethod
    def topInforme(titulo):
        try:
            ruta_logo = '.\\img\\logo.png'
            logo = Image.open(ruta_logo)

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                var.report.drawString(230, 682, titulo)
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
            print('Error en cabecera informe:', error)

if __name__ == '__main__':
    Informes.reportClientes()