import serial.tools.list_ports


def categorize_ports():
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("Aucun port COM trouvé.")
        return

    categorized_ports = {
        "Audio": [],
        "GPS": [],
        "Diagnostic": [],
        "AT": [],
        "Modem": []
    }

    for port in ports:
        if "audio" in port.description.lower():
            categorized_ports["Audio"].append(port)
        elif "nmea" in port.description.lower():
            categorized_ports["GPS"].append(port)
        elif "diagnostic" in port.description.lower():
            categorized_ports["Diagnostic"].append(port)
        elif "at" in port.description.lower():
            categorized_ports["AT"].append(port)
        elif "modem" in port.description.lower():
            categorized_ports["Modem"].append(port)

    print("Ports COM catégorisés :")
    for category, ports_list in categorized_ports.items():
        if ports_list:
            for port in ports_list:
                print(f'  Nom du port: {port.device}, Description: {port.description}, Catégorie: {category}')
        else:
            print(f"  Aucun port trouvé dans la catégorie {category}")

    return categorized_ports  # Retourner les ports catégorisés


def get_ports_by_category(categorized_ports, category):
    return categorized_ports.get(category, [])


if __name__ == "__main__":
    categorized_ports = categorize_ports()

    # Exemple d'utilisation pour récupérer les ports de la catégorie "Audio"
    audio_ports = get_ports_by_category(categorized_ports, "Audio")
    if audio_ports:
        print("\nPorts Audio trouvés :")
        for port in audio_ports:
            print(f'  Nom du port: {port.device}, Description: {port.description}')
    else:
        print("Aucun port Audio trouvé.")
