import os
import subprocess
from pathlib import Path
from tkinter import Tk

import pystray
from PIL import Image
import keyboard
from wiederverwendbar.functions.eval import eval_value

from clipboard_to_ping.settings import Settings

# get the source path
src_path = file_path = Path(os.path.abspath(__file__)).parent

# get the settings
settings = Settings(file_path=src_path / "settings.json")


def wrap_command(cn: str):
    def wrapped_command():
        # get the command from the settings
        command = settings.commands[cn]

        # release the hotkey
        keyboard.release(command.hotkey)

        # get clipboard
        keyboard.press("ctrl+c")
        keyboard.release("ctrl+c")
        clipboard = Tk().clipboard_get()

        # strip whitespace
        clipboard = clipboard.strip()

        # evaluate the command
        cmd = eval_value(f"Command '{cn}'", command.open, clipboard=clipboard)

        # run the command
        subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

    return wrapped_command


def main():
    # load the icon
    icon = Image.open(src_path / "icon.png")

    # create the tray icon
    tray = pystray.Icon("clipboard_to_ping",
                        title="Clipboard to Ping",
                        icon=icon,
                        menu=pystray.Menu(
                            pystray.MenuItem("Settings", lambda: os.system(f"start {settings.file_path}")),
                            pystray.MenuItem("Exit", lambda: tray.stop())
                        ))

    # get the hotkey from the settings
    for command_name, command in settings.commands.items():
        # wrap the command
        wrapped_command = wrap_command(command_name)
        keyboard.add_hotkey(command.hotkey, wrapped_command)

    # run the tray
    tray.run()


if __name__ == "__main__":
    main()
