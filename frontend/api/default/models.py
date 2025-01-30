import aiohttp
from pydantic import BaseModel


class BaseRequestModel(BaseModel):
    text: str
    status_code: int
    read_bytes: bytes
    response: aiohttp.ClientResponse

    class Config:
        arbitrary_types_allowed = True
