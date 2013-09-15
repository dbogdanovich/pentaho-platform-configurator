from unittest import case

__author__ = 'Night'

import ConfigParser
from xml.etree.ElementTree import ElementTree


class Config:

    configFile = "./config.ini"
    oracle_hib_config = "system/hibernate/oracle10g.hibernate.cfg.xml"

    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.configFile)

    def _get_prop(self, prop_name):
        return self.config.get("settings", prop_name)

    def is_oracle(self):
        return self.db() == "Oracle"

    def home(self):
        return self._get_prop("home")

    def db(self):
        return self._get_prop("db")

    def db_host(self):
        return self._get_prop("host")

    def db_port(self):
        return self._get_prop("port")

    def db_sid(self):
        return self._get_prop("sid")

    def db_user(self):
        return self._get_prop("username")

    def db_pass(self):
        return self._get_prop("password")

    def db_connurl(self):
        if self.db() == "Oracle":
            return "jdbc:oracle:thin:@" + self.db_host() + ":" + self.db_port() + ":" + self.db_sid()
        else:
            raise Exception("Ouch, DB is not supported!")

    def hib_settings_file(self):
        return self.home() + "pentaho-solutions/system/hibernate/hibernate-settings.xml"

    def hib_rel_db_config_file(self):
        if self.is_oracle():
            path = self.oracle_hib_config
        return path

    def hib_full_db_config_file(self):
        if self.is_oracle():
            file = self.home() + "pentaho-solutions/" + self.oracle_hib_config
        return file

def config_quartz(filename, dbDelegaeClass):
    with open(filename, "r+") as file:
        lines = file.readlines()
        i = 0
        for line in lines:
            if line.strip().find("org.quartz.jobStore.driverDelegateClass") == 0:
                break
            i += 1
        lines[i] = "org.quartz.jobStore.driverDelegateClass = " + dbDelegaeClass + "\n"
        file.seek(0)
        file.truncate()
        file.writelines(lines)
        file.flush()
        print "Confige Quartz - success!"

def modify_hibernate_settings_file():
    tree = ElementTree()
    tree.parse(cfg.hib_settings_file())
    item = tree.find("config-file")
    item.text = cfg.hib_rel_db_config_file()
    tree.write(cfg.hib_settings_file())

def modify_hibernate_db_config_file():
    tree = ElementTree()
    tree.parse(cfg.hib_full_db_config_file())
    for item in tree.findall("*property"):
        name = item.attrib["name"]
        if name == "connection.url":
            item.text = cfg.db_connurl()
        elif name == "connection.username":
            item.text = cfg.db_user()
        elif name == "connection.password":
            item.text = cfg.db_pass()
    tree.write(cfg.hib_full_db_config_file())

def config_hibernate():
    modify_hibernate_settings_file()
    modify_hibernate_db_config_file()

cfg = Config()
config_hibernate()
# config_quartz(home + "pentaho-solutions/system/quartz/quartz.properties",  "org.quartz.impl.jdbcjobstore.oracle.OracleDelegate")

# def init_repository_oracle():




