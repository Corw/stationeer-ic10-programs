"""Takes name of the src script as input, find its configuration in config, coverts the script into xml format and stores the script in the
scrpts stores in in compatipble format in scripts path."""

import os

from settings import config
from tools.models.config import ScriptConfig
from tools.models.scripts import ScriptContent

from datetime import datetime, timezone


def current_ticks():
    epoch = datetime(1, 1, 1, tzinfo=timezone.utc)
    return int((datetime.now(timezone.utc) - epoch).total_seconds() * 10_000_000)


def convert_to_xml(content: ScriptContent) -> str:
    """Converts the src content to xml format."""
    result = (
        f'<?xml version="1.0" encoding="utf-8"?>"'
        f'<InstructionData xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
        f"<DateTime>{current_ticks()}</DateTime>"
        f"<GameVersion>0.2.5954.26176</GameVersion>"
        f"<Title>{content.name}</Title>"
        f"<Description>{content.description}</Description>"
        f"<Author>Corw</Author>"
        f"<WorkshopFileHandle>0</WorkshopFileHandle>"
        f"<Instructions>{content.source_code}</InstructionData>"
    )

    return result


def set_script_content(script: str, path_scripts: str, content: ScriptContent) -> None:
    """Sets the script content in the xml format and stores it in the scripts path."""
    script_dir_path = os.path.join(path_scripts, script)
    # check if script directory exists, if not create it
    if not os.path.exists(path=script_dir_path):
        os.makedirs(name=script_dir_path)

    script_path = os.path.join(script_dir_path, "instruction.xml")

    xml_content = convert_to_xml(content=content)
    with open(file=script_path, mode="w") as file:
        file.write(xml_content)


def export_script(script_file: str) -> None:
    """Exports the script in xml format and stores it in the scripts path."""
    # Get the script configuration from config
    script_config = next(
        (
            configuration
            for configuration in config.scripts_configs
            if configuration.name == script_file
        ),
        None,
    )

    if not script_config:
        name = script_file.capitalize().replace("_", " ").strip(".ic10")
        script_config = ScriptConfig(
            name=name,
            description=f"Exported script '{script_file}'",
            src_file=script_file,
            script_directory=name,
        )

    # Convert the script to xml format
    script_path = os.path.join(config.path_cm10_code, script_file)
    src_code = open(script_path, "r").read()

    script_content = ScriptContent(
        script_config.name,
        script_config.description,
        source_code=src_code,
    )

    # Store the xml content in the scripts path
    set_script_content(
        script=script_config.script_directory,
        path_scripts=config.path_scripts,
        content=script_content,
    )
    
    print(f"Script '{script_config.name}' exported successfully to '{config.path_scripts}'.")
