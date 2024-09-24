import logging

from SIM7600 import SIM7600


class SIM7600SMS(SIM7600):
    def __init__(self, port, baudrate=115200, timeout=2):
        """Initialise le module SMS sur le port spécifié."""
        super().__init__(port, baudrate, timeout)
        self.transport = None  # Connexion série sera gérée par SIM7600

    def check_sim_card(self):
        """Vérifie si une carte SIM est présente et prête."""
        response = self.send_command('AT+CPIN?')
        if "READY" in response:
            logging.info("Carte SIM détectée et prête.")
            return True
        elif "SIM PIN" in response:
            logging.warning("La carte SIM demande un code PIN.")
            return False
        else:
            logging.error("Carte SIM non détectée.")
            return False

    def send_sms(self, phone_number, message):
        """Envoie un SMS au numéro spécifié avec le message donné."""
        if not self.check_sim_card():
            logging.error("Impossible d'envoyer un SMS : aucune carte SIM prête.")
            return None

        # Met le module en mode texte
        self.send_command('AT+CMGF=1')
        # Définit le numéro du destinataire
        self.send_command(f'AT+CMGS="{phone_number}"')
        # Envoie le message suivi de chr(26) qui représente Ctrl+Z pour finir le SMS
        self.serial_conn.write((message + chr(26)).encode())

        # Attendre la réponse du module
        response = self.read_response()
        response = self.clean_message(response)

        return response

    def read_response(self):
        """Lit la réponse du module série."""
        if self.serial_conn is None or not self.serial_conn.is_open:
            logging.error("Le port série n'est pas ouvert.")
            return None

        # On va lire la réponse jusqu'à recevoir 'OK' ou une autre fin de commande
        response = self.serial_conn.read_until(b"OK\r\n").decode('utf-8')
        return response.strip()

    def read_sms(self, delete_action=False):
        """Récupère tous les SMS stockés dans la mémoire."""
        if not self.check_sim_card():
            logging.error("Impossible de lire les SMS : aucune carte SIM prête.")
            return None

        # Met le module en mode texte
        self.send_command('AT+CMGF=1')

        # Lire tous les SMS
        response = self.send_command('AT+CMGL="ALL"')
        #logging.info(f"Réponse à la lecture des SMS : \n{response}")

        if "CMGL" in response and delete_action ==True:
            # Extraire les indices des SMS à supprimer
            messages = response.split("CMGL")
            for line in messages:
                if line.startswith(":"):  # Vérifie si la ligne contient un message
                    tab = line.split(',')
                    index=tab[0].replace(": ", "")
                    if index.isdigit():
                        self.delete_sms(int(index))

        return response

    def delete_sms(self, index):
        """Supprime le SMS à l'index spécifié."""
        response = self.send_command(f'AT+CMGD={index}')
        logging.info(f"Supprimé SMS à l'index {index}. Réponse : {response}")

def main():
    sim7600_sms = SIM7600SMS(port="COM17")

    try:
        # Ouvrir la connexion série
        sim7600_sms.open_connection()

        if sim7600_sms.serial_conn.is_open:
            logging.info("Port série ouvert avec succès.")

            # Vérifier la carte SIM
            if sim7600_sms.check_sim_card():
                # Envoyer un SMS
                response = sim7600_sms.send_sms("0665167626", "Bonjour, ceci est un message test du module Sim7600 !.")
                logging.info(f"Réponse de l'envoi de SMS: {response}")
                # Lire les SMS
                sms_response = sim7600_sms.read_sms()
                logging.info(f"Réponse de la lecture des SMS : \n{sms_response}")
        else:
            logging.error("Impossible d'ouvrir le port série.")

    except Exception as e:
        pass

    finally:
        # Fermer la connexion série proprement
        sim7600_sms.close_connection()

if __name__ == "__main__":
    main()
