# import subprocess
# import sounddevice as sd
# import soundfile as sf
# from ....helpers.clean_text import clean_text


# class TextToSpeechModule:

#     def tts(self, text: str):
#         text = clean_text(text)
#         PIPER_EXE = (
#             r"backend\friday_modules\text_to_speech_module\Piper_TTS\piper\piper.exe"
#         )
#         MODEL = r"backend\friday_modules\text_to_speech_module\Piper_TTS\voices\en_US-hfc_female-medium.onnx"
#         OUTPUT = "output.wav"

#         subprocess.run(
#             [
#                 PIPER_EXE,
#                 "--model",
#                 MODEL,
#                 "--output_file",
#                 OUTPUT,
#             ],
#             input=text,
#             text=True,
#             check=True,
#         )

#         audio, sample_rate = sf.read(OUTPUT)
#         sd.play(audio, sample_rate)
#         sd.wait()


import subprocess
import sys
from pathlib import Path

import sounddevice as sd
import soundfile as sf

from ....helpers.clean_text import clean_text


class TextToSpeechModule:

    def tts(self, text: str):
        text = clean_text(text)

        if getattr(sys, "frozen", False):
            # Production: resources are bundled alongside FridayBackend.
            resources_dir = Path(sys.executable).resolve().parent.parent

            piper_dir = (
                resources_dir
                / "backend"
                / "friday_modules"
                / "text_to_speech_module"
                / "Piper_TTS"
            )
        else:
            # Development: this file is inside the Piper_TTS directory.
            piper_dir = Path(__file__).resolve().parent

        # Correct paths based on your actual folder structure.
        piper_exe = piper_dir / "piper" / "piper.exe"
        model_path = (
            piper_dir
            / "voices"
            / "en_US-hfc_female-medium.onnx"
        )

        # Save generated audio in a writable directory.
        output_dir = Path.home() / "Friday"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "output.wav"

        if not piper_exe.is_file():
            raise FileNotFoundError(
                f"Piper executable not found: {piper_exe}"
            )

        if not model_path.is_file():
            raise FileNotFoundError(
                f"Piper voice model not found: {model_path}"
            )

        result = subprocess.run(
            [
                str(piper_exe),
                "--model",
                str(model_path),
                "--output_file",
                str(output_path),
            ],
            input=text,
            text=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            check=False,
            creationflags=(
                subprocess.CREATE_NO_WINDOW
                if sys.platform == "win32"
                else 0
            ),
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Piper failed with exit code {result.returncode}: "
                f"{result.stderr}"
            )

        if not output_path.is_file():
            raise FileNotFoundError(
                f"Piper did not generate audio: {output_path}"
            )

        audio, sample_rate = sf.read(str(output_path))
        sd.play(audio, sample_rate)
        sd.wait()
