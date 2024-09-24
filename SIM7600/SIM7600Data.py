import logging
import serial
from SIM7600 import SIM7600  # Assurez-vous que SIM7600 est également en mode synchrone


class SIM7600Data(SIM7600):
    def __init__(self, port, apn=None, baudrate=115200, timeout=2):
        """Initialise le module SIM7600 pour les données avec le port et l'APN spécifiés."""
        super().__init__(port, baudrate, timeout)
        self.apn = apn

    def configure_apn(self, apn):
        """Configure l'APN pour la connexion de données."""
        self.apn = apn
        logging.info(f"Configuration de l'APN: {self.apn}")
        self.send_command(f'AT+CGDCONT=1,"IP","{self.apn}"')  # Configure l'APN

    def connect(self):
        """Établit une connexion de données GPRS."""
        if not self.apn:
            raise ValueError("APN non configuré. Veuillez d'abord configurer un APN.")

        # Attacher le module au GPRS
        logging.info("Attachement au réseau GPRS...")
        self.send_command('AT+CGATT=1')

        # Établir la connexion
        logging.info("Établissement de la connexion de données...")
        self.send_command('AT+CIICR')

        # Obtenir l'adresse IP
        ip_address = self.send_command('AT+CIFSR')
        logging.info(f"Adresse IP obtenue: {ip_address.strip()}")
        return ip_address.strip()

    def disconnect(self):
        """Détache le module du GPRS."""
        logging.info("Détachement du réseau GPRS...")
        self.send_command('AT+CGATT=0')


def main():
    # Initialiser le module SIM7600Data
    sim7600_data = SIM7600Data(port="COM13")

    try:
        # Ouvrir la connexion série
        sim7600_data.open_connection()

        if sim7600_data.serial_conn.is_open:
            logging.info("Port série ouvert avec succès.")

            # Configurer l'APN
            apn = "your.apn.com"  # Remplacez par votre APN
            sim7600_data.configure_apn(apn)

            # Se connecter au réseau GPRS
            ip_address = sim7600_data.connect()
            print(f"Connexion établie avec l'adresse IP : {ip_address}")

            # Effectuer des opérations de données ici (comme envoyer ou recevoir des données)

        else:
            logging.error("Impossible d'ouvrir le port série.")

    except Exception as e:
        logging.error(f"Erreur lors de l'exécution : {e}")

    finally:
        # Déconnecter du réseau et fermer la connexion série proprement
        if sim7600_data.serial_conn.is_open:
            sim7600_data.disconnect()
            sim7600_data.close_connection()
            logging.info("Connexion série fermée.")


if __name__ == "__main__":
    main()
