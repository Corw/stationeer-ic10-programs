import pydantic

class ScriptConfig(pydantic.BaseModel):
    name: str
    description: str
    src_file: str
    script_directory: str

class Config(pydantic.BaseModel):
    scripts_configs: list[ScriptConfig]