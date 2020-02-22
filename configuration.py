import configparser


class Props:
    def __init__(self):
        self.filename = 'rzd_converter.conf'
        self.cfgParser = configparser.ConfigParser()

    def load(self):
        self.cfgParser.read(self.filename)

    def get_loglvl(self):
        return self.cfgParser.get('log', 'loglevel')

    def get_logconsole(self):
        return self.cfgParser.getboolean('log', 'console')


if __name__ == '__main__':
    # генерируем дефолтный конфиг
    config = configparser.ConfigParser()
    config['log'] = {}
    config['log']['loglevel'] = 'INFO'
    config['log']['console'] = 'yes'

    with open('rzd_converter.conf', 'w') as configfile:
        config.write(configfile)
