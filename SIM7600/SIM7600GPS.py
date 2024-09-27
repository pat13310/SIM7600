import logging
import time

from serial.serialutil import SerialException

from SIM7600Cmd import SIM7600Cmd
from SerialPortCategorizer import SerialPortCategorizer


class SIM7600GPS(SIM7600Cmd):
    def __init__(self, port, baudrate=115200, timeout=2):
        # Appelle le constructeur de la classe parente
        super().__init__(port, baudrate, timeout)
        self.fixed = False
        logging.info("Module GPS en cours de démarrage.")

    def get_gps_data(self):
        """Récupère les données GPS."""
        response = self.send_command("AT+CGPSINFO", raw=True)
        if "$" in response:
            self.fixed = True
            response = response.splitlines()
            return response
        else:
            logging.error("Aucune réception des données GPS.")
            self.fixed = False
            return None

    def disable_gps(self):
        """Désactive le module GPS."""
        # response = self.send_command("AT+CGPS=0")
        # if "CGPS" in response:
        #     logging.info("GPS désactivé avec succès.")
        # else:
        #     logging.error("Erreur lors de la désactivation du GPS.")

        self.fixed = False

    def is_ready(self):
        return self.fixed


def main():
    try:
        serp = SerialPortCategorizer()
        port_cmd = serp.get_port("at")
        port = serp.get_port("gps")

        sim_cmd = SIM7600Cmd(port_cmd)
        sim_cmd.open_connection()
        sim_cmd.enable_gps()
        time.sleep(2)
        sim_gps = SIM7600GPS(port)
        sim_gps.set_echo_command(False)
        sim_gps.open_connection()

        logging.info(f"Connexion réussie sur le port {port}.")
        time.sleep(5)  # Attente de 10 secondes pour l'initialisation du GPS

        for i in range(2):
            gps_data = sim_gps.get_gps_data()
            for data in gps_data:
                if len(data) > 16:
                    print(data)
            time.sleep(1)  # Attente de 5 secondes avant de réessayer

    except SerialException as e:
        logging.warning(f"Le port {port} est indisponible")
    except Exception as er:
        logging.error(f"Erreur inattendue lors de l'ouverture du port {port}")
    finally:
        #sim_gps.disable_gps()
        sim_gps.close_connection()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
