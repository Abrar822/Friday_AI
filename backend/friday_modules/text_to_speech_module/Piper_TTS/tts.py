import subprocess
import sounddevice as sd
import soundfile as sf
from ....helpers.clean_text import clean_text


class TextToSpeechModule:

    def tts(self, text: str):
        text = clean_text(text)
        PIPER_EXE = (
            r"backend\friday_modules\text_to_speech_module\Piper_TTS\piper\piper.exe"
        )
        MODEL = r"backend\friday_modules\text_to_speech_module\Piper_TTS\voices\en_US-hfc_female-medium.onnx"
        OUTPUT = "output.wav"

        subprocess.run(
            [
                PIPER_EXE,
                "--model",
                MODEL,
                "--output_file",
                OUTPUT,
            ],
            input=text,
            text=True,
            check=True,
        )

        audio, sample_rate = sf.read(OUTPUT)
        sd.play(audio, sample_rate)
        sd.wait()