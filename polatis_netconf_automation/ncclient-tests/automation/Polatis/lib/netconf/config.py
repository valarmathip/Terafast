import os
import ConfigParser
Config = ConfigParser.ConfigParser()

Config.read('config.txt')

def get_config_arg(opr, agrName):
    try:
        Name = Config.get(opr, agrName)
        return Name
    except Exception as err:
        return err



