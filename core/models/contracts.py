class PerformanceContractData:
    def __init__(
        self,
        artist,
        client=None,
        venue="",
        date=None,
        city="",
        fee=0,
        *,
        purchaser_name=None,
        purchaser_address=None,
        signatory=None,
        company_name=None,
        company_address=None,
        number_of_shows=1,

        # 👇 BOTH supported
        notes=None,
        additional_acts=None,

        shows=None,
        show_length="90 minutes",
        capacity="",
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
        production_catering="Standard production provided",
        additional_addenda="None",
        merchandising_terms="Standard merchandising terms apply",
        buyer_name=None,
        buyer_company_name=None,
        signature_date=None,
    ):
        resolved_client = (client or purchaser_name or "").strip()

        # Validation
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

        # 👇 KEY FIX (backward compatibility)
        resolved_additional_acts = additional_acts if additional_acts else notes

        # Assign
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
        self.fee = float(fee)
        self.number_of_shows = int(number_of_shows)

        # 👇 final field
        self.additional_acts = (
            str(resolved_additional_acts).strip()
            if resolved_additional_acts is not None
            else ""
        )

        self.show_length = str(show_length).strip()
        self.shows = shows or []
        self.capacity = str(capacity).strip()

        self.air_transportation = str(air_transportation).strip()
        self.hotel_accommodations = str(hotel_accommodations).strip()
        self.air_freight = str(air_freight).strip()
        self.ground_transportation = str(ground_transportation).strip()
        self.meals_incidentals = str(meals_incidentals).strip()
        self.special_provisions = str(special_provisions).strip()
        self.concessionaire_fee = str(concessionaire_fee).strip()
        self.seller = str(seller).strip()
        self.hard_merchandising = str(hard_merchandising).strip()
        self.soft_merchandising = str(soft_merchandising).strip()
        self.complimentary_tickets = str(complimentary_tickets).strip()
        self.production_catering = str(production_catering).strip()
        self.additional_addenda = str(additional_addenda).strip()
        self.merchandising_terms = str(merchandising_terms).strip()
        self.buyer_name = (buyer_name or self.signatory).strip()
        self.buyer_company_name = (buyer_company_name or self.company_name).strip()
        self.signature_date = signature_date or date

class NDAContractData:
    """
    # Data model for NDA contracts
    # Ensures required fields are valid before contract generation
    """
    def __init__(self, disclosing_party, receiving_party, purpose, duration):
        
        if not disclosing_party.strip():
            raise ValueError("Disclosing party required")
        if not receiving_party.strip():
            raise ValueError("Receiving party required")
        if len(purpose.strip()) < 10:
            raise ValueError("Purpose must be at least 10 characters")
        if not duration or duration <= 0:
            raise ValueError("Duration must be greater than 0")

        self.disclosing_party = disclosing_party.strip()
        self.receiving_party = receiving_party.strip()
        self.purpose = purpose.strip()
        self.duration = duration
