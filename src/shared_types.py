from pydantic import BaseModel


class IntroSetup(BaseModel):
    blue: list[str]
    red: list[str]
    map: str
