from pydantic import BaseModel
from typing import List, Optional

# ========================
# Subclasses
# ========================

class ApplicationCost(BaseModel):
    title:str="Estimated Application Cost"
    gov_visa_fee:str
    legal_fee:str
    translation_notary_fee:str
    flight_relocation_price: str

class CostOfLiving(BaseModel):
    title:str="Estimated Cost of Living"
    rent:str
    food:str
    transport:str
    utilities:str
    health_insurance:str
    other:str

class Phase1(BaseModel):
    item_1:str="Checklist Delivery"
    item_2:str="Document Collection and Translations"
    item_3:str="Bank account setup initiation"

class Phase2(BaseModel):
    item_1:str="Application form filling"
    item_2:str="File handed to immigration portal"
    item_3:str="Confirmation receipts stored in your dashboard"

class Phase3(BaseModel):
    item_1:str="Visa approval"
    item_2:str="Relocation assistance"
    item_3:str="Post-arrival support"


# ========================
# Main classes
# ========================

class PersonalNote(BaseModel):
    section_title:str="Personal Note"
    name:str
    note:str
    sender:str = "Rafsan Kamal"

class ExecutiveSummary(BaseModel):
    section_title:str="Executive Summary"
    first_name:str
    last_name:str
    savings:str
    total_members:int
    legal_residence:str
    remote_job:str
    nationality:str
    self_employment:str
    income:str

class KeyRecommendation(BaseModel):
    section_title:str="Key Recommendation"
    country_name: str
    visa_type: str
    fit_percentage: int
    reasons_to_recommend: List[str]

# profile at a glance ---> left for now


class VisaDetails(BaseModel):
    section_title:str="Visa Details"
    country_name_and_visa:str
    introduction: str
    personalized_highlights: List[str]
    risk_flags: List[str]
    required_documents: List[str]
    cost_of_application: ApplicationCost
    cost_of_living: CostOfLiving
    ticket_price: Optional[str]
    starter_documents: List[str]

class Recommendation(BaseModel):
    section_title:str="Our Recommendation"
    country_name: str
    visa_type: str
    reason: str



class NextSteps(BaseModel):
    section_title:str="Next Steps"
    phase_1: Phase1
    phase_2: Phase2
    phase_3: Phase3


# ============
# Final Json
# ============
class FinalJson(BaseModel):
    A:PersonalNote
    B: ExecutiveSummary
    C: KeyRecommendation
    D: KeyRecommendation
    E: VisaDetails
    F: VisaDetails
    G: Recommendation
    H: NextSteps