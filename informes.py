from reportlab.pdfgen import canvas
from PIL import Image
from datetime import datetime
import os, shutil
import var

class Informes:
    @staticmethod
    def reportClientes():
        try:
            fecha = datetime.today().strftime("%Y_%m_%d%H_%M_%S")
            nomepdfcli = fecha + ".pdf"
            titulo = "Listado clientes"
            var.report = canvas.Canvas('informes/', nomepdfcli)
            items = ["DNI", "APELLIDOS", "NOMBRE", "MOVIL", "PROVINCIA", "MUNICIPIO"]
            Informes.topInforme(titulo)
            Informes.footInforme(titulo)
            var.report.setFont("Helvetica-Bold", size=10)
            var.report.drawString(50, 650, str(items[0]))
            var.report.drawString(120, 650, str(items[1]))
            var.report.drawString(170, 650, str(items[2]))
            var.report.drawString(285, 650, str(items[3]))
            var.report.drawString(390, 650, str(items[4]))
            var.report.drawString(460, 650, str(items[5]))
            var.report.line(50, 645, 525, 645)

            var.report.save()
            rootPath = ".\\informes\\"
            for file in os.listdir(rootPath):
                print(file.format())
                if file.endswith(nomepdfcli):
                    os.startfile('%s\\%s' % (rootPath, file))

        except Exception as error:
            print(error)


    def footInforme(titulo):
        try:
            total_pages = 0
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber()))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)

    def topInforme(titulo):
        try:
            ruta_logo = '.\\img\\lupa.ico'
            logo = Image.open(ruta_logo)

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                var.report.drawString(230, 670, titulo)
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