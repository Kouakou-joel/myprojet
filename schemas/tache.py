from pydantic import BaseModel


class Tache(BaseModel):
    id: int
    title: str
    description: str
    owner: str
    class config:
        from_attributes = True

class TacheCreate(BaseModel):
    title: str
    description: str
    class config:
        from_attributes = True

class TacheResponse(BaseModel):

    list: list[Tache]
    class Config:
        from_attributes = True