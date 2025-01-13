from fastapi import FastAPI, HTTPException
import Schemas.Schema
import Models.models
from sqlalchemy.orm import Session



def book_ride_instant(Rides: Session, Ride: Schemas.Schema.BookARide, UserID: int,RideID:int):
   

    
    db_Rides = Models.models.Bookings(
        UserID=UserID,
        RideID=RideID,
        Seats_Booked=Ride.Seats_Booked,
        booking_status=True
    )
    
    try:
       
        Rides.add(db_Rides)
        Rides.commit()
        Rides.refresh(db_Rides)
        return db_Rides
    except Exception as e:
        Rides.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to book ride: {str(e)}")

