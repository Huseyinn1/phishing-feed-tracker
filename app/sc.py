from pydantic import BaseModel

class URLBase(BaseModel):
    url: str
    url_id: int
    url_author: str
    source: str

class URLCreate(URLBase):
    pass

class URL(URLBase):
    id: int

    class Config:
        orm_mode = True
