import re


class NMEParser():
    def __init__(self):
        print('NMEParser')
        pass

    def parse_gga(self, nmea_sentence):
        """Analyse une trame GGA et retourne un dictionnaire de données."""
        gga_regex = r'^\$GNGGA,(\d{6}\.\d{2}),([\d.]+),([NS]),([\d.]+),([EW]),(\d),(\d+),([\d.]+),([M]),([\d.]+),([M]),(\d{1,2})'
        match = re.match(gga_regex, nmea_sentence)

        if match:
            return {
                'time': match.group(1),
                'latitude': match.group(2),
                'lat_direction': match.group(3),
                'longitude': match.group(4),
                'lon_direction': match.group(5),
                'fix_quality': match.group(6),
                'satellites': match.group(7),
                'hdop': match.group(8),
                'altitude': match.group(9),
                'altitude_unit': match.group(10),
                'geoidal_separation': match.group(11),
                'geoidal_separation_unit': 'M',
                'age_of_diff_corr': match.group(12),
            }
        return None

    def parse_rmc(self, nmea_sentence):
        """Analyse une trame RMC et retourne un dictionnaire de données."""
        rmc_regex = r'^\$GNRMC,(\d{6}\.\d{2}),([AV]),([\d.]+),([NS]),([\d.]+),([EW]),([\d.]+),([\d.]+),(\d{6})'
        match = re.match(rmc_regex, nmea_sentence)

        if match:
            return {
                'time': match.group(1),
                'status': match.group(2),
                'latitude': match.group(3),
                'lat_direction': match.group(4),
                'longitude': match.group(5),
                'lon_direction': match.group(6),
                'speed': match.group(7),  # Vitesse en nœuds
                'course': match.group(8),
                'date': match.group(9),  # Date au format DDMMYY
            }
        return None

    def parse_gsv(self, nmea_sentence):
        """Analyse une trame GSV et retourne un dictionnaire de données."""
        gsv_regex = r'^\$GNGSV,\d,\d,(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)'
        match = re.match(gsv_regex, nmea_sentence)

        if match:
            return {
                'total_messages': match.group(1),
                'satellites_in_view': match.group(2),
                'satellite_data': []  # Vous pouvez remplir cette liste avec des données satellites supplémentaires
            }
        return None

    def parse_gsa(self, nmea_sentence):
        """Analyse une trame GSA et retourne un dictionnaire de données."""
        gsa_regex = r'^\$GNGSA,A,\d+\,([\d,]+),([\d.]+),([\d.]+),([\d.]+),([\d.]+),([\d.]+),([\d.]+),([\d.]+),([\d.]+),([\d.]+)'
        match = re.match(gsa_regex, nmea_sentence)

        if match:
            return {
                'mode': match.group(1),
                'fix_type': match.group(2),
                'pdop': match.group(3),
                'hdop': match.group(4),
                'vdop': match.group(5),
                'satellites_used': match.group(6).split(','),
            }
        return None

    def parse_vtg(self, nmea_sentence):
        """Analyse une trame VTG et retourne un dictionnaire de données."""
        vtg_regex = r'^\$GNVTG,([\d.]+),(N),([\d.]+),(K),([\d.]+),(M)'
        match = re.match(vtg_regex, nmea_sentence)

        if match:
            return {
                'track_angle': match.group(1),
                'track_unit': match.group(2),
                'speed_knots': match.group(3),
                'speed_kmh': match.group(4),
                'magnetic_variation': match.group(5),
            }
        return None

    def parse_gst(self, nmea_sentence):
        """Analyse une trame GST et retourne un dictionnaire de données."""
        gst_regex = r'^\$GNGST,(\d{6}\.\d{2}),([\d.]+),([\d.]+),([\d.]+),([\d.]+),([\d.]+)'
        match = re.match(gst_regex, nmea_sentence)

        if match:
            return {
                'time': match.group(1),
                'rms': match.group(2),
                'sigma_latitude': match.group(3),
                'sigma_longitude': match.group(4),
                'sigma_altitude': match.group(5),
                'geoidal_separation': match.group(6),
            }
        return None

    def parse(self, nmea_sentence):
        """Analyse une trame NMEA et retourne un dictionnaire de données approprié."""
        if nmea_sentence.startswith('$GNGGA'):
            return self.parse_gga(nmea_sentence)
        elif nmea_sentence.startswith('$GNRMC'):
            return self.parse_rmc(nmea_sentence)
        elif nmea_sentence.startswith('$GNGSV'):
            return self.parse_gsv(nmea_sentence)
        elif nmea_sentence.startswith('$GNGSA'):
            return self.parse_gsa(nmea_sentence)
        elif nmea_sentence.startswith('$GNVTG'):
            return self.parse_vtg(nmea_sentence)
        elif nmea_sentence.startswith('$GNGST'):
            return self.parse_gst(nmea_sentence)
        return None
