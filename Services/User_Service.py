from fastapi import FastAPI ,File, UploadFile,Depends
import Models.models
import Schemas.Schema
from sqlalchemy.orm import Session
import os 
from uuid import uuid4
def create_user(users:Session,user:Schemas.Schema.Users):
    db_user=Models.models.Users(
        id=user.id,
        Name=user.Name,
        E_mail=user.E_mail,
        Phone_number=user.Phone_number,
        password=user.password
    )

    users.add(db_user)
    users.commit()
    users.refresh(db_user)
    return db_user

def get_user_by_mail(users:Session,email:str):
    return users.query(Models.models.Users).filter(email==Models.models.Users.E_mail).first()

def get_user(users: Session, id: int):
    return users.query(Models.models.Users).filter(Models.models.Users.id==id).first()

def save_user_extra_details( user:Session,user_info:Schemas.Schema.UserInformation,UserID:int):
    # allowed_files=["jpg","jpeg","png"]
    # if allowed_files not in file.filename:
    #     raise Exception("Invalid File Format")
    
    # file_ext=file.filename.split(".")[-1]
    # file_name=str(uuid4())+"."+file_ext
    # file_path=os.path.join("uploads",file_name)

    # with open(file_path, "wb") as buffer:
    #    buffer.write(file.read()) 

    db_user_info=Models.models.UserInformation(
        UserID=UserID,
        About=user_info.About,
        Vehicle=user_info.Vehicle,
        Travel_Preference_Music=user_info.Travel_Preference_Music,
        Travel_Preference_Pets=user_info.Travel_Preference_Pets,
        Travel_Preference_Smoking=user_info.Travel_Preference_Smoking,
        Travel_Preference_Conversation=user_info.Travel_Preference_Conversation
    )

    user.add(db_user_info)
    user.commit()
    user.refresh(db_user_info)
    return db_user_info

def get_user_entrainfo(users: Session, id: int):
    return users.query(Models.models.UserInformation).filter(Models.models.UserInformation.id==id).first()