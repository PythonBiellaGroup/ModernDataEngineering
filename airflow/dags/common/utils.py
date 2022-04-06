import os


def check_if_file_exists(file):
    if os.path.exists(file) and os.path.isfile(file):
        return True
    else:
        return False
