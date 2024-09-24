import logging

from serial.serialutil import SerialException

from SIM7600 import SIM7600


class SIMGPS(SIM7600):
    def __init__(self, port, baudrate=115200, timeout=2):
        # Appelle le constructeur de la classe parente
        super().__init__(port, baudrate, timeout)
        logging.info("Module GPS initialisé.")

    def enable_gps(self):
        """Active le module GPS."""
        response = self.send_command("AT+CGPS=1")  # Activer le GPS
        if "OK" in response:
            logging.info("GPS activé avec succès.")
        else:
            logging.error("Erreur lors de l'activation du GPS.")

    def get_gps_data(self):
        """Récupère les données GPS."""
        response = self.send_command("AT+CGPSINFO")
        if "$GP" in response:
            return response
        else:
            logging.error("Erreur dans la réception des données GPS.")
            return None

    def disable_gps(self):
        """Désactive le module GPS."""
        response = self.send_command("AT+CGPS=0")
        if "OK" in response:
            logging.info("GPS désactivé avec succès.")
        else:
            logging.error("Erreur lors de la désactivation du GPS.")


def main():
    ports_to_try = ["COM16"]  # Liste des ports à essayer
    simgps = None

    for port in ports_to_try:
        try:
            simgps = SIMGPS(port)
            simgps.open_connection()
            logging.info(f"Connexion réussie sur le port {port}.")
            break
        except SerialException as e:
            logging.warning(f"Le port {port} est indisponible")
        except Exception as e:
            logging.error(f"Erreur inattendue lors de l'ouverture du port {port}")

    if simgps is None:
        logging.critical("Impossible de se connecter à un port série.")
        return

    # Activer le GPS et récupérer les données
    simgps.enable_gps()

    # Attendre un peu pour laisser le GPS obtenir un fix
    import time
    time.sleep(5)

    # Récupérer les données GPS
    for i in range(100):
        gps_data = simgps.get_gps_data()
        if gps_data:
            logging.info(f"Données GPS : {gps_data}")
        else:
            logging.error("Aucune donnée GPS valide reçue.")

    # Désactiver le GPS après usage
    simgps.disable_gps()

    # Fermer la connexion série
    simgps.close_connection()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
