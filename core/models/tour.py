# core/models/tour.py

class TourData:
    """
    Structured data model for tour planning

    Represents validated input used to generate
    tour schedules and routing information
    """
    def __init__(
            self, 
            artist, 
            cities, 
            start_date, 
            concerts_before_rest, 
            rest_days
        ):
        
        # Required field validation
        if not artist.strip():
            raise ValueError("Artist required")

        if not cities:
            raise ValueError("At least one city required")

        # Normalize artist name
        self.artist = artist.strip()

        # Remove empty city entries and normalize spacing
        self.cities = [c.strip() for c in cities if c.strip()]

        # Tour scheduling configuration
        self.start_date = start_date
        self.concerts_before_rest = concerts_before_rest
        self.rest_days = rest_days
