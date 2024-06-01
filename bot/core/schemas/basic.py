from pydantic import BaseModel


class ResultItems(BaseModel):
    items: list
    