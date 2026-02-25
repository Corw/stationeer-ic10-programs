import os
import settings
from models import ScriptContent, ScriptConfig
from xml.etree import ElementTree



def get_scripts(path: str) -> list[str]:
    """Returns a list of all directories in the given path."""
    return [
        item for item in os.listdir(path) if os.path.isdir(os.path.join(path, item))
    ]


def get_script_content(script: str, path_scripts: str) -> ScriptContent:
    """Imports a script.

    Add script to a config, extract cm10 code from the file and creates a cm10 code file.
    """
    script_path = os.path.join(path_scripts, script, "instruction.xml")
    if not os.path.exists(script_path):
        raise ValueError(f"Script {script} does not have an instruction.xml file.")

    # script is and xml file, we need to extract followingbelements:
    # InstructionData/Title
    # InstructionData/Description
    # InstructionData/Instructions
    tree = ElementTree.parse(source=script_path)
    root = tree.getroot()
    title = root.find("Title").text
    description = root.find("Description").text.replace("\u200b", "")
    instructions = root.find("Instructions").text

    result = ScriptContent(name=title, description=description, source_code=instructions)
    return result

def store_script_source(script_source: str, path_cm10_code: str):
    """Stores the source code of a script to a file."""
    with open(path_cm10_code, "w") as f:
        f.write(script_source)

def main():
    # get all script directories from settings configured directory
    script_directories = get_scripts(path=settings.scripts_dir)
    # for each script directory check config if it is already there, if not add it to the config
    new_scripts = [
        script
        for script in script_directories
        if script
        not in [
            script_config.script_directory
            for script_config in settings.config.scripts_configs
        ]
    ]

    print(f"Found {len(new_scripts)} new scripts: {new_scripts}")

    # store script code to code file and config
    for new_script in new_scripts:
        script_content = get_script_content(script=new_script, path_scripts=settings.config.path_scripts)

        script_source_file = f"{script_content.name.lower().replace(' ', '_')}.ic10"
        script_source_path = os.path.join(settings.config.path_cm10_code, script_source_file)

        store_script_source(script_source=script_content.source_code, path_cm10_code=script_source_path)

        settings.config.scripts_configs.append(
            ScriptConfig(
                name=script_content.name,
                description=script_content.description,
                src_file=script_source_file,
                script_directory=new_script,
            )
        )
    
    settings.save_config()


main()
