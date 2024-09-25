import logging
import re
from serial.serialutil import SerialException

from SIM7600 import SIM7600


class SIM7600Info(SIM7600):
    def __init__(self, port, baudrate=115200, timeout=2):
        super().__init__(port, baudrate, timeout)

    def get_firmware_version(self):
        response = self.send_command("AT+CGMR")
        pattern=r'\+CGMR:\s*([^\s]+)'
        match = re.search(pattern, response)  # Extrait la version du firmware
        return match.group(1) if match else "Version non trouvée"

    def get_manufacturer(self):
        response = self.send_command("AT+CGMI")
        pattern = r'\+CGMI \s*(.+)'
        match = re.search(pattern, response)  # Extrait le nom du fabricant
        return match.group(1).strip() if match else "Fabricant non trouvé"

    def get_serial_number(self):
        response = self.send_command("AT+CGSN")
        pattern = r'\+CGSN \s*(.+)'   # Capture des caractères alphanumériques après +CGSN:
        match = re.search(pattern, response)  # Extrait le numéro de série
        return match.group(1) if match else "Numéro de série non trouvé"

    def get_module_version(self):
        response = self.send_command("AT+CGMM")
        pattern = r'\+CGMM \s*(.+)'
        match = re.search(pattern, response)  # Extrait la version du module
        return match.group(1).strip() if match else "Version du module non trouvée"

    def get_chip_info(self):
        response = self.send_command("AT+CSUB")
        # Nouvel pattern pour capturer les informations correctement
        pattern = r'\+CSUB:\s*([^\s]+)\s+\+CSUB:\s*([^\s]+)'

        match = re.search(pattern, response)
        chip_info={}
        if match:
            sub_version = match.group(1).strip()  # Version de sous-système
            modem_version = match.group(2).strip()  # Version de modem
            chip_info["sub_version"]=sub_version
            chip_info["modem_version"]=modem_version
            return chip_info
        else:
            return "Informations du chip non trouvées"

    def get_full_info(self):
        response = self.send_command("ATI")
        model_info = {}

        # Utilisation d'une expression régulière pour extraire le modèle, la révision et l'IMEI
        model_match = re.search(r'Model:\s*([\w\-]+)', response)
        revision_match = re.search(r'Revision:\s*([\w\-\.]+)', response)
        imei_match = re.search(r'IMEI:\s*(\d+)', response)

        if model_match:
            model_info['Modèle'] = model_match.group(1).strip()
        else:
            model_info['Modèle'] = "Modèle non trouvé"

        if revision_match:
            model_info['Révision'] = revision_match.group(1).strip()
        else:
            model_info['Révision'] = "Révision non trouvée"

        if imei_match:
            model_info['IMEI'] = imei_match.group(1).strip()
        else:
            model_info['IMEI'] = "IMEI non trouvé"

        return model_info

    def print_all_info(self):
        logging.info("=== Informations SIM7600 ===")
        logging.info(f"Micrologiciel: {self.get_firmware_version()}")
        logging.info(f"Fabricant: {self.get_manufacturer()}")
        logging.info(f"Numéro de série: {self.get_serial_number()}")
        logging.info(f"Version du module: {self.get_module_version()}")
        chip_info=self.get_chip_info()
        logging.info(f"Information du chip: sub version :{chip_info['sub_version']}")
        logging.info(f"Information du chip: modem version :{chip_info['modem_version']}")
        full_info = self.get_full_info()
        logging.info(f"Modèle: {full_info['Modèle']}")
        logging.info(f"Révision: {full_info['Révision']}")
        logging.info(f"IMEI: {full_info['IMEI']}")
        logging.info("============================")


def main():
    ports_to_try = ["COM17"]
    sim_info = None

    for port in ports_to_try:
        try:
            sim_info = SIM7600Info(port)
            sim_info.set_echo_command(False)
            sim_info.open_connection()
            logging.info(f"Connexion réussie sur le port {port}.")
            break
        except SerialException as e:
            logging.warning(f"Le port {port} est indisponible: {e}")
        except Exception as e:
            logging.error(f"Erreur inattendue lors de l'ouverture du port {port}: {e}")

    if sim_info is None:
        logging.critical("Impossible de se connecter à un port série.")
        return

    try:
        # Affichage de toutes les informations
        sim_info.print_all_info()

    except Exception as er:
        logging.error(f"Erreur inattendue: {er}")
    finally:
        sim_info.close_connection()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Erreur non gérée: {e}")
