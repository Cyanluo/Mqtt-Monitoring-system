import configparser
from os import path

class CfgInfo:
    def __init__(self):
        self.log_configPath = path.join(path.dirname(path.abspath(__file__)), "../config/logger.conf")
        self.mqtt_configPath = path.join(path.dirname(path.abspath(__file__)), "../config/mqtt.conf")

    def get_mqtt_cfg(self):
        cfg_info = dict()
        conf = configparser.ConfigParser()

        conf.read(self.mqtt_configPath, encoding="utf-8")
        sections = conf.sections()
        for s in sections:
            cfg_info[s] = dict(conf.items(s))

        return cfg_info

    def get_mqtt_address(self):
        return self.get_mqtt_cfg()["address"]

    def get_mqtt_server_topic(self):
        return self.get_mqtt_cfg()["topic-server"]

    def get_mqtt_client_topic(self):
        return self.get_mqtt_cfg()["topic-client"]


if __name__ == '__main__':
    cfg = CfgInfo()
    print(cfg.get_mqtt_address())
