# -*- coding: utf-8 -*-
import re

import socket
import os

class Config:
    config = dict()

    @staticmethod
    def load():
        dir_path = os.path.dirname(os.path.realpath(__file__))

        configFile = open(dir_path + "/resources/" + str(socket.gethostname()) + ".properties")

        with configFile as f:
            for line in f:
                splits = re.split('=|\n',line)
                Config.config[splits[0]] = splits[1]

    @staticmethod
    def get(key):
        if len(Config.config) == 0:
            Config.load()
        return Config.config[key]

    @staticmethod
    def get_default(key, default_value):
        try:
            if len(Config.config) == 0:
                Config.load()
        except:
            return default_value
        if not key in Config.config:
            return default_value
        return Config.get(key)