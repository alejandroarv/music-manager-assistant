# features/tour/domain/logic.py

from datetime import datetime, timedelta
from core.models.tour import TourData

def build_tour(data: TourData):
    """
    # Generate a tour schedule based on input data

    # Responsibilities:
    # - Create ordered schedule of concerts and rest days
    # - Enforce sequencing logic (concert -> rest cycles)
    # - Return structured result(no formatting, no storage)

    # This is a PURE FUNCTION:
    # - No side effects
    # - No storage
    # - Derteministic output
    """

    # List to hold the final schedule
    tour = []

    # Initialize starting date (combine date with midnight time)
    current_date = datetime.combine(data.start_date, datetime.min.time())

    # Counter for consecutive concerts
    concert_count = 0

    # Iterate through each city
    for i, city in enumerate(data.cities):

        # ------------------------
        # Add concert event
        # ------------------------

        tour.append({
            "type": "concert",
            "date": current_date,
            "city": city
        })

        concert_count += 1

        # Move to next day
        current_date += timedelta(days=1)

        # -----------------------------
        # Determines if rest is needed
        # -----------------------------

        should_rest = concert_count == data.concerts_before_rest

        # Only add rest if:
        # - we reached the limit
        # - AND this is not the last city
        if should_rest and i != len(data.cities) - 1:

            # Add rest days
            for _ in range(data.rest_days):
                tour.append({
                    "type": "rest",
                    "date": current_date
                })

                # Move to next day
                current_date += timedelta(days=1)
            # Reset concert counter after rest
            concert_count = 0

    # Return structured result
    return {
        "name": data.artist,
        "schedule": tour
    }
