from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON 
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"  # Ensure this matches in all cases
    id = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50))
    E_mail = Column(String(50), unique=True, index=True)
    Phone_number = Column(Integer, unique=True)
    password = Column(String(255))

    publishrides = relationship("PublishRide", back_populates="user", lazy="select")
    userinformation = relationship("UserInformation", back_populates="user", lazy="select")

class PublishRide(Base):
    __tablename__ = "publishedrides"  
    id = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.id')) 
    pickup = Column(String(80))
    destination = Column(String(80))
    stopovers = Column(JSON, nullable=False)
    date = Column(String(30))
    time = Column(String(50))
    Is_women_only = Column(Boolean)
    Rules_ = Column(String(1000))
    Fare = Column(String(50))
    StopOver_Fare = Column(JSON, nullable=False)
    Car_Number = Column(Integer)
    Car_Type = Column(String(50))
    No_Of_Seats = Column(Integer)

    user = relationship("Users", back_populates="publishrides")  

class UserInformation(Base):
    __tablename__ = "userExtraDetails"  
    id = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('users.id')) 
    About = Column(String(1000))
    
    Vehicle = Column(String(50))
    Travel_Preference_Music = Column(String(50))
    Travel_Preference_Pets = Column(String(50))
    Travel_Preference_Smoking = Column(String(50))
    Travel_Preference_Conversation = Column(String(50))
    user = relationship("Users", back_populates="userinformation")    

