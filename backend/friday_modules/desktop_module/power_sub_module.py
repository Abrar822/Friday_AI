import subprocess


class PowerSubModule:
    def __init__(self):
        self.actions = {
            "perform_shutdown": self.perform_shutdown,
            "perform_restart": self.perform_restart,
            "perform_locking": self.perform_locking,
            "perform_sleep": self.perform_sleep,
            "perform_hibernation": self.perform_hibernation,
        }

    def perform_shutdown(self):
        # subprocess.run(["shutdown", "/s", "/t", "0"])
        print('shutting device')

    def perform_restart(self):
        # subprocess.run(["shutdown", "/r", "/t", "0"])
        print('restarting device')

    def perform_locking(self):
        # subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        print('locking device')

    def perform_sleep(self):
        # subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        print('sleeping device')

    def perform_hibernation(self):
        # subprocess.run(["shutdown", "/h"])
        print('hibernating device')

    def execute(self, task):
        action = self.actions.get(task.action)
        if action:
            return action()
