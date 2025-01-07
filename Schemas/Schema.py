from typing import Optional ,List
from pydantic import BaseModel, EmailStr, Field

class Users(BaseModel):
    
    Name: str = Field(..., min_length=3, max_length=50)  
    E_mail: EmailStr
    Phone_number: int  
    password: str = Field(..., min_length=8)  

    class Config:
        orm_mode = True

class Login(BaseModel):
    E_mail:EmailStr
    password:str = Field(..., min_length=8)

class StopoverType(BaseModel):
    text: str

class StopoverFareType(BaseModel):
    price: str

class PublishRide(BaseModel):
    UserID:int
    pickup: str
    destination: str
    stopovers:Optional[List[StopoverType] ] 
    date: str
    time: str
    Is_women_only: bool
    Rules_: Optional[str] = None 
    Fare: int
    StopOver_Fare:Optional[List[StopoverFareType] ] 
    Car_Number: int
    Car_Type: str
    No_Of_Seats: int

class Config:
        orm_mode = True

class userProfile(BaseModel):
    Name: str
    E_mail: EmailStr
    Phone_number: int

    class Config:
        orm_mode = True

class Stopover(BaseModel):
    stopovers:Optional[List[StopoverType] ] 

class Config:
        orm_mode = True  

class UserInformation(BaseModel):
    UserID:int
    About: str
    Vehicle: str
    Travel_Preference_Music: str
    Travel_Preference_Pets: str
    Travel_Preference_Smoking: str
    Travel_Preference_Conversation: str
    

    class Config:
        orm_mode = True

