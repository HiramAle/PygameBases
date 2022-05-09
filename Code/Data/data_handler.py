import configparser


def get_config(section: str, key: str):
    config = configparser.ConfigParser()
    if config.read("Data/config_data.ini"):
        if section in config:
            if key in config[section]:
                return config[section][key]
            else:
                print("Key not found")
        else:
            print("Section not found")
    else:
        print("File not found")
    return False


def set_config(section: str, key: str, value: str | int | float | bool):
    config = configparser.ConfigParser()
    if config.read("Data/config_data.ini"):
        config.set(section, key, str(value))
        with open('Data/config_data.ini', 'w') as configfile:
            config.write(configfile)
    else:
        print("File not found")


