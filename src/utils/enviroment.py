import configparser
import pathlib


class EnvironmentVariables:

    CONFIG_PATH = pathlib.Path(__file__).parent.parent.parent.joinpath("config.ini")
    __instance = None

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_PATH)
        self.config = config

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(EnvironmentVariables)
        return cls.__instance

    def get(self, section, option):
        return self.config.get(section, option)
