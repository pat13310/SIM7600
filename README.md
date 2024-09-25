## Module SIM 7600
<image src="https://github.com/user-attachments/assets/a084f882-9833-4f40-a591-5fafea92a3cc" height="250px">

Voici la description de la classe SIM7600 et ses principales classes :

## Classe SIM7600

La classe SIM7600 est conçue pour interagir avec un modem SIM7600, permettant la gestion des communications cellulaires.

### Initialisation

```python
modem = SIM7600(port="COM17", baudrate=115200, timeout=2)
```

Cette ligne crée une instance de la classe SIM7600, configurée pour communiquer via le port COM17 avec un débit de 115200 bauds et un délai d'attente de 2 secondes[1].

### Fonctions principales

#### Ouverture de la connexion

```python
modem.open_connection()
```

Cette fonction ouvre la connexion série avec le modem. Elle doit être appelée avant toute autre opération[1].

#### Envoi de commandes AT

```python
response = modem.send_command("AT+CSQ")
print(f"Qualité du signal : {response}")
```

Cette fonction envoie une commande AT au modem et retourne la réponse. Dans cet exemple, elle récupère la qualité du signal[1].

#### Vérification de la carte SIM

```python
if modem.check_sim_card():
    print("Carte SIM détectée et prête")
else:
    print("Problème avec la carte SIM")
```

Cette fonction vérifie si une carte SIM est présente et prête à être utilisée[1].

#### Récupération de la qualité du signal

```python
dbm, quality = modem.get_signal_quality()
print(f"Force du signal : {dbm} dBm, Qualité : {quality}")
```

Cette fonction retourne la force du signal en dBm et une interprétation qualitative[1].

#### Configuration du mode réseau

```python
modem.set_network_mode(NetworkType.AUTO)
print(f"Mode réseau actuel : {modem.get_network_type_str()}")
```

Cette fonction permet de définir le mode réseau (2G, 3G, 4G, 5G ou automatique) et de vérifier le mode actuel[1].

#### Vérification de l'enregistrement réseau

```python
try:
    network_info = modem.check_network_registration()
    print(f"Statut d'enregistrement : {network_info['status'].name}")
    print(f"Opérateur : {network_info['operator']}")
except RegistrationError as e:
    print(f"Erreur d'enregistrement : {e}")
```

Cette fonction fournit des informations détaillées sur l'enregistrement du modem au réseau cellulaire[1].

#### Affichage du statut réseau

```python
modem.print_network_status()
```

Cette fonction affiche un résumé complet du statut réseau, incluant l'enregistrement, le type de réseau, la qualité du signal, et d'autres informations pertinentes[1].

#### Fermeture de la connexion

```python
modem.close_connection()
```

Cette fonction ferme proprement la connexion série avec le modem. Elle doit être appelée à la fin de l'utilisation du modem[1].

## Énumérations et exceptions

La classe utilise plusieurs énumérations pour représenter les différents états et types de réseau :

- `NetworkStatus` : représente les différents états d'enregistrement au réseau.
- `NetworkType` : représente les différents types de réseaux cellulaires (2G, 3G, 4G, 5G, AUTO).

Une exception personnalisée `RegistrationError` est également définie pour gérer les erreurs spécifiques à l'enregistrement réseau[1].

## Logging

La classe utilise le module `logging` avec une configuration colorée pour faciliter le débogage et le suivi des opérations[1].

Cette classe SIM7600 offre une interface complète pour gérer les communications cellulaires, permettant un contrôle fin du modem et l'accès à diverses informations réseau.

<br>

## Classe SIM7600SMS

La classe SIM7600SMS hérite de SIM7600 et ajoute des fonctionnalités spécifiques pour la gestion des SMS.

### Initialisation

```python
sms = SIM7600SMS(port="COM17", baudrate=115200, timeout=2)
```

Cette ligne crée une instance de la classe SIM7600SMS, configurée pour communiquer via le port COM17 avec un débit de 115200 bauds et un délai d'attente de 2 secondes.

### Fonctions principales

#### Vérification de la carte SIM

```python
if sms.check_sim_card():
    print("Carte SIM détectée et prête")
else:
    print("Problème avec la carte SIM")
```

Cette fonction vérifie si une carte SIM est présente et prête à être utilisée.

#### Envoi de SMS

```python
response = sms.send_sms("0612345678", "Bonjour, ceci est un test!")
print(f"Réponse de l'envoi de SMS : {response}")
```

Cette fonction envoie un SMS au numéro spécifié avec le message donné.

#### Lecture des SMS

```python
sms_list = sms.read_sms()
print(f"SMS reçus : {sms_list}")
```

Cette fonction récupère tous les SMS stockés dans la mémoire du modem.

#### Suppression de SMS

```python
sms.delete_sms(1)
```

Cette fonction supprime le SMS à l'index spécifié.

### Fonctionnalités supplémentaires

#### Lecture avec suppression automatique

```python
sms_list = sms.read_sms(delete_action=True)
print(f"SMS lus et supprimés : {sms_list}")
```

Cette option permet de lire tous les SMS et de les supprimer automatiquement après la lecture.

#### Lecture de la réponse du modem

```python
response = sms.read_response()
print(f"Réponse du modem : {response}")
```

Cette fonction lit la réponse du module série, utile pour le débogage ou la gestion des réponses asynchrones.

## Gestion des erreurs

La classe SIM7600SMS intègre une gestion des erreurs robuste :

- Vérification de la présence de la carte SIM avant chaque opération SMS.
- Logging des erreurs et des informations importantes.
- Gestion des exceptions pour les opérations critiques.

## Utilisation dans un script principal

```python
def main():
    sms = SIM7600SMS(port="COM17")
    try:
        sms.open_connection()
        if sms.check_sim_card():
            sms.send_sms("0612345678", "Message test")
            sms_list = sms.read_sms()
            print(f"SMS reçus : {sms_list}")
    except Exception as e:
        logging.error(f"Erreur : {e}")
    finally:
        sms.close_connection()

if __name__ == "__main__":
    main()
```

Ce script principal illustre l'utilisation typique de la classe SIM7600SMS, avec ouverture de la connexion, vérification de la carte SIM, envoi et lecture de SMS, et fermeture propre de la connexion.
<br>

## Classe SIMGPS

La classe SIMGPS hérite de SIM7600 et ajoute des fonctionnalités spécifiques pour la gestion du GPS.

### Initialisation

```python
gps = SIMGPS(port="COM16", baudrate=115200, timeout=2)
```

Cette ligne crée une instance de la classe SIMGPS, configurée pour communiquer via le port COM16 avec un débit de 115200 bauds et un délai d'attente de 2 secondes.

### Fonctions principales

#### Activation du GPS

```python
gps.enable_gps()
```

Cette fonction active le module GPS du modem.

#### Récupération des données GPS

```python
gps_data = gps.get_gps_data()
if gps_data:
    print(f"Données GPS : {gps_data}")
else:
    print("Aucune donnée GPS valide reçue.")
```

Cette fonction récupère les données GPS actuelles du modem.

#### Désactivation du GPS

```python
gps.disable_gps()
```

Cette fonction désactive le module GPS du modem.

### Gestion des erreurs

La classe SIMGPS intègre une gestion des erreurs robuste :

- Logging des erreurs et des informations importantes.
- Gestion des exceptions pour les opérations critiques.

## Utilisation dans un script principal

```python
def main():
    gps = SIMGPS(port="COM16")
    try:
        gps.open_connection()
        gps.enable_gps()
        
        # Attente pour obtenir un fix GPS
        time.sleep(5)
        
        for _ in range(100):
            gps_data = gps.get_gps_data()
            if gps_data:
                logging.info(f"Données GPS : {gps_data}")
            else:
                logging.error("Aucune donnée GPS valide reçue.")
        
        gps.disable_gps()
    except Exception as e:
        logging.error(f"Erreur : {e}")
    finally:
        gps.close_connection()

if __name__ == "__main__":
    main()
```

Ce script principal illustre l'utilisation typique de la classe SIMGPS, avec ouverture de la connexion, activation du GPS, récupération des données GPS en boucle, désactivation du GPS, et fermeture propre de la connexion.

## Particularités

- La classe utilise des commandes AT spécifiques pour gérer le GPS (AT+CGPS).
- Un délai est introduit après l'activation du GPS pour permettre l'obtention d'un fix.
- La récupération des données GPS se fait en boucle pour obtenir des mises à jour continues.
## Matériels nécessaires
<image src="https://github.com/user-attachments/assets/0a546fb1-bd19-48cc-8baa-9fa6e748a9d2" height="200px">
<br>
💡 <b>Remarque</b> : Comme illustré sur l'image, il faudra rajouter l"antenne pour fixer correctement le signal GPS.<br>
Cette classe SIMGPS offre une interface simple pour gérer les fonctionnalités GPS d'un modem SIM7600, permettant une intégration facile dans des projets nécessitant des capacités de géolocalisation.
<br>

## Classe SIM7600MQTT

La classe SIM7600MQTT hérite de SIM7600 et ajoute des fonctionnalités pour la communication MQTT via un modem cellulaire.

### Initialisation

```python
mqtt_modem = SIM7600MQTT(port="COM17", apn="m2m.lebara.fr", broker="test.mosquitto.org", port_mqtt=1883)
```

Cette ligne crée une instance de la classe SIM7600MQTT, configurée pour communiquer via le port COM17, utiliser l'APN "m2m.lebara.fr", et se connecter au broker MQTT "test.mosquitto.org" sur le port 1883.

### Fonctions principales

#### Configuration de l'APN

```python
mqtt_modem.configure_apn()
```

Cette fonction configure l'APN pour la connexion de données cellulaires.

#### Établissement de la connexion

```python
ip = mqtt_modem.connect()
print(f"Adresse IP: {ip}")
```

Cette fonction établit une connexion de données GPRS et retourne l'adresse IP attribuée.

#### Connexion au broker MQTT

```python
mqtt_modem.connect_mqtt()
```

Cette fonction connecte le client Paho MQTT au broker spécifié.

#### Publication de messages MQTT

```python
mqtt_modem.publish("test/topic", "Hello, MQTT via SIM7600!")
```

Cette fonction publie un message sur un topic MQTT spécifié.

#### Fermeture des connexions

```python
mqtt_modem.close()
```

Cette fonction ferme la connexion au broker MQTT et la connexion série.

### Callbacks MQTT

La classe définit également des callbacks pour gérer les événements MQTT :

- `on_connect`: Appelé lors de la connexion au broker
- `on_message`: Appelé lors de la réception d'un message
- `on_publish`: Appelé après la publication d'un message

## Utilisation dans un script principal

```python
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mqtt_modem = SIM7600MQTT(port="COM17", apn="m2m.lebara.fr", broker="test.mosquitto.org")

    try:
        ip = mqtt_modem.connect()
        logging.info(f"Adresse IP: {ip}")

        mqtt_modem.connect_mqtt()

        for i in range(10000):
            message = f"Message {i}: Hello, MQTT via SIM7600!"
            mqtt_modem.publish("test/topic", message)

        time.sleep(2)

    except Exception as e:
        logging.error(f"Erreur: {e}")
    finally:
        mqtt_modem.close()
```

Ce script principal illustre l'utilisation typique de la classe SIM7600MQTT, avec l'établissement de la connexion cellulaire, la connexion au broker MQTT, la publication de messages en boucle, et la fermeture propre des connexions.

Cette classe SIM7600MQTT offre une interface simple pour combiner les fonctionnalités d'un modem cellulaire SIM7600 avec la communication MQTT, permettant une intégration facile dans des projets IoT nécessitant une connectivité cellulaire.

<br>

## Classe SerialPortCategorizer
Voici des exemples d'utilisation pour chaque fonction de la classe SerialPortCategorizer :

### Initialisation

```python
port_categorizer = SerialPortCategorizer()
```

Cette ligne crée une instance de SerialPortCategorizer et catégorise automatiquement les ports disponibles.

### Affichage des ports catégorisés

```python
port_categorizer.display_ports()
```

Cette fonction affichera tous les ports catégorisés, par exemple :

```
Ports COM catégorisés :
  Nom du port: COM3, Description: Simcom AT Port, Catégorie: AT
  Nom du port: COM4, Description: Simcom GPS Port, Catégorie: GPS
  Nom du port: COM5, Description: Simcom Modem Port, Catégorie: Modem
  Aucun port trouvé dans la catégorie Audio
  Aucun port trouvé dans la catégorie Diagnostic
```

### Obtention des ports par catégorie

```python
gps_ports = port_categorizer.get_ports_by_category("GPS")
for port in gps_ports:
    print(f"Port GPS trouvé : {port.device}")
```

Cette fonction retourne une liste de ports pour une catégorie donnée.

### Obtention du premier port d'une catégorie

```python
at_port = port_categorizer.get_port("AT")
if at_port:
    print(f"Premier port AT trouvé : {at_port}")
else:
    print("Aucun port AT trouvé")
```

Cette fonction retourne le nom du premier port trouvé pour une catégorie spécifique.

### Utilisation dans un script principal

```python
def main():
    port_categorizer = SerialPortCategorizer()
    
    # Afficher tous les ports catégorisés
    port_categorizer.display_ports()
    
    # Obtenir et afficher le port GPS
    gps_port = port_categorizer.get_port("GPS")
    print(f"Port GPS : {gps_port}")
    
    # Obtenir et afficher le port AT
    at_port = port_categorizer.get_port("AT")
    print(f"Port AT : {at_port}")
    
    # Obtenir et afficher tous les ports modem
    modem_ports = port_categorizer.get_ports_by_category("MODEM")
    print("Ports Modem :")
    for port in modem_ports:
        print(f"  {port.device}")

if __name__ == "__main__":
    main()
```

Ce script principal démontre l'utilisation de toutes les fonctions de la classe SerialPortCategorizer, en affichant les ports catégorisés, en obtenant des ports spécifiques, et en listant tous les ports d'une catégorie donnée.
<br>
## SIM7600Info Class Documentation

La classe `SIM7600Info` permet d'interagir avec le module SIM7600 et de récupérer des informations telles que la version du firmware, le fabricant, le numéro de série, la version du module, les informations sur la puce, et d'autres détails pertinents.

### Héritage

Cette classe hérite de la classe `SIM7600`.

### Constructeur

#### `__init__(self, port, baudrate=115200, timeout=2)`

Initialise une instance de `SIM7600Info`.

#### Paramètres
- `port` (str): Le port série à utiliser pour la communication avec le module SIM7600.
- `baudrate` (int, optionnel): La vitesse de transmission (défaut: 115200).
- `timeout` (int, optionnel): Le délai d'attente pour les opérations de communication (défaut: 2 secondes).

#### Exemple
```python
sim7600 = SIM7600Info(port="COM17")
```



### Version du firmware

Récupère la version du firmware du module SIM7600.


#### Exemple
```python
version = sim7600.get_firmware_version()
print("Version du firmware:", version)
```

### Nom du fabricant 

Récupère le nom du fabricant du module SIM7600.


#### Exemple
```python
manufacturer = sim7600.get_manufacturer()
print("Fabricant:", manufacturer)
```

### Lecture du numéro de série de série 

Récupère le numéro de série du module SIM7600.


#### Exemple
```python
serial_number = sim7600.get_serial_number()
print("Numéro de série:", serial_number)
```

### Lecture du numéro de version du module

Récupère la version du module SIM7600 sous forme de chaîne

#### Exemple
```python
module_version = sim7600.get_module_version()
print("Version du module:", module_version)
```

### Lecture des informations de la puce

Récupère les informations de la puce du module SIM7600, y compris la version du sous-système et la version du modem sous forme de dictionnaire


#### Exemple
```python
chip_info = sim7600.get_chip_info()
print("Informations de la puce: numéro de sub version", chip_info['sub_version')
print("Informations de la puce: numéro du modem version", chip_info['modem_version')
```

### Récupération du modèle , le numéro de révision et l'IMEI 

Récupère des informations complètes sur le module SIM7600, y compris le modèle, la révision et l'IMEI.


#### Exemple
```python
full_info = sim7600.get_full_info()
print("Modèle: ", full_info['Modèle'])
print("Révision: ", full_info['Révision'])
print("IMEI: ", full_info['IMEI'])
```

### Afficher toutes les informations

Affiche toutes les informations du module SIM7600 en utilisant le module de logging.

#### Exemple
```python
sim7600.print_all_info()
```

## Exemple d'utilisation

Voici un exemple complet d'utilisation de la classe `SIM7600Info` :

```python
import logging
from SIM7600Info import SIM7600Info

# Configurer le logging
logging.basicConfig(level=logging.INFO)

def main():
    sim_info = SIM7600Info(port="COM17")
    
    try:
        sim_info.open_connection()
        logging.info("Connexion réussie.")
        sim_info.print_all_info()
    except Exception as e:
        logging.error(f"Erreur: {e}")
    finally:
        sim_info.close_connection()

if __name__ == "__main__":
    main()
```

## Notes

- Assurez-vous que le port série est correctement configuré et que le module SIM7600 est connecté avant d'exécuter le script.
- Les méthodes de cette classe reposent sur des commandes AT pour interagir avec le module, donc le module doit être compatible avec les commandes AT standard.



