import os
import platform


def get_os():
    os_name = platform.system()
    return os_name


def custom_normpath(path: str) -> str:
    # Normalize the path
    normalized_path = os.path.normpath(path)
    plat = get_os()
    if plat == "Linux":
        # Replace backslashes with forward slashes for consistency
        return normalized_path.replace('\\', '/')
    # Replace forward slashes with backslashes for consistency
    return normalized_path.replace('/', '\\')