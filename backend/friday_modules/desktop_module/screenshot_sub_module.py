import pyautogui
from datetime import datetime
from pathlib import Path
import time


class ScreenshotSubModule:

    def __init__(self):
        self.actions = {
            "take_screenshot": self.take_screenshot,
        }

    def take_screenshot(self, task):
        time.sleep(2)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = Path.home() / "Downloads" / f"screenshot_{timestamp}.png"

        ss = pyautogui.screenshot()
        ss.save(path)
        return "Screenshot saved in Downloads folder."

    def execute(self, task):
        action = self.actions.get(task.action)
        if action:
            return action(task)
