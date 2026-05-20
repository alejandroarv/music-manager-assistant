from core.models.contracts import NDAContractData, PerformanceContractData
from core.models.record import Record
from core.repositories.record_repository import RecordRepository
from core.result import Result
from core.templates import get_template
from features.contracts.domain.logic import (
    build_nda_contract,
    build_performance_contract,
)
from utils.helpers import format_filename, make_json_safe
from core.constants import PERFORMANCE_CONTRACT, NDA_CONTRACT


class ContractService:
    """
    Application service for contract generation.
    """

    def __init__(self, repository: RecordRepository):
        self.repo = repository

    def preview_performance_contract(self, data: PerformanceContractData) -> Result:
        try:
            return Result.ok(build_performance_contract(data))
        except Exception as e:
            return Result.fail(f"Failed to build performance contract: {str(e)}")

    def generate_performance_contract(self, data: PerformanceContractData) -> Result:
        contract_result = self.preview_performance_contract(data)
        if not contract_result.success:
            return contract_result

        try:
            template_name = (
                "performance_single"
                if data.number_of_shows == 1
                else "performance_multi"
            )

            record = Record(
                type=PERFORMANCE_CONTRACT,
                name=data.artist,
                content={
                    "format": "docx",
                    "template": template_name,
                    "artist": data.artist,
                    "client": data.client,
                    "purchaser_name": data.purchaser_name,
                    "purchaser_address": data.purchaser_address,
                    "signatory": data.signatory,
                    "company_name": data.company_name,
                    "company_address": data.company_address,
                    "venue": data.venue,
                    "date": str(data.date),
                    "signature_date": str(data.signature_date),
                    "city": data.city,
                    "fee": data.fee,
                    "number_of_shows": data.number_of_shows,
                    "notes": data.additional_acts,
                    "show_length": data.show_length,
                    "capacity": data.capacity,
                    "air_transportation": data.air_transportation,
                    "hotel_accommodations": data.hotel_accommodations,
                    "air_freight": data.air_freight,
                    "ground_transportation": data.ground_transportation,
                    "meals_incidentals": data.meals_incidentals,
                    "special_provisions": data.special_provisions,
                    "concessionaire_fee": data.concessionaire_fee,
                    "seller": data.seller,
                    "hard_merchandising": data.hard_merchandising,
                    "soft_merchandising": data.soft_merchandising,
                    "complimentary_tickets": data.complimentary_tickets,
                    "production_catering": data.production_catering,
                    "additional_addenda": data.additional_addenda,
                    "merchandising_terms": data.merchandising_terms,
                    "buyer_name": data.buyer_name,
                    "buyer_company_name": data.buyer_company_name,
                    "shows": make_json_safe(data.shows),
                },
                metadata={
                    "artist": data.artist,
                    "venue": data.venue,
                    "date": str(data.date),
                    "number_of_shows": data.number_of_shows,
                },
            )

            self.repo.save(record)
            return contract_result

        except Exception as e:
            return Result.fail(f"Failed to generate performance contract: {str(e)}")

    # ✅ NEW SAFE ENTRY POINT
    def create_performance_contract(self, data: dict) -> Result:
        try:
            contract_data = PerformanceContractData(**data)
        except ValueError as e:
            return Result.fail(str(e))

        return self.generate_performance_contract(contract_data)

    def generate_filename(self, name: str, suffix: str, extension: str = "txt") -> str:
        return f"{format_filename(name)}_{suffix}.{extension}"

    def generate_nda_contract(self, data: NDAContractData) -> Result:

        try:
            template = get_template("nda")
            contract = build_nda_contract(data, template)

            record = Record(
                type=NDA_CONTRACT,
                name=data.disclosing_party,
                content=contract,
                metadata={
                    "disclosing_party": data.disclosing_party,
                    "receiving_party": data.receiving_party,
                },
            )

            self.repo.save(record)

        except Exception:
            return Result.fail("Failed to generate NDA contract")

        return Result.ok(contract)

    # ✅ NEW SAFE ENTRY POINT
    def create_nda_contract(self, data: dict) -> Result:
        try:
            contract_data = NDAContractData(**data)
        except ValueError as e:
            return Result.fail(str(e))

        return self.generate_nda_contract(contract_data)
