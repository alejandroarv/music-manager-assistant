# core/models/contracts.py

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

        deal_type="Flat Guarantee",

        flat_guarantee=0,

        percentage=0,

        deal_basis="Net",

        minimum_guarantee=0,
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
        air_transportation_required=True,
        air_transportation_yes="",
        air_transportation_no="",
        hotel_accommodations_required=True,
        hotel_accommodations_yes="",
        hotel_accommodations_no="",
        air_freight_required=True,
        air_freight_yes="",
        air_freight_no="",
        ground_transportation_required=True,
        ground_transportation_yes="",
        ground_transportation_no="",
        meals_incidentals_required=True,
        meals_incidentals_yes="",
        meals_incidentals_no="",
        hotel_accommodations=None,
        air_freight=None,
        ground_transportation=None,
        meals_incidentals=None,

        visas_required=True,
        visa_responsible_party="Purchaser",

        special_provisions="None",
        concessionaire_fee="0%",

        seller="TBD",

        hard_merchandising=100,
        hard_concessionaire_fee=0,

        soft_merchandising=100,
        soft_concessionaire_fee=0,

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
        
        if deal_type in (

            "Flat Guarantee",

            "Versus Deal",

            "Buyout",

        ):

            if float(
                flat_guarantee
            ) <= 0:

                raise ValueError(

                    "Guarantee must be greater than 0"

                )

        elif deal_type in (

            "Percentage Deal",

            "Door Deal",

        ):

            if float(
                percentage
            ) <= 0:

                raise ValueError(

                    "Percentage must be greater than 0"

                )

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

        self.deal_type = str(
            deal_type
        ).strip()

        self.flat_guarantee = float(
            flat_guarantee
        )

        self.percentage = float(
            percentage
        )

        self.deal_basis = str(
            deal_basis
        ).strip()

        self.minimum_guarantee = float(
            minimum_guarantee
        )
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

        if isinstance(air_transportation_required, str):
            self.air_transportation_required = (
                air_transportation_required.strip().lower() == "yes"
            )
        else:
            self.air_transportation_required = bool(
                air_transportation_required
            )

        self.air_transportation_yes = str(
            air_transportation_yes
        ).strip()

        self.air_transportation_no = str(
            air_transportation_no
        ).strip()

        if isinstance(hotel_accommodations_required, str):
            self.hotel_accommodations_required = (
                hotel_accommodations_required.strip().lower() == "yes"
            )
        else:
            self.hotel_accommodations_required = bool(
                hotel_accommodations_required
            )

        self.hotel_accommodations_yes = str(
            hotel_accommodations_yes
            or hotel_accommodations
            or ""
        ).strip()

        self.hotel_accommodations_no = str(
            hotel_accommodations_no
        ).strip()

        if isinstance(air_freight_required, str):
            self.air_freight_required = (
                air_freight_required.strip().lower() == "yes"
            )
        else:
            self.air_freight_required = bool(
                air_freight_required
            )

        self.air_freight_yes = str(
            air_freight_yes
            or air_freight
            or ""
        ).strip()

        self.air_freight_no = str(
            air_freight_no
        ).strip()

        if isinstance(ground_transportation_required, str):
            self.ground_transportation_required = (
                ground_transportation_required.strip().lower() == "yes"
            )
        else:
            self.ground_transportation_required = bool(
                ground_transportation_required
            )

        self.ground_transportation_yes = str(
            ground_transportation_yes
            or ground_transportation
            or ""
        ).strip()

        self.ground_transportation_no = str(
            ground_transportation_no
        ).strip()

        if isinstance(meals_incidentals_required, str):
            self.meals_incidentals_required = (
                meals_incidentals_required.strip().lower() == "yes"
            )
        else:
            self.meals_incidentals_required = bool(
                meals_incidentals_required
            )

        self.meals_incidentals_yes = str(
            meals_incidentals_yes
            or meals_incidentals
            or ""
        ).strip()

        self.meals_incidentals_no = str(
            meals_incidentals_no
        ).strip()

        if isinstance(visas_required, str):
            self.visas_required = (
                visas_required.strip().lower() == "yes"
            )
        else:
            self.visas_required = bool(
                visas_required
            )

        self.visa_responsible_party = str(
            visa_responsible_party
        ).strip()
        # Additional contractual terms
        self.special_provisions = str(special_provisions).strip()
        self.concessionaire_fee = str(
            concessionaire_fee
        ).strip()

        self.seller = str(
            seller
        ).strip()

        self.hard_merchandising = int(
            hard_merchandising
        )

        self.hard_concessionaire_fee = int(
            hard_concessionaire_fee
        )

        self.soft_merchandising = int(
            soft_merchandising
        )

        self.soft_concessionaire_fee = int(
            soft_concessionaire_fee
        )
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
