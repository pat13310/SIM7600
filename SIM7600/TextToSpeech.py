import logging
import time

import vlc
from gtts import gTTS


class TextToSpeech:
    def __init__(self, lang='fr'):
        self.lang = lang
        self.audio_file=None

    def synthesize(self, text, output_file="output.mp3"):
        """Convertit du texte en parole et sauvegarde en tant que fichier MP3."""
        try:
            self.audio_file = output_file
            tts = gTTS(text=text, lang=self.lang)
            tts.save(output_file)
            logging.info("Synthèse vocale réussie, fichier généré.")
            return self
        except Exception as e:
            logging.error(f"Erreur lors de la synthèse vocale : {e}")
            return None

    def play(self):
        # Créer un instance de lecteur VLC
        player = vlc.MediaPlayer(self.audio_file)

        # Démarrer la lecture
        player.play()

        # Attendre que la lecture commence
        time.sleep(1)  # Donne le temps au lecteur de démarrer

        # Boucle jusqu'à ce que la lecture soit terminée
        while player.is_playing():
            time.sleep(1)

    def say(self, text):
        self.synthesize(text)
        self.play()

def main():
    tts=TextToSpeech()
    tts.synthesize("Bonjour je suis votre assistant vocal").play()



if __name__ == '__main__':
    main()
