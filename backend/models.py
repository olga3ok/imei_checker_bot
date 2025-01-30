from pydantic import BaseModel


class IMEIRequest(BaseModel):
    imei: str