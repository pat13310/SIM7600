import logging
import time
from SIM7600 import SIM7600Cmd  # Assurez-vous d'importer correctement votre classe SIM7600

class SIM7600Modem(SIM7600):
    def __init__(self, port, apn="Lebara"):
        """Initialise le module SIM7600 avec le port série et l'APN Lebara."""
        super().__init__(port)
        self.apn = apn

    def configure_apn(self):
        """Configure l'APN pour l'opérateur Lebara."""
        response = self.send_command(f'AT+CGDCONT=1,"IP","{self.apn}"')
        if "OK" in response:
            logging.info(f"APN configuré : {self.apn}")
        else:
            logging.error("Erreur lors de la configuration de l'APN.")

    def attach_to_network(self):
        """Attache le module au réseau cellulaire."""
        response = self.send_command('AT+CGATT=1')
        if "OK" in response:
            logging.info("Module attaché au réseau.")
        else:
            logging.error("Échec de l'attachement au réseau.")

    def establish_ppp_connection(self):
        """Établit une connexion PPP pour l'accès à Internet."""
        response = self.send_command('ATD*99#')
        if "CONNECT" in response:
            logging.info("Connexion PPP établie.")
        else:
            logging.error("Erreur lors de l'établissement de la connexion PPP.")

    def get_ip_address(self):
        """Obtient l'adresse IP après la connexion."""
        ip_address = self.send_command('AT+CIFSR')
        logging.info(f"Adresse IP obtenue : {ip_address}")
        return ip_address

    def connect(self):
        """Configure l'APN, attache au réseau, et établit la connexion PPP."""
        self.configure_apn()
        self.attach_to_network()
        time.sleep(2)  # Pause pour stabiliser la connexion
        self.establish_ppp_connection()
        return self.get_ip_address()

# Utilisation du module SIM7600Modem avec Lebara
if __name__ == "__main__":
    try:
        modem = SIM7600Modem(port="COM13")
        modem.open_connection()

        if modem.serial_conn.is_open:
            # Configurer et se connecter
            ip_address = modem.connect()
            print(f"Connecté avec l'adresse IP : {ip_address}")

        # Fermer la connexion une fois terminé
        modem.close_connection()
    except Exception as e:
        pass
