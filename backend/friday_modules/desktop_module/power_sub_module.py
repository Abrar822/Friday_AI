import subprocess


class PowerSubModule:

    def perform_shutdown(self, task):
        subprocess.run(["shutdown", "/s", "/t", "0"])
        return

    def perform_restart(self, task):
        subprocess.run(["shutdown", "/r", "/t", "0"])
        return

    def perform_locking(self, task):
        subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
        return

    def perform_sleep(self, task):
        subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"])
        return

    def perform_hibernation(self, task):
        subprocess.run(["shutdown", "/h"])
        return
