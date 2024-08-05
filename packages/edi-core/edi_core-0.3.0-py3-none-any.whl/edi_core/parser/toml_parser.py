import toml


def parse_toml_file(toml_file_path: str) -> dict:
    with open(toml_file_path, 'r') as file:
        return toml.load(file)


def parse_toml_str(toml_str: str) -> dict:
    return toml.loads(toml_str)


def save_to_toml_file(path: str, data: dict):
    with open(path, 'w') as file:
        toml.dump(data, file)
