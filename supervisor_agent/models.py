from pydantic import BaseModel
from typing import List, Optional

# ========================
# Subclasses
# ========================


class personalHighlight(BaseModel):
    keyword: str
    reason: str


class personalRiskFlags(BaseModel):
    keyword: str
    reason: str


class ApplicationCost(BaseModel):
    title: str = "Estimated Application Cost"
    gov_visa_fee: int
    legal_fee: int
    translation_notary_fee: int
    flight_relocation_price: int


class CostOfLiving(BaseModel):
    title: str = "Estimated Cost of Living"
    rent: int
    food: int
    transport: int
    utilities: int
    health_insurance: int
    other: int


class ticketPrice(BaseModel):
    one_way: int
    round_trip: int


class Glance(BaseModel):
    current_location: str
    relocation_timeline: str
    family: str
    startup_status: str
    annual_income: str
    investment_budget: str
    preferred_climate: str
    language_preference: str


class Snapshot(BaseModel):
    current_location: str
    relocation_timeline: str
    family: str
    income_source: str
    startup_stage: str
    investment_budget: str
    climate_preference: str
    language_preference: str


class Phase1(BaseModel):
    item_1: str = "Checklist Delivery"
    item_2: str = "Document Collection and Translations"
    item_3: str = "Bank account setup initiation"


class Phase2(BaseModel):
    item_1: str = "Application form filling"
    item_2: str = "File handed to immigration portal"
    item_3: str = "Confirmation receipts stored in your dashboard"


class Phase3(BaseModel):
    item_1: str = "Visa approval"
    item_2: str = "Relocation assistance"
    item_3: str = "Post-arrival support"


# ========================
# Main classes
# ========================


class PersonalNote(BaseModel):
    section_title: str = "Personal Note"
    name: str
    note: str
    sender: str = "Rafsan Kamal"


class ExecutiveSummary(BaseModel):
    section_title: str = "Executive Summary"
    first_name: str
    last_name: str
    savings: str
    total_members: int
    legal_residence: str
    remote_job: str
    nationality: str
    self_employment: str
    income: str


class KeyRecommendation(BaseModel):
    section_title: str = "Key Recommendation"
    country_name: str
    visa_type: str
    fit_percentage: int
    reasons_to_recommend: List[str]


class profileGlance(BaseModel):
    glance: Glance
    snapshot: Snapshot


class VisaDetails(BaseModel):
    section_title: str = "Visa Details"
    country_name_and_visa: str
    introduction: str
    personalized_highlights: List[personalHighlight]
    risk_flags: List[personalRiskFlags]
    required_documents: List[str]
    cost_of_application: ApplicationCost
    cost_of_living: CostOfLiving
    ticket_price: ticketPrice
    starter_documents: List[str]


class Recommendation(BaseModel):
    section_title: str = "Our Recommendation"
    country_name: str
    visa_type: str
    reason: str


class NextSteps(BaseModel):
    section_title: str = "Next Steps"
    phase_1: Phase1
    phase_2: Phase2
    phase_3: Phase3


# ============
# Final Json
# ============
class FinalJson(BaseModel):
    A: PersonalNote
    B: ExecutiveSummary
    C: List[KeyRecommendation]
    D: profileGlance
    E: VisaDetails
    F: VisaDetails
    G: Recommendation
    H: NextSteps
