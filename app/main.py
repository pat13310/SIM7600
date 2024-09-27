import asyncio
import logging

from SIM7600.SIM7600Cmd import SIM7600Cmd

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SerialPortError(Exception):
    """Exception levée pour les erreurs liées au port série."""
    pass


async def main():
    sim7600 = SIM7600Cmd()
    await sim7600.open()

    try:
        # Vérification de l'état de la SIM
        sim_status = await sim7600.send_command("AT+CPIN?")
        logging.info(f"État de la SIM: {sim_status}")

        # Activation du GPS
        gps_status = await sim7600.send_command("AT+CGPS=1")
        logging.info(f"Activation GPS: {gps_status}")

        # Attendre un moment pour obtenir des données GPS
        await asyncio.sleep(5)  # Attendre un peu pour que le GPS se fixe
        gps_info = await sim7600.send_command("AT+CGPSINFO")
        logging.info(f"Informations GPS: {gps_info}")

        # Envoi d'un SMS
        await sim7600.send_command("AT+CMGF=1")  # Mettre le mode SMS
        sms_command = 'AT+CMGS="+1234567890"'  # Remplacez par le numéro à appeler
        sms_response = await sim7600.send_command(sms_command)
        await asyncio.sleep(1)  # Attendre un moment pour que la commande soit acceptée
        sms_response += await sim7600.send_command("Bonjour, ceci est un test. \x1A")  # Envoyer le message
        logging.info(f"Réponse SMS: {sms_response}")

        # Connexion de données
        await sim7600.send_command('AT+CSTT="your.apn.here"')  # Remplacez par votre APN
        ip_address = await sim7600.send_command('AT+CIICR')  # Activer la connexion
        logging.info(f"Adresse IP obtenue: {ip_address}")

        # Passer un appel
        call_response = await sim7600.send_command('ATD+33665167626;')  # Remplacez par le numéro à appeler
        logging.info(f"Réponse d'appel: {call_response}")

    except Exception as e:
        logging.error(f"Une erreur s'est produite : {e}")

    finally:
        sim7600.close()

if __name__ == "__main__":
    asyncio.run(main())
