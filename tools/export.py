"""Takes name of the src script as input, find its configuration in config, coverts the script into xml format and stores the script in the
scrpts stores in in compatipble format in scripts path."""

import os

import settings
from models.config import ScriptConfig
from models.scripts import ScriptContent

from datetime import datetime, timezone
from xml.sax.saxutils import escape


def current_ticks():
    epoch = datetime(1, 1, 1, tzinfo=timezone.utc)
    return int((datetime.now(timezone.utc) - epoch).total_seconds() * 10_000_000)


def convert_to_xml(content: ScriptContent) -> str:
    """Convert a :class:`ScriptContent` to the expected XML string."""

    dticks = current_ticks()
    title = escape(content.name)
    description = escape(content.description)
    instructions = escape(content.source_code)

    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<InstructionData xmlns:xsd="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
        f"  <DateTime>{dticks}</DateTime>",
        "  <GameVersion>0.2.5954.26176</GameVersion>",
        f"  <Title>{title}</Title>",
        f"  <Description>{description}</Description>",
        "  <Author>Corw</Author>",
        "  <WorkshopFileHandle>0</WorkshopFileHandle>",
        f"  <Instructions>{instructions}</Instructions>",
        "</InstructionData>",
    ]

    return "\n".join(lines)


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
            for configuration in settings.config.scripts_configs
            if configuration.src_file == script_file
        ),
        None,
    )

    if not script_config:
        print(f"Script configuration for '{script_file}' not found in config. Using default configuration.")
        name = script_file.capitalize().replace("_", " ").strip(".ic10")
        script_config = ScriptConfig(
            name=name,
            description=f"Exported script '{script_file}'",
            src_file=script_file,
            script_directory=name,
        )
        settings.config.scripts_configs.append(script_config)

    # Convert the script to xml format
    script_path = os.path.join(settings.config.path_cm10_code, script_file)
    print(f"Reading source code from '{script_path}'...")
    src_code = open(script_path, "r").read().strip()
    if len(src_code) > 4096:
        raise ValueError(f"The source code of '{script_file}' is too long. Please check the file size and content.")

    script_content = ScriptContent(
        name=script_config.name,
        description=script_config.description,
        source_code=src_code,
    )

    # Store the xml content in the scripts path
    print(f"Exporting script '{script_config.name}' to '{settings.config.path_scripts}'...")
    set_script_content(
        script=script_config.script_directory,
        path_scripts=settings.config.path_scripts,
        content=script_content,
    )

    print(f"Script '{script_config.name}' exported successfully to '{settings.config.path_scripts}'.")

    print(f"Updating config with script '{script_config.name}'...")
    settings.save_config()

# export_script(script_file="test.ic10")

# read input from terminal
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Export a script to the scripts path.")
    parser.add_argument("script_file", type=str, help="The name of the script file to export (e.g. 'test.ic10').")
    args = parser.parse_args()
    print(f"Exporting script '{args.script_file}'...")
    export_script(script_file=args.script_file)