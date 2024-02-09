import os

from smart_config import ConfigLoader


class Utility:
    environment = {}

    @staticmethod
    def load_environment(env="system_file"):
        """
        Loads the environment variables and their values from the
        system.yaml file for defining the working environment of the app

        :return: None
        """
        Utility.environment = ConfigLoader(os.getenv(env, "/home/nupur_khare/PycharmProjects/Library/system.yaml")).get_config()
