import logging
import re
import time
import enum


from SIM7600 import SIM7600
from SerialPortCategorizer import SerialPortCategorizer
from TextToSpeech import TextToSpeech


class TypeCall(enum.Enum):
    VOICE = 0
    AUTOMATE=1


class SIM7600Voice(SIM7600):
    def __init__(self, port, tts=None):
        """Initialise le module vocal sur le port spécifié."""
        super().__init__(port)
        self.text_automate = "Message automatique du module SIM 7600"
        self.tts = tts
        self.duration = 0
        self.phone = None
        self.mode_call = TypeCall.VOICE

    def call(self, phone_number):
        """Compose un numéro de téléphone et détecte le décrochage de l'appelé."""
        self.phone = phone_number
        response = self.send_command(f'ATD{phone_number};')
        if 'OK' in response:
            logging.info("Appel lancé avec succès.")
            self._wait_for_connection()
        else:
            logging.error("Erreur lors du lancement de l'appel.")
        return response

    def _wait_for_connection(self):
        """Attend la connexion de l'appel et gère le statut."""
        while True:
            call_status = self.read_response()
            if 'CONNECT' in call_status:
                logging.info(f"L'appelé {self.phone} a décroché.")
                break
            elif 'NO CARRIER' in call_status:
                logging.info(f"L'appel avec {self.phone} a été terminé.")
                break
            time.sleep(1)  # Attendre un moment avant de vérifier à nouveau

    def hang_up(self):
        """Raccroche l'appel en cours."""
        response = self.send_command('ATH')
        if 'OK' in response:
            logging.info("Appel raccroché avec succès.")
        else:
            logging.error("Erreur lors du raccrochage.")
        return response

    def enable_caller_id(self):
        """Active l'identification de l'appelant (CLI)."""
        response = self.send_command('AT+CLIP=1')
        if 'OK' in response:
            logging.info("Identification de l'appelant activée.")
        else:
            logging.error("Erreur lors de l'activation de l'identification de l'appelant.")
        return response

    def set_volume(self, level):
        """Configure le volume audio du module, où level est compris entre 0 et 100."""
        response = self.send_command(f'AT+CLVL={level}')
        if 'OK' in response:
            logging.info(f"Volume réglé à {level}.")
        else:
            logging.error("Erreur lors du réglage du volume.")
        return response

    def read_response(self):
        """Lit la réponse du module SIM7600 depuis le port série."""
        response = []
        while True:
            line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
            if line:
                if "BEGIN" in line:
                    logging.debug(f"Début de l'appel avec {self.phone}")
                    if self.mode_call == TypeCall.AUTOMATE:
                        self._handle_automate_mode()
                elif "END" in line:
                    self.duration = self.extract_call_duration(line)
                    logging.debug(f"Fin de l'appel avec {self.phone}")
                elif "NO CARRIER" in line:
                    pass
                else:
                    logging.debug(f"Lu: {line}")
                response.append(line)
            else:
                break  # Arrête de lire si aucune nouvelle donnée n'est reçue
        return '\n'.join(response)

    def _handle_automate_mode(self):
        """Gère le mode d'appel automatique."""
        if self.tts:
            self.tts.say(self.text_automate)  # Cette ligne joue le message
            # Assurez-vous que l'audio est physiquement acheminé vers le module SIM
            self.hang_up()

    def extract_call_duration(self, log_entry):
        """Extrait la durée de l'appel du journal."""
        match = re.search(r'VOICE CALL: END: (\d+)', log_entry)
        if match:
            call_duration_seconds = int(match.group(1))
            return self.convert_seconds_to_hms(call_duration_seconds)
        else:
            return None

    def get_duration(self):
        """Retourne la durée de l'appel."""
        return self.duration

    def convert_seconds_to_hms(self, duration_seconds):
        """Convertit une durée en secondes en format heures, minutes, et secondes."""
        # Calculer les heures, minutes et secondes
        hours, remainder = divmod(duration_seconds, 1000)
        minutes, seconds = divmod(remainder, 100)

        # Formater en H:M:S
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def set_automate_text(self, texte: str):
        """Configure le texte pour le mode automatique."""
        self.mode_call = TypeCall.AUTOMATE
        self.text_automate = texte


# Exemple d'utilisation
def main():
    serp = SerialPortCategorizer()
    port=serp.get_port("at")
    tts = TextToSpeech()
    sim7600_voice = SIM7600Voice(port, tts)
    try:
        sim7600_voice.open_connection()

        # Activer l'identification de l'appelant
        sim7600_voice.enable_caller_id()
        sim7600_voice.set_volume(5)  # Régler le volume à 50%
        #sim7600_voice.set_automate_text("Salut, c'est un message automatique du module SIM 7600")

        # Composer un appel
        sim7600_voice.call("0665167626")

    except Exception as e:
        logging.error(f"Erreur: {e}")
    finally:
        logging.info(f"Durée de l'appel: {sim7600_voice.get_duration()}")
        sim7600_voice.close_connection()


if __name__ == '__main__':
    main()
