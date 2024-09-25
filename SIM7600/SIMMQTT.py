import logging
import time

import paho.mqtt.client as mqtt

from SIM7600 import SIM7600

class SIM7600MQTT(SIM7600):
    def __init__(self, port, apn, broker, port_mqtt=1883):
        super().__init__(port)
        self.apn = apn
        self.broker = broker
        self.broker_port = port_mqtt
        self.open_connection()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

        # Définition des callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc, properties=None, user_data=None):
        """Callback appelé lors de la connexion au broker."""
        logging.info(f"Connecté au broker avec le code de résultat {rc}")
        client.subscribe("test/topic")  # Souscription à un topic

    def on_message(self, client, userdata, message):
        """Callback appelé lors de la réception d'un message."""
        logging.info(f"Message reçu sur le topic {message.topic}: {message.payload.decode()}")

    def on_publish(self, client, userdata, mid, properties=None, user_data=None):
        """Callback appelé après la publication d'un message."""
        logging.info(f"Message publié avec ID: {mid}")

    def connect_mqtt(self):
        """Connecte le client Paho au broker MQTT."""
        try:
            self.client.connect(self.broker, self.broker_port)
            self.client.loop_start()  # Démarre le loop pour traiter les messages
            logging.info("Client MQTT connecté.")
        except Exception as e:
            logging.error(f"Erreur lors de la connexion au broker MQTT: {e}")

    def publish(self, topic, message):
        """Publie un message sur un topic MQTT."""
        self.client.publish(topic, message)
        logging.info(f"Message publié sur {topic}: {message}")

    def close(self):
        """Ferme la connexion au broker MQTT et la connexion série."""
        self.client.loop_stop()
        self.client.disconnect()
        super().close_connection()

    def configure_apn(self):
        """Configure l'APN pour la connexion de données."""
        self.send_command(f'AT+CGDCONT=1,"IP","{self.apn}"')

    def connect(self):
        """Établit une connexion de données GPRS."""
        self.configure_apn()
        self.send_command('AT+CGATT=1')
        self.send_command('AT+CIICR')
        ip = self.send_command('AT+CIFSR')
        return ip


# Utilisation de la classe
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sim7600_mqtt = SIM7600MQTT(port="COM17", apn="m2m.lebara.fr", broker="test.mosquitto.org")

    try:
        ip = sim7600_mqtt.connect()  # Appel à la méthode connect de la classe SIM7600
        logging.info(f"Adresse IP: {ip}")

        # Connecter au broker MQTT
        sim7600_mqtt.connect_mqtt()

        # Publier un message
        topic = "test/topic"
        for i in range(10000):
            message = f"Message {i}: Hello, MQTT via SIM7600!"
            sim7600_mqtt.publish(topic, message)

        # Gardez le programme en cours d'exécution pour écouter les messages
        time.sleep(2)  # Attendre 10 secondes pour permettre l'écoute

    except Exception as e:
        logging.error(f"Erreur: {e}")
    finally:
        sim7600_mqtt.close()
