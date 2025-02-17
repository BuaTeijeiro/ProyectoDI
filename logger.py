

import eventos
from datetime import datetime



class Logger(object):

    @staticmethod
    def log(messageType, mensaje):
        try:
            with open('logs/message.log', 'a', encoding='utf-8') as f:
                now = datetime.now()
                formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
                f.write(f'{formatted_now}-{messageType} MESSAGE-{mensaje}\n')
                f.close()
        except Exception as e:
            eventos.Eventos.mostrarMensajeError("Error al registrar en el logger, " + e)
