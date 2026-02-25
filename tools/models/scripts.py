import pydantic

class ScriptContent(pydantic.BaseModel):
    name: str
    description: str
    content: str