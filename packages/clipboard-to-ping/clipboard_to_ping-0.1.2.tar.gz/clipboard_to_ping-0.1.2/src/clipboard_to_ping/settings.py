from pydantic import BaseModel

from wiederverwendbar.pydantic.file_config import FileConfig


class Settings(FileConfig):
    class Command(BaseModel):
        hotkey: str
        open: list[str]

    commands: dict[str, Command] = {}
