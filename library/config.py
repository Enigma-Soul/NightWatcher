from json import loads,dumps

def load_config(path):
    with open(path, "r") as f:
        config = loads(f.read())
    return config
def save_config(path, config):
    with open(path, "w") as f:
        f.write(dumps(config, indent=4))
        f.close()
    return None