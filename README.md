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
Voici la description de la classe SIMGPS et ses principales fonctions en format Markdown :

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
> **Note :** Comme illustré sur l'image, il faudra rajouter l"antenne pour fixer correctement le signal GPS.

Cette classe SIMGPS offre une interface simple pour gérer les fonctionnalités GPS d'un modem SIM7600, permettant une intégration facile dans des projets nécessitant des capacités de géolocalisation.

