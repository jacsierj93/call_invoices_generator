from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PhoneInvoiceRequest(BaseModel):
    phone_number: str  # User's phone number
    date_from: datetime  # Invoice start date
    date_to: datetime  # Invoice end date

class CallDetail(BaseModel):
    phone_number: str  # Destination number
    duration: int  # Call duration in seconds
    timestamp: datetime  # Call date and time
    amount: float  # Call cost

class UserDetail(BaseModel):
    address: str  # User's address
    name: str  # User's name
    phone_number: str  # User's phone number
    
class PhoneInvoiceResponse(BaseModel):
    user: UserDetail  # User details
    calls: List[CallDetail]  # List of call details
    total_international_seconds: int  # Total international seconds
    total_national_seconds: int  # Total national seconds
    total_friends_seconds: int  # Total friends seconds
    gross_total: float  # Invoice total
    friends_discount: float  # Friends call discount
    total: float  # Total to pay

class UserResponse(BaseModel):
    address: str  # User's address
    friends: List[str]  # List of friends' phone numbers
    name: str  # User's name
    phone_number: str  # User's phone number

class CallResponse(BaseModel):
    numero_origen: str  # Origin phone number
    numero_destino: str  # Destination phone number
    duracion: int  # Call duration in seconds
    fecha: datetime  # Call date and time