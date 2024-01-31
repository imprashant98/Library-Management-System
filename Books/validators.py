from pydantic import BaseModel


class GetUserValidator(BaseModel):
    user_id: int
