import pyautogui
from datetime import datetime
from pathlib import Path
import time


class ScreenshotSubModule:

    def take_screenshot(self, task):
        time.sleep(2)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = Path.home() / "Downloads" / f"screenshot_{timestamp}.png"

        ss = pyautogui.screenshot()
        ss.save(path)
        return "Screenshot saved in Downloads folder."
