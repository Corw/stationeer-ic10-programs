import os
import settings


def get_scripts(path: str)-> list[str]:
    """Returns a list of all directories in the given path."""
    return [item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))]

def main():
    # get all script directories from settings configured directory
    script_directories = get_scripts(path=settings.SCRIPTS_DIR)
    # for each script directory check config if it is already there, if not add it to the config
    new_scripts = [
        script for script in script_directories if script not in [script_config.script_directory for script_config in settings.config.scripts_configs]
    ]

main()
