import logging
from SIM7600 import SIM7600  # Assurez-vous que SIM7600 est bien en mode synchrone


class SIM7600Network(SIM7600):
    def __init__(self, port, baudrate=115200, timeout=2):
        """Initialise le module réseau SIM7600 sur le port spécifié."""
        super().__init__(port, baudrate, timeout)

    def check_sim_status(self):
        """
        Vérifie l'état de la carte SIM et du réseau, et retourne le statut sous forme de chaîne.
        """
        commands = [
            ('AT+CPIN?', "Vérification de l'état de la carte SIM..."),
            ('AT+CFUN?', "Vérification du mode RF..."),
            ('AT+CNMP?', "Vérification du mode réseau..."),
            ('AT+CSQ', "Vérification de la qualité du signal..."),
            ('AT+COPS?', "Vérification de l'opérateur..."),
            ('AT+CPSI?', "Vérification de l'état du réseau..."),
            ('AT+CGREG?', "Vérification de l'enregistrement sur le réseau..."),
            ('AT+CGDCONT?', "Vérification de la configuration de l'APN..."),
            ('AT+SIMCOMATI', "Vérification de la version du firmware...")
        ]

        status = []
        for cmd, desc in commands:
            logging.info(desc)
            response = self.send_command(cmd)
            if response:
                status.append(f"{desc} : {response.strip()}")
            else:
                status.append(f"{desc} : Échec ou pas de réponse")

        return "\n".join(status)  # Retourne tout le statut en une seule chaîne


# Exemple d'utilisation
def main():
    # Initialiser le module SIM7600Network
    sim7600_network = SIM7600Network(port="COM13")

    try:
        # Ouvrir la connexion série
        sim7600_network.open_connection()

        if sim7600_network.serial_conn.is_open:
            logging.info("Port série ouvert avec succès.")

            # Vérifier l'état de la carte SIM et du réseau
            sim_status = sim7600_network.check_sim_status()
            print(sim_status)

        else:
            logging.error("Impossible d'ouvrir le port série.")

    except Exception as e:
        pass

    finally:
        # Fermer la connexion série proprement
        if sim7600_network.is_open:
            sim7600_network.close_connection()
            logging.info("Connexion série fermée.")


if __name__ == "__main__":
    main()
