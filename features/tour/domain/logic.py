# features/tour/domain/logic.py

from datetime import (
    datetime,
    timedelta,
)

from core.models.tour import TourData


def build_tour(data: TourData):
    """
    Generate a structured tour schedule
    from normalized tour configuration data.

    Responsibilities:
    - Build ordered concert schedules
    - Insert rest-day intervals
    - Enforce concert/rest sequencing rules
    - Return pure structured data

    This is a pure domain function:
    - No persistence
    - No UI formatting
    - No side effects
    - Deterministic output
    """

    # Container for generated schedule events
    tour = []

    # Normalize starting date into a full
    # datetime object for arithmetic operations
    current_date = datetime.combine(
        data.start_date,
        datetime.min.time(),
    )

    # Tracks consecutive concerts in order
    # to determine when rest periods occur
    concert_count = 0

    # Build tour schedule sequentially
    for i, city in enumerate(data.cities):

        # ------------------------
        # Concert Event
        # ------------------------

        tour.append(
            {
                "type": "concert",
                "date": current_date,
                "city": city,
            }
        )

        concert_count += 1

        # Advance to the next calendar day
        current_date += timedelta(days=1)

        # -----------------------------
        # Rest-Day Scheduling Logic
        # -----------------------------

        should_rest = (
            concert_count
            == data.concerts_before_rest
        )

        # Insert rest periods only if:
        # - the concert threshold is reached
        # - there are remaining tour cities
        if (
            should_rest
            and i != len(data.cities) - 1
        ):

            # Generate configured rest days
            for _ in range(data.rest_days):

                tour.append(
                    {
                        "type": "rest",
                        "date": current_date,
                    }
                )

                # Advance timeline during rest
                current_date += timedelta(
                    days=1
                )

            # Reset concert counter after
            # completing the rest cycle
            concert_count = 0

    # Return normalized tour structure
    return {
        "name": data.artist,
        "schedule": tour,
    }