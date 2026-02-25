import pydantic

class ScriptConfig(pydantic.BaseModel):
    name: str
    description: str
    src_file: str
    script_directory: str

class Config(pydantic.BaseModel):
    path_cm10_code: str
    path_scripts: str
    scripts_configs: list[ScriptConfig]