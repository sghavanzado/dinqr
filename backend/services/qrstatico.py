# generate_qr.py
import os
from PIL import Image
import qrcode
from vobject import vCard
import pythoncom
from win32com.server import dispatch

class QRGenerator:
    _public_methods_ = ['GenerateQR']
    _reg_progid_ = "QRGenerator.Python64"
    _reg_clsid_ = "{A1B2C3D4-5678-90AB-CDEF-1234567890AB}"  # Utiliza un GUID único para 64 bits

    def GenerateQR(self, telefone, email, nome, funcao, area, sap, output_path):
        try:
            # Crear vCard
            vcard = vCard()
            vcard.add("tel").value = telefone
            vcard.add("email").value = email
            vcard.add("fn").value = nome
            vcard.add("title").value = funcao
            vcard.add("nickname").value = area
            vcard.add("uid").value = sap

            # Serializar vCard
            vcard_data = vcard.serialize()

            # Generar código QR
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(vcard_data)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")

            # Asegurarse de que la carpeta de salida exista
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            # Guardar el código QR
            qr_file_name = f"{id}.png"
            qr_file_path = os.path.join(output_path, qr_file_name)
            img.save(qr_file_path)

            return qr_file_path

        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    from win32com.server import register
    register.UseCommandLine(QRGenerator)