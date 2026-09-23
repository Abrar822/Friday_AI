import webbrowser
import pyautogui
import pyperclip
import time


class EmailGenerationModule:

    def compose_email(self, task):
        try:
            subject = task.parameters.subject
            body = task.parameters.body

            webbrowser.open("https://mail.google.com/mail/u/0/#inbox?compose=new")
            time.sleep(15)

            pyautogui.press("tab")
            pyperclip.copy(subject)
            pyautogui.hotkey("ctrl", "v")

            pyautogui.press("tab")
            pyperclip.copy(body)
            pyautogui.hotkey("ctrl", "v")
        except:
            return "Sorry, I could not generate the email"

    def execute(self, task):
        match task.action:
            case "compose_email":
                return self.compose_email(task)
