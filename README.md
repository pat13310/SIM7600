## Module SIM 7600
<image src="https://github.com/user-attachments/assets/a084f882-9833-4f40-a591-5fafea92a3cc" height="250px">

Voici la description de la classe SIM7600 et ses principales classes :

## Classe SIM7600

La classe SIM7600 est conçue pour interagir avec un modem SIM7600, permettant la gestion des communications cellulaires.


## Documentation des fonctions principales

### Initialisation

```python
sim7600 = SIM7600Cmd("COM17", baudrate=115200, timeout=2)
sim7600.open_connection()
```

Cette séquence initialise l'objet SIM7600Cmd et ouvre la connexion série.

### Vérification de la carte SIM

```python
if sim7600.check_sim_card():
    print("Carte SIM détectée et prête")
else:
    print("Problème avec la carte SIM")
```

Vérifie si une carte SIM est présente et fonctionnelle.

### Configuration du mode réseau

```python
from SIM7600Cmd import NetworkType

sim7600.set_network_mode(NetworkType.AUTO)
print(f"Mode réseau actuel : {sim7600.get_network_type_str()}")
```

Configure le mode réseau et affiche le mode actuel.

### Qualité du signal

```python
dbm, quality = sim7600.get_signal_quality()
print(f"Qualité du signal : {dbm} dBm ({quality})")
```

Récupère et affiche la qualité du signal en dBm avec une interprétation.

### Informations sur l'opérateur

```python
operator_info = sim7600.get_operator_info()
print(f"Informations opérateur : {operator_info}")
```

Obtient et affiche les informations sur l'opérateur réseau.

### Statut du réseau

```python
sim7600.print_network_status()
```

Affiche un résumé détaillé du statut réseau.

### Activation du GPS

```python
sim7600.enable_gps()
```

Active le module GPS.

### Réinitialisation du module

```python
sim7600.reset_module()
```

Réinitialise les configurations du modem.

### Fermeture de la connexion

```python
sim7600.close_connection()
```

Ferme la connexion série.

## Script complet

Voici un script complet qui utilise les fonctions principales :

```python
from SIM7600Cmd import SIM7600Cmd, NetworkType, setup_logging
import logging
import time

def main():
    setup_logging()
    sim7600 = SIM7600Cmd("COM17")
    
    try:
        sim7600.open_connection()
        logging.info("Connexion ouverte")

        if sim7600.check_sim_card():
            logging.info("Carte SIM détectée")
        else:
            logging.error("Problème avec la carte SIM")
            return

        sim7600.set_network_mode(NetworkType.AUTO)
        logging.info(f"Mode réseau : {sim7600.get_network_type_str()}")

        dbm, quality = sim7600.get_signal_quality()
        logging.info(f"Signal : {dbm} dBm ({quality})")

        operator_info = sim7600.get_operator_info()
        logging.info(f"Opérateur : {operator_info}")

        sim7600.print_network_status()

        sim7600.enable_gps()
        logging.info("GPS activé")

        time.sleep(10)  # Attente de 10 secondes

        sim7600.reset_module()
        logging.info("Module réinitialisé")

    except Exception as e:
        logging.error(f"Erreur : {e}")
    finally:
        sim7600.close_connection()
        logging.info("Connexion fermée")

if __name__ == "__main__":
    main()
```

Ce script démontre l'utilisation des principales fonctions de la classe SIM7600Cmd dans un scénario typique. Il initialise le module, vérifie la carte SIM, configure le réseau, obtient des informations sur le signal et l'opérateur, active le GPS, attend un peu, puis réinitialise le module. Le script gère également les exceptions et assure la fermeture de la connexion, même en cas d'erreur.
<br>

## Classe SIM7600Info

Voici la documentation révisée avec des exemples pour les fonctions principales de la classe SIM7600Info, suivie d'un script complet à la fin :

## Documentation des fonctions principales

### Initialisation

```python
sim_info = SIM7600Info("COM17", baudrate=115200, timeout=2)
sim_info.open_connection()
```

Cette séquence initialise l'objet SIM7600Info et ouvre la connexion série.

### Obtenir la version du firmware

```python
firmware_version = sim_info.get_firmware_version()
print(f"Version du firmware : {firmware_version}")
```

Récupère la version du firmware du module.

### Obtenir le fabricant

```python
manufacturer = sim_info.get_manufacturer()
print(f"Fabricant : {manufacturer}")
```

Récupère le nom du fabricant du module.

### Obtenir le numéro de série

```python
serial_number = sim_info.get_serial_number()
print(f"Numéro de série : {serial_number}")
```

Récupère le numéro de série du module.

### Obtenir la version du module

```python
module_version = sim_info.get_module_version()
print(f"Version du module : {module_version}")
```

Récupère la version du module.

### Obtenir les informations du chip

```python
chip_info = sim_info.get_chip_info()
print(f"Version du sous-système : {chip_info['sub_version']}")
print(f"Version du modem : {chip_info['modem_version']}")
```

Récupère les informations détaillées du chip.

### Obtenir les informations complètes

```python
full_info = sim_info.get_full_info()
print(f"Modèle : {full_info['Modèle']}")
print(f"Révision : {full_info['Révision']}")
print(f"IMEI : {full_info['IMEI']}")
```

Récupère les informations complètes du module, y compris le modèle, la révision et l'IMEI.

### Afficher toutes les informations

```python
sim_info.print_all_info()
```

Affiche toutes les informations du module de manière formatée.

## Script complet

Voici un script complet qui utilise les fonctions principales de la classe SIM7600Info :

```python
from SIM7600Info import SIM7600Info
import logging
from serial.serialutil import SerialException

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    setup_logging()
    ports_to_try = ["COM17", "COM18", "COM19"]  # Ajoutez d'autres ports si nécessaire
    sim_info = None

    for port in ports_to_try:
        try:
            sim_info = SIM7600Info(port)
            sim_info.set_echo_command(False)
            sim_info.open_connection()
            logging.info(f"Connexion réussie sur le port {port}.")
            break
        except SerialException as e:
            logging.warning(f"Le port {port} est indisponible: {e}")
        except Exception as e:
            logging.error(f"Erreur inattendue lors de l'ouverture du port {port}: {e}")

    if sim_info is None:
        logging.critical("Impossible de se connecter à un port série.")
        return

    try:
        # Récupération et affichage des informations individuelles
        logging.info(f"Version du firmware : {sim_info.get_firmware_version()}")
        logging.info(f"Fabricant : {sim_info.get_manufacturer()}")
        logging.info(f"Numéro de série : {sim_info.get_serial_number()}")
        logging.info(f"Version du module : {sim_info.get_module_version()}")

        chip_info = sim_info.get_chip_info()
        logging.info(f"Information du chip: sub version : {chip_info['sub_version']}")
        logging.info(f"Information du chip: modem version : {chip_info['modem_version']}")

        full_info = sim_info.get_full_info()
        logging.info(f"Modèle : {full_info['Modèle']}")
        logging.info(f"Révision : {full_info['Révision']}")
        logging.info(f"IMEI : {full_info['IMEI']}")

        # Affichage de toutes les informations en une fois
        logging.info("Affichage de toutes les informations :")
        sim_info.print_all_info()

    except Exception as er:
        logging.error(f"Erreur inattendue: {er}")
    finally:
        sim_info.close_connection()
        logging.info("Connexion fermée.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(f"Erreur non gérée: {e}")
```

Ce script démontre l'utilisation des principales fonctions de la classe SIM7600Info. Il tente de se connecter à différents ports série, récupère et affiche diverses informations sur le module SIM7600, et gère les exceptions potentielles. Le script utilise également la fonction `print_all_info()` pour afficher toutes les informations en une seule fois.
<br>

Voici la documentation révisée avec des exemples pour les fonctions principales de la classe SIM7600SMS, suivie d'une explication de son utilité :

## Classe SIM7600SMS

La classe SIM7600SMS est une extension de SIM7600Cmd spécialisée dans la gestion des SMS. Elle permet d'envoyer, lire et supprimer des SMS sur un module SIM7600.

### Initialisation

```python
sim_sms = SIM7600SMS("COM17", baudrate=115200, timeout=2)
sim_sms.open_connection()
```

Cette séquence initialise l'objet SIM7600SMS et ouvre la connexion série.

### Vérification de la carte SIM

```python
if sim_sms.check_sim_card():
    print("Carte SIM détectée et prête")
else:
    print("Problème avec la carte SIM")
```

Vérifie si une carte SIM est présente et fonctionnelle.

### Envoi d'un SMS

```python
response = sim_sms.send_sms("+33612345678", "Bonjour, ceci est un test.")
print(f"Réponse à l'envoi de SMS: {response}")
```

Envoie un SMS au numéro spécifié avec le message donné.

### Lecture des SMS

```python
messages = sim_sms.read_sms()
for sms in messages:
    print(f"De: {sms['phone_number']}, Date: {sms['date']}, Message: {sms['content']}")
```

Lit tous les SMS stockés sur la carte SIM.

### Suppression d'un SMS

```python
sim_sms.delete_sms(1)  # Supprime le SMS à l'index 1
```

Supprime un SMS spécifique par son index.

### Lecture et suppression des SMS

```python
messages = sim_sms.read_sms(delete_action=True)
for sms in messages:
    print(f"SMS lu et supprimé: {sms['content']}")
```

Lit tous les SMS et les supprime après lecture.

## Utilité de la classe SIM7600SMS

La classe SIM7600SMS est conçue pour simplifier la gestion des SMS sur un module SIM7600. Elle offre les fonctionnalités suivantes :

1. **Gestion des SMS** : Permet d'envoyer, lire et supprimer des SMS facilement.
2. **Décodage automatique** : Gère le décodage des messages, y compris pour les caractères non-ASCII.
3. **Vérification de la carte SIM** : S'assure que la carte SIM est présente et prête avant d'effectuer des opérations.
4. **Gestion des erreurs** : Inclut une gestion des erreurs pour les opérations liées aux SMS.
5. **Flexibilité** : Permet de lire les SMS avec ou sans suppression automatique.

Cette classe est particulièrement utile pour les projets IoT ou de télémétrie nécessitant une communication par SMS, comme les systèmes d'alerte, la surveillance à distance, ou la commande à distance via SMS.


<br>
Voici la documentation révisée avec des exemples pour les fonctions principales de la classe SIM7600GPS, suivie d'une explication de son utilité :

## Classe SIM7600GPS

La classe SIM7600GPS est une extension de SIM7600Cmd spécialisée dans la gestion du module GPS du SIM7600.

### Initialisation

```python
sim_gps = SIM7600GPS("COM17", baudrate=115200, timeout=2)
sim_gps.open_connection()
```

Cette séquence initialise l'objet SIM7600GPS et ouvre la connexion série.

### Récupération des données GPS

```python
gps_data = sim_gps.get_gps_data()
if gps_data:
    for data in gps_data:
        if len(data) > 16:
            print(data)
else:
    print("Aucune donnée GPS disponible")
```

Récupère les données GPS si disponibles.

### Vérification de l'état du GPS

```python
if sim_gps.is_ready():
    print("Le GPS a une position fixe")
else:
    print("Le GPS n'a pas encore de position fixe")
```

Vérifie si le GPS a une position fixe.

### Désactivation du GPS

```python
sim_gps.disable_gps()
```

Désactive le module GPS.

## Utilité de la classe SIM7600GPS

La classe SIM7600GPS est conçue pour simplifier l'utilisation du module GPS intégré au SIM7600. Elle offre les fonctionnalités suivantes :

1. **Gestion du GPS** : Permet d'activer, désactiver et récupérer les données GPS facilement.
2. **Vérification de l'état** : Fournit une méthode pour vérifier si le GPS a une position fixe.
3. **Traitement des données** : Gère le traitement initial des données GPS brutes.
4. **Intégration avec SIM7600Cmd** : Hérite des fonctionnalités de base de SIM7600Cmd pour une utilisation cohérente avec d'autres fonctionnalités du module.

Cette classe est particulièrement utile pour les projets nécessitant une localisation précise, comme :
- Le suivi de véhicules ou d'actifs
- Les applications de navigation
- La géolocalisation pour l'IoT
- La collecte de données géographiques

En simplifiant l'interface avec le module GPS du SIM7600, cette classe permet aux développeurs de se concentrer sur l'utilisation des données GPS plutôt que sur les détails de communication avec le matériel.

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/19879401/cdb8ba2d-61c6-4354-a7ea-7f3f08edf141/paste.txt
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/19879401/b5e71edf-6a37-4c41-807a-339d339e8955/paste.txt
## Matériels nécessaires
<image src="https://github.com/user-attachments/assets/0a546fb1-bd19-48cc-8baa-9fa6e748a9d2" height="200px">
<br>
💡 <b>Remarque</b> : Comme illustré sur l'image, il faudra rajouter l"antenne pour fixer correctement le signal GPS.<br>
Cette classe SIMGPS offre une interface simple pour gérer les fonctionnalités GPS d'un modem SIM7600, permettant une intégration facile dans des projets nécessitant des capacités de géolocalisation.
<br>


<br>
Voici la documentation révisée avec des exemples pour les fonctions principales de la classe SIM7600MQTT, suivie d'une explication de son utilité :

## SIM7600MQTT

La classe SIM7600MQTT étend SIM7600Cmd pour ajouter des fonctionnalités MQTT au module SIM7600.

### Initialisation

```python
sim_mqtt = SIM7600MQTT(port="COM17", apn="m2m.lebara.fr", broker="test.mosquitto.org", port_mqtt=1883)
```

Initialise l'objet SIM7600MQTT avec le port série, l'APN, l'adresse du broker MQTT et le port MQTT.

### Configuration de l'APN et connexion

```python
sim_mqtt.configure_apn()
ip = sim_mqtt.connect()
print(f"Adresse IP: {ip}")
```

Configure l'APN et établit une connexion de données GPRS.

### Connexion au broker MQTT

```python
sim_mqtt.connect_mqtt()
```

Connecte le client au broker MQTT spécifié.

### Publication d'un message

```python
sim_mqtt.publish("test/topic", "Hello, MQTT via SIM7600!")
```

Publie un message sur un topic MQTT spécifié.

### Fermeture des connexions

```python
sim_mqtt.close()
```

Ferme la connexion au broker MQTT et la connexion série.

## Utilité de la classe SIM7600MQTT

La classe SIM7600MQTT est conçue pour faciliter l'utilisation du protocole MQTT sur un module SIM7600. Elle offre les fonctionnalités suivantes :

1. **Gestion de la connexion cellulaire** : Configure l'APN et établit une connexion de données GPRS.
2. **Intégration MQTT** : Utilise la bibliothèque Paho MQTT pour gérer les communications MQTT.
3. **Simplicité d'utilisation** : Encapsule les détails de la connexion cellulaire et MQTT dans une interface simple.
4. **Callbacks personnalisables** : Permet de définir des comportements personnalisés pour les événements MQTT (connexion, réception de message, publication).

Cette classe est particulièrement utile pour :
- Les projets IoT nécessitant une communication MQTT sur réseau cellulaire
- La télémétrie à distance
- Les systèmes de contrôle et de surveillance utilisant MQTT comme protocole de communication

En combinant les fonctionnalités du module SIM7600 avec le protocole MQTT, cette classe permet de créer facilement des dispositifs IoT connectés capables de communiquer efficacement sur de longues distances via le réseau cellulaire.
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
