import serial.tools.list_ports
from enum import Enum

class PortCategory(Enum):
    AUDIO = "Audio"
    GPS = "GPS"
    DIAGNOSTIC = "Diagnostic"
    AT = "AT"
    MODEM = "Modem"

class SerialPortCategorizer:
    def __init__(self):
        """Initialise le catégoriseur de ports série et catégorise les ports disponibles."""
        self.categorized_ports = {category: [] for category in PortCategory}
        self.categorize_ports()

    def categorize_ports(self):
        """Catégorise les ports série disponibles en fonction de leur description."""
        ports = serial.tools.list_ports.comports()

        if not ports:
            print("Aucun port COM trouvé.")
            return

        for port in ports:
            if "audio" in port.description.lower():
                self.categorized_ports[PortCategory.AUDIO].append(port)
            elif "nmea" in port.description.lower():
                self.categorized_ports[PortCategory.GPS].append(port)
            elif "diagnostic" in port.description.lower():
                self.categorized_ports[PortCategory.DIAGNOSTIC].append(port)
            elif "at" in port.description.lower():
                self.categorized_ports[PortCategory.AT].append(port)
            elif "modem" in port.description.lower():
                self.categorized_ports[PortCategory.MODEM].append(port)

        #self.display_ports()

    def display_ports(self):
        """Affiche les ports série catégorisés."""
        print("Ports COM catégorisés :")
        for category, ports_list in self.categorized_ports.items():
            if ports_list:
                for port in ports_list:
                    print(f'  Nom du port: {port.device}, Description: {port.description}, Catégorie: {category.value}')
            else:
                print(f"  Aucun port trouvé dans la catégorie {category.value}")

    def get_ports_by_category(self, category):
        """Retourne la liste des ports pour une catégorie donnée."""
        try:
            category_enum = PortCategory[category.upper()]
            return self.categorized_ports.get(category_enum, [])
        except KeyError:
            print(f"Catégorie '{category}' non trouvée.")
            return []

    def get_port(self, categorie):
        """Retourne le nom du premier port trouvé dans la catégorie donnée."""
        try:
            category_enum = PortCategory[categorie.upper()]
            ports = self.categorized_ports.get(category_enum, [])
            if ports:
                return ports[0].device  # Renvoie le nom du premier port (ex : 'COM13')
            else:
                return None  # Aucun port trouvé dans cette catégorie
        except KeyError:
            return None  # Catégorie non trouvée

if __name__ == "__main__":
    port_categorizer = SerialPortCategorizer()
    category = "gps"
    port = port_categorizer.get_port(category)
    print(f"\nPort '{category.upper()}' trouvé : {port}")
