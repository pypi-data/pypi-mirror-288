import platform


def get_platform():
    return platform.platform()


def get_system():
    return platform.system()


def is_windows():
    return get_system() == 'Windows'
