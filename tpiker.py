import os
import shutil


def read_config():
    config = {}
    with open('tpicker.conf', 'r') as file:
        for line in file:
            line = line.strip()
            try:
                key, value = line.split('=')
                config[key] = value
            except:
                if not line.startswith("#"):
                    print(f"Warning : tpicker.conf contains an unknown statement : {line}")
    return config


def remove_existing_tree_and_copy(source, destination):
    if os.path.exists(destination):  # Remove the currently existing backup directory so that copytree
        shutil.rmtree(destination)   # doesn't throw a FileExistsError.
    shutil.copytree(source, destination)


def is_valid_path(path):
    """
    Check if a string is a valid OS path.
    """
    try:
        return os.path.normpath(path) == path
    except Exception as e:
        return False


class InvalidPathException(Exception):
    pass

class InvalidThemeException(Exception):
    pass


"""
Represents a configuration of the rice. Links the location of a configuration file to the location of the variants
of this file defined by each theme. Call the apply function to copy the configuration file of the target theme
to the live location.
"""
class Config:
    def __init__(self, running_directory, theme_directory):
        """
        :param running_directory: The directory of the live config.
        :param theme_directory: The directory of the config within a theme directory.
        Example : kitty's running directory is '<your_home>/.config/kitty' and its theme directory could be 'kitty'.
        You can define the theme directory of a config to be whatever you want since its content will be copied but
        not the directory itself.
        """
        if not is_valid_path(running_directory):
            raise InvalidPathException(f"Invalid path (running_directory) : {running_directory}")
        if not is_valid_path(theme_directory):
            raise InvalidPathException(f"Invalid path (theme_directory) : {theme_directory}")
        self.running_directory = running_directory
        self.theme_directory = theme_directory

    def apply(self, theme):
        """
        Copy the content of the config directory of the target theme to the live config directory.
        Creates a backup of the current config directory in /tmp/tpiker_backups/.
        """
        if theme not in THEMES:
            raise InvalidThemeException(f"Invalid theme : {theme}. Check that there exists a theme directory in {THEMES_DIRECTORY}.")
        # Create target directory if necessary
        os.makedirs(self.running_directory, exist_ok=True)
        # Create a backup of the current config
        backup_directory = '/tmp/tpiker_backups/' + self.running_directory
        backup_directory = backup_directory.replace('//', '/')
        remove_existing_tree_and_copy(self.running_directory, backup_directory)
        # Copy the theme file to the live location
        source_directory = f"{THEMES_DIRECTORY}/{theme}/{self.theme_directory}"
        source_directory = source_directory.replace('//', '/')
        remove_existing_tree_and_copy(source_directory, self.running_directory)


CONFIG = read_config()

THEMES_DIRECTORY = CONFIG['themes_directory']
THEMES = os.listdir(THEMES_DIRECTORY)
if len(THEMES) == 0:
    print(f"No themes defined. Current themes location : {THEMES_DIRECTORY}.")
    exit()
TARGET_THEME = CONFIG['target_theme']

# EXAMPLE :
# KITTY_CONFIG = Config('/home/username/.config/kitty', 'kitty')
# KITTY_CONFIG.apply(TARGET_THEME) # you could also use KITTY_CONFIG.apply('viking')
