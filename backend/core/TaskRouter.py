from ..friday_modules.desktop_module.desktop_module import DesktopModule
from ..friday_modules.browser_module.browser_module import BrowserModule


class TaskRouter:
    def __init__(self):
        self.desktop = DesktopModule()
        self.browser = BrowserModule()
        self.modules = {
            "desktop": self.desktop,
            "browser": self.browser,
        }

    def execute(self, tasks):
        result = []
        for task in tasks:
            module = self.modules.get(task.module)
            if module:
                res = module.execute(task)
                if res:
                    result.append(res)
        return result
