import serial
import pyaudio

from SerialPortCategorizer import SerialPortCategorizer


class SIM7600Audio:
    def __init__(self, at_port='COM17', audio_port='COM15', baudrate=115200):
        # Initialisation des ports série
        self.stream_out = None
        self.s_AT = serial.Serial(at_port, baudrate)
        self.s_Audio = serial.Serial(audio_port, baudrate)

        # Initialisation de PyAudio
        self.p = pyaudio.PyAudio()

    def send_at_command(self, command):
        """Envoie une commande AT et retourne la réponse."""
        if self.s_AT.is_open:
            command_to_send = command.strip() + '\r\n'
            self.s_AT.write(command_to_send.encode())
            print(f"Command sent: {command}")
            return self.read_response()
        else:
            print("AT port is not open.")
            return None

    def read_response(self):
        """Lit la réponse du module après l'envoi d'une commande AT."""
        response = ""
        while True:
            if self.s_AT.in_waiting:
                response += self.s_AT.read(self.s_AT.in_waiting).decode()
                if 'OK' in response or 'ERROR' in response:
                    break
        print(f"Response: {response}")
        return response

    def start_audio_stream(self):
        """Démarre le streaming audio entre le microphone et le module."""
        self.stream_out = self.p.open(format=self.p.get_format_from_width(2),
                                      channels=1,
                                      rate=8000,
                                      output=True)

        self.stream_in = self.p.open(format=self.p.get_format_from_width(2),
                                     channels=1,
                                     rate=8000,
                                     input=True,
                                     stream_callback=self.pcm_out)

        self.stream_in.start_stream()

    def pcm_out(self, in_data, frame_count, time_info, status):
        """Callback pour rediriger le flux audio vers le module."""
        self.s_Audio.write(in_data)
        return (in_data, pyaudio.paContinue)

    def close(self):
        """Ferme les ports série et les flux audio."""
        if self.s_AT.is_open:
            self.s_AT.close()
        if self.s_Audio.is_open:
            self.s_Audio.close()
        if self.stream_in.is_active():
            self.stream_in.stop_stream()
            self.stream_in.close()
        if self.stream_out.is_active():
            self.stream_out.stop_stream()
            self.stream_out.close()
        self.p.terminate()
        print("Resources closed.")


# Utilisation de la classe
if __name__ == "__main__":
    serializer=SerialPortCategorizer()
    data=serializer.get_port("AT")
    audio=serializer.get_port("audio")
    if audio is None:
        exit(0)
    sim7600_audio = SIM7600Audio(at_port=data, audio_port=audio)
    try:
        sim7600_audio.send_at_command("AT")  # Envoyer une commande AT pour tester
        sim7600_audio.start_audio_stream()  # Démarrer le streaming audio

        # Reste du traitement
        while True:
            pass  # Logique principale

    except KeyboardInterrupt:
        sim7600_audio.close()
