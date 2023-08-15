import os
import smtplib
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Configuración - Modificar aqui 
correo_emisor = 'jazgamarra@example'
password_emisor = 'password123'
asunto_correo = 'Certificado - Cursos y Talleres de Invierno 2023'
cuerpo_correo = '''¡Muchas gracias por participar de los Cursos y Talleres de Invierno 2023! Adjuntamos tu certificado de participación.'''
carpeta_archivos = r'C:\\ ... \\carpeta_certificados' # modificar para el uso

# Función para extraer la dirección de correo electrónico del nombre del archivo
def obtener_correo_desde_nombre(nombre_archivo):
    patron_correo = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    resultado = re.search(patron_correo, nombre_archivo)
    if resultado:
        return resultado.group(1)
    else:
        return None

# Función para enviar el correo
def enviar_correo(correo_destinatario, archivo):
    msg = MIMEMultipart()
    msg['From'] = correo_emisor
    msg['To'] = correo_destinatario
    msg['Subject'] = asunto_correo

    msg.attach(MIMEText(cuerpo_correo, 'plain')) 

    with open(archivo, "rb") as f:
        adjunto = MIMEApplication(f.read(), _subtype="pdf")
        adjunto.add_header('Content-Disposition', 'attachment', filename=os.path.basename(archivo))
        msg.attach(adjunto)

    # Enviar el correo
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(correo_emisor, password_emisor)
    server.sendmail(correo_emisor, correo_destinatario, msg.as_string())
    server.quit()

def main (): 
    # Obtener la lista de archivos pdf en la carpeta
    archivos_pdf = [archivo for archivo in os.listdir(carpeta_archivos) if archivo.endswith('.pdf')]

    # Enviar cada archivo a la dirección de correo correspondiente
    for archivo in archivos_pdf:
        correo_destinatario = obtener_correo_desde_nombre(archivo[:-4])  # Eliminar los últimos 4 caracteres (.pdf)
        if correo_destinatario:
            ruta_archivo = os.path.join(carpeta_archivos, archivo)
            enviar_correo(correo_destinatario, ruta_archivo)
            print(f'Archivo {archivo} enviado a {correo_destinatario} correctamente.')
        else:
            print(f'Error: El archivo {archivo} no contiene una dirección de correo válida.')

main()