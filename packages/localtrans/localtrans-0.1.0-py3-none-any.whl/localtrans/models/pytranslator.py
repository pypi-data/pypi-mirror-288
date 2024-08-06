from pydantic import BaseModel


class PytFile(BaseModel):
    language_name: str
    file_path: str
