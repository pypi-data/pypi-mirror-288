from datetime import datetime

from pydantic import BaseModel, Field


class Reference(BaseModel):
    index: int
    handle: str


class PidData(BaseModel):
    type: str
    parsed_data: str | dict
    timestamp: datetime = Field(default_factory=datetime.now)
    ttl_type: int = Field(0, ge=0, le=1)
    ttl: int = 86400
    refs: list[Reference] = None
    privs: str = Field('rwr-', pattern='^[r-][w-][r-][w-]')


class Pid(BaseModel):
    prefix: str = None
    suffix: str = None
    data: list[PidData] = None

    @property
    def pid_str(self) -> str:
        return f'{self.prefix}/{self.suffix}'

    @pid_str.setter
    def pid_str(self, value: str):
        items = value.split('/', 1)
        self.prefix = items[0]
        self.suffix = items[1]
