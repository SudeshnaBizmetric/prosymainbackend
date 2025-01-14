import datetime
from typing import List ,Optional
from fastapi import Depends, FastAPI ,HTTPException ,File, Query, UploadFile
from fastapi.security import OAuth2PasswordBearer
import Models.models 
import Services.BookRideService
import Services.PublishRideService
import Services.User_Service
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from Schemas import Schema
import auth
from database import Base ,engine ,Local_Session
from passlib.context import CryptContext
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from Models.models import Users
from sqlalchemy import and_, cast, Date
from Models.models import PublishRide
from sqlalchemy.sql import func

security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()    #fastapi instance
Base.metadata.create_all(bind=engine)   #to connect with database 
password_crypt=CryptContext(schemes=["bcrypt"],deprecated="auto")  #for password hashing
origins = [
    "http://localhost:5173",
]

UPLOAD_FOLDER = 'uploads'
#os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  #frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
def hashed_password(password:str)->str:
   return password_crypt.hash(password)

def get_db():
    db=Local_Session()

    try:
       yield db
    finally:
       db.close()


#Registration API 

@app.post("/v1/users",response_model=Schema.Users,status_code=201)
def add_new_user(user:Schema.Users,users:Session=Depends(get_db)):
   user.password = hashed_password(user.password)
   new_user=Models.models.Users(
      Name=user.Name,
      E_mail=user.E_mail,
      Phone_number=user.Phone_number,
      password=user.password
   )
   users.add(new_user)
   users.commit()
   users.refresh(new_user)
   return new_user

   
@app.post("/v1/login") 
def LoginUser(login:Schema.Login,users:Session=Depends(get_db)):
     user=Services.User_Service.get_user_by_mail(users,login.E_mail)

     if not user:
         raise  HTTPException (status_code=401,detail="Invalid Credentials")
     if (login.password==user.password):
         raise  HTTPException (status_code=401,detail="Invalid Credentials")
     access_token=auth.create_access_token(data={"id":user.id})
     return {"access_token": access_token, "id": user.id}


def get_current_user(
    token: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> Users:
    try:
        # Decode the token
        payload = jwt.decode(token.credentials, auth.secret, algorithms=auth.algorithm)
        user_id: int = payload.get("id")  # Extract the user ID
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: Missing user ID")
        
        # Query the user in the database
        user = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

@app.post("/v1/publishrides", response_model=Schema.PublishRide, status_code=201)
def publish_rides(ride_data: Schema.PublishRide, rides: Session = Depends(get_db),current_userid:Models.models.Users= Depends(get_current_user)):
 
    try:
        # Use the service layer to handle ride creation logic
        ride = Services.PublishRideService.Publish_Ride(rides, ride_data,UserID=current_userid.id)
        
        # Database operations
        rides.add(ride)
        rides.commit()
        rides.refresh(ride)
        return ride
    except Exception as e:
      rides.rollback()
      raise HTTPException(
        status_code=400,
        detail=f"Failed to publish ride: {str(e)}"
)
    
@app.get("/v1/publishrides/{UserID}")
def get_rides_by_userid(UserID:int,rides:Session=Depends(get_db)):
    return Services.PublishRideService.get_rides_by_userid(rides,UserID)

@app.get("/v1/users/{id}")
def get_user(id:int,users:Session=Depends(get_db)):
    return Services.User_Service.get_user(users,id)

@app.post("/v1/userinformation/{UserID}",response_model=Schema.UserInformation,status_code=201)
def save_user_extra_details(user_info:Schema.UserInformation,users:Session=Depends(get_db),current_userid:Models.models.Users= Depends(get_current_user)):
    user_info.UserID=current_userid.id
    user_info=Services.User_Service.save_user_extra_details(users,user_info,current_userid.id)
    return user_info

@app.get("/v1/users_info/{id}")
def get_user_entrainfo(id:int,users:Session=Depends(get_db)):
    return Services.User_Service.get_user_entrainfo(users,id)

from fastapi import HTTPException

@app.get("/v1/search-rides")
def search_rides(
    pickup: str,
    destination: str,
    date: str,
    no_of_seats: int,
    db: Session = Depends(get_db)
):
    # date comparison matches only the date portion of a datetime
    rides = db.query(PublishRide).filter(
        PublishRide.pickup.ilike(f"%{pickup}%"),  
        PublishRide.destination.ilike(f"%{destination}%"),  
        func.date(PublishRide.date) == date, 
        PublishRide.No_Of_Seats >= no_of_seats  
    ).all()
    
    
    
    if not rides:
        return {"message": "No rides found.", "rides": []}

    
    ride_details = [
        {
            "ride_id": ride.id,  
            "pickup": ride.pickup,
            "destination": ride.destination,
            "date": ride.date,
            "No_Of_Seats": ride.No_Of_Seats,
            "Fare": ride.Fare,
            "Car_Type": ride.Car_Type,
            "Car_Number": ride.Car_Number,
            "stopovers": ride.stopovers,
            "StopOver_Fare": ride.StopOver_Fare,
            "time": ride.time,
            "instant_booking": ride.instant_booking,
        }
        for ride in rides
    ]

    return {"message": "Rides found.", "rides": ride_details}
 
     
    

@app.post("/v1/bookings_instant", response_model=Schema.BookARide, status_code=201)
def book_ride(
    booking_data: Schema.BookARide, 
    rides: Session = Depends(get_db), 
    current_user: Models.models.Users = Depends(get_current_user)
):
    try:
        # Fetch the ride details using RideID
        ride_record = rides.query(Models.models.PublishRide).filter(
            Models.models.PublishRide.id == booking_data.RideID
        ).first()

        if not ride_record:
            raise HTTPException(status_code=404, detail="Ride not found")

        # Call the booking service to process the booking
        booking = Services.BookRideService.book_ride_instant(
            rides, 
            booking_data, 
            UserID=current_user.id, 
            RideID=booking_data.RideID, 
            seats=booking_data.Seats_Booked  # Pass the number of seats requested by the user
        )
        
        return booking

    except HTTPException as e:
        raise e
    except Exception as e:
        rides.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to book ride: {str(e)}"
        )