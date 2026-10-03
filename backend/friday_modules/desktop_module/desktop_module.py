from backend.friday_modules.desktop_module.power_sub_module import PowerSubModule
from backend.friday_modules.desktop_module.file_operations_sub_module import (
    FileOperationsSubModule,
)
from backend.friday_modules.desktop_module.screenshot_sub_module import (
    ScreenshotSubModule,
)
from .app_registry import registry

import screen_brightness_control as sbc
import pyautogui
import pyperclip
import time
from pycaw.pycaw import AudioUtilities
import pythoncom
import subprocess
from difflib import SequenceMatcher


class DesktopModule:

    def __init__(self):
        self.power = PowerSubModule()
        self.file = FileOperationsSubModule()
        self.screenshot = ScreenshotSubModule()

        self.actions = {
            "set_volume": self.set_volume,
            "set_brightness": self.set_brightness,
            "perform_shutdown": self.power.perform_shutdown,
            "perform_restart": self.power.perform_restart,
            "perform_locking": self.power.perform_locking,
            "perform_sleep": self.power.perform_sleep,
            "perform_hibernation": self.power.perform_hibernation,
            "take_screenshot": self.screenshot.take_screenshot,
            "create_file": self.file.create_file,
            "create_folder": self.file.create_folder,
            "open_file": self.file.open_file,
            "open_folder": self.file.open_folder,
            "delete_file": self.file.delete_file,
            "delete_folder": self.file.delete_folder,
            "rename_file": self.file.rename_file,
            "rename_folder": self.file.rename_folder,
            "close_file": self.file.close_file,
            "move_folder": self.file.move_folder,
            "move_file": self.file.move_file,
            "search_file": self.file.search_file,
            "search_folder": self.file.search_folder,
            "open_local_app": self.open_local_app,
            "conversation": self.conversation,
            "paste": self.paste,
            "rename_folder_direct": self.file.rename_folder_direct,
            "delete_folder_direct": self.file.delete_folder_direct,
            "move_folder_direct": self.file.move_folder_direct
        }

    def normalise(self, s: str):
        return s.replace("_", "").replace("-", "").replace(" ", "").lower().strip()

    def open_local_app(self, task):
        app_name = task.parameters.display_name
        app_name = self.normalise(app_name)

        app_list = list(
            filter(
                lambda x: (app_name) in self.normalise(x["Name"])
                or (self.normalise(x["Name"])) in app_name,
                registry.registry,
            )
        )

        if app_list:
            candidates = []
            for app in app_list:
                score = SequenceMatcher(
                    None, app_name, self.normalise(app["Name"])
                ).ratio()
                candidates.append((score, app["AppID"]))
            candidates.sort(key=lambda x: x[0], reverse=True)

            app_id = candidates[0][1]
            subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{app_id}"])
            return

        return f"'{app_name}' not installed on the machine."

    def conversation(self, task):
        pass

    def set_volume(self, task):
        pythoncom.CoInitialize()
        level = task.parameters.level
        if level < 0:
            level = 10
        elif level > 100:
            level = 100

        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        volume.SetMute(False, None)
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
        pythoncom.CoUninitialize()

    def set_brightness(self, task):
        level = task.parameters.level
        level = max(0, min(level, 100))

        sbc.set_brightness(level)

    def paste(self, task):
        try:
            content = task.parameters.content
            pyperclip.copy(content)
            pyautogui.hotkey("ctrl", "v")
            return "Pasted successfully."
        except:
            return "Failed to paste the content."

    def execute(self, task):
        action = self.actions.get(task.action)
        if action:
            return action(task)
