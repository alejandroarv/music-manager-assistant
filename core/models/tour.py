# core/models/tour.py

class TourData:
    """
    # Data model for tour planning
    # Represents input needed to generate a tour schedule
    """
    def __init__(self, artist, cities, start_date, concerts_before_rest, rest_days):
        
        # Validate required fields
        if not artist.strip():
            raise ValueError("Artist required")

        if not cities:
            raise ValueError("At least one city required")

        # Normalize and assign
        self.artist = artist.strip()

        # Clean city list (remove empty entries and strip spaces)
        self.cities = [c.strip() for c in cities if c.strip()]

        self.start_date = start_date
        self.concerts_before_rest = concerts_before_rest
        self.rest_days = rest_days
