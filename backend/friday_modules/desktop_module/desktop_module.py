from backend.friday_modules.desktop_module.power_sub_module import PowerSubModule
from backend.friday_modules.desktop_module.file_operations_sub_module import (
    FileOperationsSubModule,
)
from backend.friday_modules.desktop_module.screenshot_sub_module import (
    ScreenshotSubModule,
)
from .app_registry import registry

import screen_brightness_control as sbc
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
            "shutdown": self.power.execute,
            "restart": self.power.execute,
            "lock": self.power.execute,
            "sleep": self.power.execute,
            "hibernate": self.power.execute,
            "take_screenshot": self.screenshot.execute,
            "create_file": self.file.execute,
            "create_folder": self.file.execute,
            "open_file": self.file.execute,
            "open_folder": self.file.execute,
            "delete_file": self.file.execute,
            "delete_folder": self.file.execute,
            "rename_file": self.file.execute,
            "rename_folder": self.file.execute,
            "close_file": self.file.execute,
            "move_folder": self.file.execute,
            "move_file": self.file.execute,
            "search_file": self.file.execute,
            "search_folder": self.file.execute,
            "open_local_app": self.open_local_app,
            "conversation": self.conversation,
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

    def execute(self, task):
        action = self.actions.get(task.action)
        if action:
            return action(task)
