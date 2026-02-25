import pydantic

class ScriptContent(pydantic.BaseModel):
    name: str
    description: str
    source_code: str