## Module SIM 7600
<image src="https://github.com/user-attachments/assets/a084f882-9833-4f40-a591-5fafea92a3cc" height="250px">

Voici la description de la classe SIM7600 et ses principales fonctions en format Markdown :

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

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/19879401/4330e61b-6064-47a8-aab1-ac3710d02148/paste.txt
