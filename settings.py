import yaml
from typing import Dict


class Stage:
    def __init__(self, data: dict) -> None:
        self.RAW = data

        self.NAME: str = self.RAW["name"]
        self.CHANNEL_ID: int = self.RAW["channel-id"]
        self.ASK_TO_SPEAK: bool = self.RAW.get("ask-to-speak", True)
        self.ASK_TO_LISTEN: bool = self.RAW.get("ask-to-listen", False)

        self.ROLE_IDS: Dict(str, int) = self.RAW.get("role-ids", {})
        self.ROLE_ID_ADMIN = self.ROLE_IDS.get("admin", None)
        self.ROLE_ID_SPEAKER = self.ROLE_IDS.get("speaker", None)
        self.ROLE_ID_LISTENER = self.ROLE_IDS.get("listener", None)
        self.ROLE_ID_BANNED = self.ROLE_IDS.get("banned", None)

    def as_dict(self):
        return {
            "name": self.NAME,
            "channel-id": self.CHANNEL_ID,
            "ask-to-speak": self.ASK_TO_SPEAK,
            "ask-to-listen": self.ASK_TO_LISTEN,
            "role-ids": {
                "admin": self.ROLE_ID_ADMIN,
                "speaker": self.ROLE_ID_SPEAKER,
                "listener": self.ROLE_ID_LISTENER,
                "banned": self.ROLE_ID_BANNED,
            },
        }


class Config:
    def __init__(self, path: str = "config.yml") -> None:
        self.PATH = path
        with open(path, "r", encoding="UTF-8") as file:
            self.RAW = yaml.load(file, yaml.Loader) or {}

        self.BOT_TOKEN = self.RAW.get("bot-token", None)
        self.GUILD_ID = self.RAW.get("guild-id", None)

        self.STAGES = [Stage(stage) for stage in self.RAW.get("stages", [])]
        self.update_stages_by_name()

    def update_stages_by_name(self):
        self.STAGES_BY_NAME = {stage.NAME: stage for stage in self.STAGES}

    def update_stages(self):
        self.STAGES = [stage for stage in self.STAGES_BY_NAME.values()]

    def as_dict(self):
        return {
            "bot-token": self.BOT_TOKEN,
            "guild-id": self.GUILD_ID,
            "stages": [stage.as_dict() for stage in self.STAGES],
        }

    def save(self):
        with open(self.PATH, "w", encoding="UTF-8") as file:
            yaml.dump(self.as_dict(), file, yaml.Dumper)
