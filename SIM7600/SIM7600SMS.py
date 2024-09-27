import logging
import re
import string

from serial.serialutil import SerialException

from SIM7600.SerialPortCategorizer import SerialPortCategorizer
from SIM7600Cmd import SIM7600Cmd, NetworkType


def is_hexadecimal_and_printable(hex_str):
    # Supprime les espaces pour traiter des chaînes hexadécimales telles que "4F62 6F"
    hex_str = hex_str.replace(" ", "")

    # Vérifie si la chaîne est hexadécimale valide
    if re.match(r'^[0-9A-Fa-f]+$', hex_str):
        try:
            # Convertit la chaîne hexadécimale en bytes
            bytes_data = bytes.fromhex(hex_str)
            # Convertit les bytes en texte clair (ASCII)
            decoded_str = bytes_data.decode('utf-8', errors='ignore')  # ignore les erreurs de décodage

            # Vérifie si tous les caractères sont imprimables
            return all(c in string.printable for c in decoded_str)
        except ValueError:
            return False  # En cas d'erreur lors de la conversion
    return False  # Si la chaîne n'est pas une hexadécimale valide

class SIM7600SMS(SIM7600Cmd):
    def __init__(self, port, baudrate=115200, timeout=2):
        """Initialise le module SMS sur le port spécifié."""
        super().__init__(port, baudrate, timeout)
        self.sms_instances = []
        self.transport = None  # Connexion série sera gérée par SIM7600
        self.card_is_ready = False

    def check_sim_card(self):
        """Vérifie si une carte SIM est présente et prête."""
        response = self.send_command('AT+CPIN?')
        if "READY" in response:
            logging.info("Carte SIM détectée et prête.")
            self.card_is_ready = True
        elif "SIM PIN" in response:
            logging.warning("La carte SIM demande un code PIN.")
            self.card_is_ready = False
        else:
            logging.error("Carte SIM non détectée.")
            self.card_is_ready = False
        return self.card_is_ready

    def send_sms(self, phone_number, message):
        """Envoie un SMS au numéro spécifié avec le message donné."""
        if not self.card_is_ready:
            logging.error("Impossible d'envoyer un SMS : aucune carte SIM prête.")
            return None

        # Met le module en mode texte
        self.send_command('AT+CMGF=1')
        # Définit le numéro du destinataire
        self.send_command(f'AT+CMGS="{phone_number}"')
        self.serial_conn.write((message + chr(26)).encode())

        # Attendre la réponse du module
        response = self.read_response()
        response = self.clean_message(response)
        return response

    def command_read_sms(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            raise SerialException("Le port série n'est pas ouvert.")

        command='AT+CMGL="ALL"'
        # Envoyer la commande AT
        if self.echo:
            logging.info(f"Envoi de la commande: {command}")

        self.serial_conn.write((command + '\r\n').encode('utf-8',errors='ignore'))

        return self.read_response_message()


    def read_sms(self, delete_action=False):
        if not self.card_is_ready:
            logging.error("Impossible de lire les SMS : aucune carte SIM prête.")
            return None

        self.sms_instances = []
        response = self.send_command('AT+CMGF=1')
        if "CMGF" not in response:
            logging.error("Erreur lors de la configuration du mode SMS.")
            return

        response = self.command_read_sms()
        if "CMGL" in response:
            messages = response.split("CMGL")
            for line in messages:
                line = line.strip()
                if line.startswith(":"):
                    self.process_sms_line(line)

        if delete_action:
            for instance in self.sms_instances:
                self.delete_sms(instance['index'])

        return self.sms_instances

    def read_response(self, show=False, raw=False):
        response = self.serial_conn.read_until(b"OK\r\n")
        response=response.decode()
        if not show:
            response = response.replace("OK", "")
        if not raw:
            response = self.clean_message(response)
        return response

    def read_response_message(self, show=False, raw=False):
        response = self.serial_conn.read_until(b"OK\r\n")
        response=response.decode("utf-8",errors='ignore')
        if not show:
            response = response.replace("OK", "")
        if not raw:
            response = self.clean_message(response)
        return response

    def process_sms_line(self, line):
        pattern = r'^:\s(\d+),"REC READ","(\+?\d+)","","(\d{2}/\d{2}/\d{2}),(\d{2}:\d{2}:\d{2}\+\d{2})"\s(.*)'
        match = re.search(pattern, line)
        if match:
            index, phone_number, date, time, content_hex = match.groups()
            content = self.decode_content(content_hex)
            sms_instance = {
                'index': int(index),
                'phone_number': phone_number,
                'date': date,
                'time': time,
                'content': content
            }
            self.sms_instances.append(sms_instance)

    def decode_content(self, content_hex):
        if is_hexadecimal_and_printable(content_hex):
            return bytes.fromhex(content_hex).decode('utf-16-be', errors='ignore')
        return content_hex

    def get_sms(self):
        return self.sms_instances


    def delete_sms(self, index):
        """Supprime le SMS à l'index spécifié."""
        response = self.send_command(f'AT+CMGD={index}')
        logging.info(f"Supprimé SMS à l'index {index}. Réponse : {response}")



def main():
    logging.basicConfig(level=logging.INFO)

    ports_to_try = ["COM17"]  # Add more ports as needed
    sim7600 = None

    # Attempt to establish connection
    for port in ports_to_try:
        try:
            sim7600 = SIM7600SMS(port)
            sim7600.open_connection()
            logging.info(f"Connexion réussie sur le port {port}.")
            break
        except SerialException as e:
            logging.warning(f"Le port {port} est indisponible: {e}")
        except Exception as e:
            logging.error(f"Erreur inattendue lors de l'ouverture du port {port}: {e}")

    if sim7600 is None:
        logging.critical("Impossible de se connecter à un port série.")
        return

    try:
        if sim7600.check_sim_card():
            logging.info("Carte SIM prête.")
        else:
            logging.warning("Carte SIM non prête.")
            return

        # Example: Send an SMS
        # phone_number = input("Entrez le numéro de téléphone pour envoyer un SMS: ")
        # message = input("Entrez le message à envoyer: ")
        # response = sim7600.send_sms(phone_number, message)
        # logging.info(f"Réponse à l'envoi de SMS: {response}")

        # Example: Read SMS
        read_sms = sim7600.read_sms()
        for sms in read_sms:
            print(f"SMS: {sms}")

        # Optionally delete SMS after reading
        delete_after_read = input("Voulez-vous supprimer les SMS lus ? (o/n): ").lower() == 'o'
        if delete_after_read:
            for sms in read_sms:
                sim7600.delete_sms(sms['index'])

    except SerialException as es:
        logging.error(f"Erreur lors de l'envoi de la commande: {es}")
    except Exception as er:
        logging.error(f"Erreur inattendue: {er}")
    finally:
        sim7600.close_connection()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Erreur dans le programme principal: {e}")
