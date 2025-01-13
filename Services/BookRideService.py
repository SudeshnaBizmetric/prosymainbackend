from fastapi import FastAPI, HTTPException
import Schemas.Schema
import Models.models
from sqlalchemy.orm import Session



def book_ride_instant(Rides: Session, Ride: Schemas.Schema.BookARide, UserID: int,RideID:int):
   

    # Now create the booking in the Bookings table
    db_Rides = Models.models.Bookings(
        UserID=UserID,
        RideID=RideID,
        Seats_Booked=Ride.seats_booked,
        booking_status=True
    )
    
    try:
        # Save the booking to the database
        Rides.add(db_Rides)
        Rides.commit()
        Rides.refresh(db_Rides)
        return db_Rides
    except Exception as e:
        Rides.rollback()
        raise HTTPException(status_code=400, detail=f"Failed to book ride: {str(e)}")

