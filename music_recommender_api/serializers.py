from pydantic import BaseModel



class GetRecommendsSerializer(BaseModel):
    N: int
    data: list[dict]