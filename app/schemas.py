from pydantic import BaseModel, field_validator
import re
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, v):
            raise ValueError('Invalid email address')
        return v

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        if v is not None:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_regex, v):
                raise ValueError('Invalid email address')
        return v

class CustomerResponse(CustomerBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class CreditCheckRequest(BaseModel):
    customer_id: str
    callback_url: str
    wait_seconds: int = 5

    @field_validator('wait_seconds')
    @classmethod
    def validate_wait_seconds(cls, v):
        if v < 1 or v > 60:
            raise ValueError('wait_seconds must be between 1 and 60')
        return v

    @field_validator('callback_url')
    @classmethod
    def validate_callback_url(cls, v):
        url_regex = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_regex, v):
            raise ValueError('Invalid callback URL')
        return v

class CreditCheckResponse(BaseModel):
    message: str
    task_id: str

class CreditCheckCallback(BaseModel):
    customer_id: str
    credit_score: int
    risk_level: str
    timestamp: datetime