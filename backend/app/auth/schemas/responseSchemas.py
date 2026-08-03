from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    fullname: str
    email: str

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse
