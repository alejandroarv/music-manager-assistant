class PerformanceContractData:
    """
    Structure data model for performance contracts

    Encapsulates contract-related input data and performs
    normalization and validation before contract generation

    Responsibilities:
    - Validate required contract fields
    - Normalize incoming values
    - Maintain backward compatibility with older field names
    - Provide a consistent contract data structure
    """

    def __init__(
        self,
        artist,
        client=None,
        venue="",
        date=None,
        city="",
        venue_address="",
        fee=0,
        *,
        purchaser_name=None,
        purchaser_address=None,
        signatory=None,
        company_name=None,
        company_address=None,
        number_of_shows=1,

        # Backward-compatible support for legacy fields
        notes=None,
        additional_acts=None,

        shows=None,
        show_length="90 minutes",
        capacity="",
        ticketing_fee_percent=0.0,
        air_transportation="Provided",
        hotel_accommodations="Provided",
        air_freight="Included",
        ground_transportation="Provided",
        meals_incidentals="Provided",
        special_provisions="None",
        concessionaire_fee="0%",
        seller="TBD",
        hard_merchandising="Allowed",
        soft_merchandising="Allowed",
        complimentary_tickets="20",
        production="Standard production provided",
        catering="Standard catering provided",
        additional_addenda="None",
        merchandising_terms="Standard merchandising terms apply",
        buyer_name=None,
        buyer_company_name=None,

        manager_name="",
        manager_company_name="",

        signature_date=None,
    ):
        
        # Resolve client information from available inputs
        resolved_client = (client or purchaser_name or "").strip()

        # Core validation
        if not artist.strip():
            raise ValueError("Artist required")
        
        if not resolved_client:
            raise ValueError("Client required")
        
        if not city.strip():
            raise ValueError("City required")
        
        if int(number_of_shows) < 1:
            raise ValueError("Number of shows must be at least 1")
        
        if float(fee) <= 0:
            raise ValueError("Flat Guarantee must be greater than 0")

        # Maintain compatibility with older note-based contract data
        resolved_additional_acts = additional_acts if additional_acts else notes

        # Core contract information
        self.artist = artist.strip()
        self.client = resolved_client
        self.purchaser_name = (purchaser_name or resolved_client).strip()

        self.purchaser_address = str(purchaser_address).strip() if purchaser_address else ""

        self.signatory = (signatory or self.purchaser_name).strip()

        self.company_name = (company_name or resolved_client).strip()

        self.company_address = str(company_address).strip() if company_address else ""

        self.venue = venue.strip()
        self.date = date
        self.city = city.strip()
        self.venue_address = str(
            venue_address
        ).strip()
        self.fee = float(fee)
        self.number_of_shows = int(number_of_shows)

        # Additional performer information
        self.additional_acts = (
            str(resolved_additional_acts).strip()
            if resolved_additional_acts is not None
            else ""
        )

        # Show configuration
        self.show_length = str(show_length).strip()
        legacy_capacity = str(capacity).strip()

        if shows:

            self.shows = [
                {
                    **show,
                    "capacity": show.get(
                        "capacity"
                    ) or legacy_capacity,
                }
                for show in shows
            ]

        else:

            self.shows = (
                [
                    {
                        "capacity": legacy_capacity,
                    }
                ]
                if legacy_capacity
                else []
            )

        self.ticketing_fee_percent = (
            float(ticketing_fee_percent)
        )
        
        # Logistics and accommodations
        self.air_transportation = str(air_transportation).strip()
        self.hotel_accommodations = str(hotel_accommodations).strip()
        self.air_freight = str(air_freight).strip()
        self.ground_transportation = str(ground_transportation).strip()
        self.meals_incidentals = str(meals_incidentals).strip()

        # Additional contractual terms
        self.special_provisions = str(special_provisions).strip()
        self.concessionaire_fee = str(concessionaire_fee).strip()
        self.seller = str(seller).strip()
        self.hard_merchandising = str(hard_merchandising).strip()
        self.soft_merchandising = str(soft_merchandising).strip()
        self.complimentary_tickets = str(complimentary_tickets).strip()
        self.production = str(
            production
        ).strip()

        self.catering = str(
            catering
        ).strip()
        self.additional_addenda = str(additional_addenda).strip()
        self.merchandising_terms = str(merchandising_terms).strip()

        # Buyer information
        # Buyer information
        self.buyer_name = (
            buyer_name
            or self.signatory
        ).strip()

        self.buyer_company_name = (
            buyer_company_name
            or self.company_name
        ).strip()

        self.manager_name = str(
            manager_name
        ).strip()

        self.manager_company_name = str(
            manager_company_name
        ).strip()

        self.signature_date = (
            signature_date
            or date
        )

class NDAContractData:
    """
    Structured data model for NDA contracts

    Validates NDA input data before document generation
    and ensures required agreement fields are present
    """
    def __init__(self, disclosing_party, receiving_party, purpose, duration):
        
        # Required field validation
        if not disclosing_party.strip():
            raise ValueError("Disclosing party required")
        
        if not receiving_party.strip():
            raise ValueError("Receiving party required")
        
        if len(purpose.strip()) < 10:
            raise ValueError("Purpose must be at least 10 characters")
        
        if not duration or duration <= 0:
            raise ValueError("Duration must be greater than 0")
        
        # Normalized NDA data
        self.disclosing_party = disclosing_party.strip()
        self.receiving_party = receiving_party.strip()
        self.purpose = purpose.strip()
        self.duration = duration
