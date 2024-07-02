from pydantic import BaseModel
from typing import Union


class MainData(BaseModel):
    resume_id: str
    url: str
    salary: Union[str, None]
