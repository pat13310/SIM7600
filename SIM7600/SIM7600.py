import re
from typing import Dict, Any, Optional

import serial
from serial import SerialException

from enum import Enum
import logging
import colorlog

class NetworkStatus(Enum):
    NOT_REGISTERED = 0
    REGISTERED_HOME = 1
    SEARCHING = 2
    REGISTRATION_DENIED = 3
    UNKNOWN = 4
    REGISTERED_ROAMING = 5

# class NetworkType(Enum):
#     GSM = 0
#     GPRS = 1
#     EDGE = 3
#     UMTS = 2
#     HSDPA = 4
#     HSUPA = 5
#     HSPA = 6
#     LTE = 7
#     NR = 8  # 5G New Radio

class RegistrationError(Exception):
    pass

class NetworkType(Enum):
    G2 = 13  # GSM only
    G3 = 14  # WCDMA only
    G4 = 38  # LTE only
    G5 = 71  # NR only (5G)
    AUTO = 2  # Automatic

# Configuration du logging
def setup_logging():
    handler = colorlog.StreamHandler()
    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


setup_logging()



class SIM7600:
    def __init__(self, port, baudrate=115200, timeout=2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        logging.info(f"Initialisation de SIM7600 sur le port {port}.")

    def open_connection(self):
        """Ouvre la connexion série."""
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            logging.info(f"Connexion établie sur le port {self.port}.")
        except SerialException as e:
            logging.error(f"Erreur lors de l'ouverture du port {self.port}")
            raise SerialException(f"Erreur d'ouverture du port {self.port}")

    def close_connection(self):
        """Ferme la connexion série."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            logging.info("Connexion fermée.")

    def send_command(self, command):
        """Envoie une commande AT et attend la réponse."""
        if not self.serial_conn or not self.serial_conn.is_open:
            raise SerialException("Le port série n'est pas ouvert.")

        # Envoyer la commande AT
        logging.info(f"Envoi de la commande: {command}")
        self.serial_conn.write((command + '\r\n').encode('utf-8'))

        # Lire la réponse jusqu'à "OK"
        response = self.serial_conn.read_until(b"OK\r\n").decode('utf-8')
        response = self.clean_message(response)
        return response

    def clean_message(self, message):
        response = message.replace("\r", "")
        response = response.rstrip()
        response = response.split("\n")
        return " ".join(response)

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
            logging.error(f"Erreur lors de la vérification de la carte SIM : {response}")
            return False

    def is_open(self):
        """Vérifie si la connexion série est ouverte."""
        if self.serial_conn:
            return self.serial_conn.is_open
        return False

    def get_signal_quality(self):
        """Récupère la qualité du signal en dBm et l'interprète."""
        response = self.send_command('AT+CSQ')
        if "+CSQ: " in response:
            response = self.clean_message(response)
            csq_values = response.split("+CSQ: ")[1].split(",")
            if len(csq_values) < 2:
                return "Erreur: Réponse invalide"
            signal_quality = int(csq_values[0])
            if signal_quality == 99:
                return "Signal inconnu"
            else:
                dbm = signal_quality * 2 - 113
                if dbm >= -70:
                    quality = "Excellent"
                elif dbm >= -85:
                    quality = "Bon"
                elif dbm >= -100:
                    quality = "Faible"
                else:
                    quality = "Très faible"
                return dbm,quality
        else:
            return "Erreur: Impossible de récupérer la qualité du signal"

    def get_operator_info(self):
        """Récupère des informations sur l'opérateur."""
        response = self.send_command('AT+COPS?')
        return response

    def get_lte_cell_id(self):
        """Récupère le Cell ID pour les réseaux LTE."""
        response = self.send_command('AT+CEREG?')
        return response

    def set_network_mode(self, network_type: NetworkType):
        if not isinstance(network_type, NetworkType):
            raise ValueError("Le type de réseau doit être une valeur de l'énumération NetworkType")

        command = f'AT+CNMP={network_type.value}'
        response = self.send_command(command)

        if 'OK' in response:
            logging.info(f"Mode réseau configuré sur {network_type.name}")
        else:
            logging.warning(f"Erreur lors de la configuration du mode réseau {network_type.name}")

    def get_current_network_mode(self):
        response = self.send_command('AT+CNMP?')

        # La réponse typique sera sous la forme "+CNMP: <mode>"
        if '+CNMP:' in response:
            response=response.replace("OK","")
            mode = response.split(':')[1].strip()
            mode = int(mode)  # Convertir en entier

            # Mapper la valeur du mode à l'énumération NetworkType
            for network_type in NetworkType:
                if network_type.value == mode:
                    return network_type

            # Si le mode n'est pas reconnu, retourner None ou lever une exception
            logging.warning(f"Mode réseau non reconnu : {mode}")
            return None
        else:
            logging.error("Erreur lors de la récupération du mode réseau")
            return None

    def get_network_type_str(self):
        network_mode = self.get_current_network_mode()
        if network_mode:
            if network_mode == NetworkType.AUTO:
                return "Automatique"
            else:
                mode=network_mode.name.replace('G', '')  # Retourne '2', '3', '4', ou '5'
                return f'Mode {mode}G'
        else:
            return "Inconnu"

    def check_network_registration(self) -> Dict[str, Any]:
        """
        Vérifie l'état d'enregistrement du réseau de manière détaillée.

        Returns:
            Dict[str, Any]: Un dictionnaire contenant les informations détaillées d'enregistrement du réseau.

        Raises:
            RegistrationError: Si une erreur se produit lors de la vérification de l'enregistrement.
        """
        try:
            response = self.send_command('AT+CREG?')
            extended_response = self.send_command('AT+CEREG?')
            signal_quality,_ = self.get_signal_quality()
            operator_info = self.get_operator_info()

            result = self._parse_creg_response(response)
            result.update(self._parse_cereg_response(extended_response))
            result['signal_quality'] = signal_quality
            result['operator'] = operator_info

            self._enrich_network_info(result)

            return result
        except Exception as er:
            raise RegistrationError(f"Erreur lors de la vérification de l'enregistrement réseau: {str(er)}")

    def _parse_creg_response(self, response: str) -> Dict[str, Any]:
        """Parse la réponse de la commande AT+CREG?"""
        match = re.search(r'\+CREG: (\d+),(\d+)(?:,"([0-9A-F]+)","([0-9A-F]+)")?', response)
        if not match:
            raise ValueError("Format de réponse CREG invalide")

        n, stat = map(int, match.group(1, 2))
        lac = match.group(3)
        ci = match.group(4)

        return {
            'status': NetworkStatus(stat),
            'registered': stat in [1, 5],
            'location_area_code': lac,
            'cell_id': ci
        }

    def _parse_cereg_response(self, response: str) -> Dict[str, Any]:
        """Parse la réponse de la commande AT+CEREG?"""
        match = re.search(r'\+CEREG: (\d+),(\d+)(?:,"([0-9A-F]+)","([0-9A-F]+)",(\d+))?', response)
        if not match:
            raise ValueError("Format de réponse CEREG invalide")

        n, stat = map(int, match.group(1, 2))
        tac = match.group(3)
        ci = match.group(4)
        act = int(match.group(5)) if match.group(5) else None

        return {
            'tac': tac,  # Tracking Area Code (for 4G/5G)
            'eci': ci,   # E-UTRAN Cell Identifier (for 4G/5G)
            'act': NetworkType(act) if act is not None else None
        }

    def _enrich_network_info(self, result: Dict[str, Any]) -> None:
        """Enrichit les informations réseau avec des données supplémentaires"""
        result['network_generation'] = self._determine_network_generation(result.get('act'))
        result['coverage_quality'] = self._assess_coverage_quality(result.get('signal_quality'))
        result['location_info'] = self._get_approximate_location(result.get('location_area_code'), result.get('cell_id'))

    def _determine_network_generation(self, act: Optional[NetworkType]) -> str:
        if act is None:
            return "Inconnu"
        generation_map = {
            NetworkType.GSM: "2G",
            NetworkType.GPRS: "2.5G",
            NetworkType.EDGE: "2.75G",
            NetworkType.UMTS: "3G",
            NetworkType.HSDPA: "3.5G",
            NetworkType.HSUPA: "3.75G",
            NetworkType.HSPA: "3.75G",
            NetworkType.LTE: "4G",
            NetworkType.NR: "5G"
        }
        return generation_map.get(act, "Inconnu")

    def _assess_coverage_quality(self, signal_quality: int) -> str:
        if signal_quality >= -70:
            return "Excellent"
        elif signal_quality >= -85:
            return "Bon"
        elif signal_quality >= -100:
            return "Moyen"
        elif signal_quality >= -110:
            return "Faible"
        else:
            return "Très Faible"

    def _get_approximate_location(self, lac: Optional[str], ci: Optional[str]) -> Dict[str, Any]:
        # Cette méthode pourrait être implémentée pour obtenir une localisation approximative
        # basée sur le LAC et le Cell ID, peut-être en utilisant une API externe ou une base de données locale
        return {
            "latitude": None,
            "longitude": None,
            "accuracy": None,
            "source": "Network-based (approximate)"
        }

    def print_network_status(self) -> None:
        """Affiche un résumé détaillé du statut réseau"""
        try:
            info = self.check_network_registration()
            print("=== Statut du Réseau ===")
            print(f"Enregistré: {'Oui' if info['registered'] else 'Non'}")
            print(f"Statut: {info['status'].name}")
            print(f"Type de réseau: {info['act'].name if info['act'] else 'Inconnu'}")
            print(f"Génération: {info['network_generation']}")
            print(f"Qualité du signal: {info['signal_quality']} dBm ({info['coverage_quality']})")
            print(f"Opérateur: {info['operator']}")
            print(f"LAC/TAC: {info['location_area_code'] or info['tac'] or 'N/A'}")
            print(f"Cell ID/ECI: {info['cell_id'] or info['eci'] or 'N/A'}")
            if info['location_info']['latitude']:
                print(f"Position approximative: {info['location_info']['latitude']}, {info['location_info']['longitude']}")
            print("========================")
        except RegistrationError as e:
            print(f"Erreur lors de la vérification du statut réseau: {e}")


def main():
    ports_to_try = ["COM17"]
    sim7600 = None

    for port in ports_to_try:
        try:
            sim7600 = SIM7600(port)
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
        sim7600.set_network_mode(NetworkType.AUTO)
        response = sim7600.send_command("AT")
        logging.info(f"Réponse reçue: {response}")
        response,_ = sim7600.get_signal_quality()  # Vérifiez la qualité du signal
        logging.info(f"Réponse reçue: {response}")
        response = sim7600.get_operator_info()  # Récupérez les informations sur l'opérateur
        logging.info(f"Réponse reçue: {response}")
        response = sim7600.get_lte_cell_id()  # Essayez de récupérer le Cell ID LTE
        logging.info(f"Réponse reçue: {response}")

        response=sim7600.get_network_type_str()
        logging.info(f"Réponse reçue: {response} ")

        sim7600.print_network_status()


    except SerialException as es:
        logging.error(f"Erreur lors de l'envoi de la commande: {es}")
    except Exception as er:
        logging.error(f"Erreur inattendue: {er}")

    sim7600.close_connection()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pass
