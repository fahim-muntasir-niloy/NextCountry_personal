from typing import List, Optional
from pydantic import BaseModel, EmailStr
from langgraph.graph import MessagesState

class NC_UserResponse(MessagesState):
    main_goal: Optional[str]
    current_nationality: Optional[str]
    additional_passport: bool
    additional_residency: bool
    current_work_situation: Optional[str]
    current_job_industry: Optional[str]
    company_registered_at_home: bool
    will_open_company_at_abroad: bool
    monthly_income: Optional[str]
    savings_in_personal_account: Optional[str]
    interested_region: Optional[str]
    duration_of_stay: Optional[str]
    tax_benefits_option: Optional[str]
    help_open_bank_account: bool
    extend_stay_option: bool
    solo_or_family: Optional[str]
    number_of_dependents: Optional[str]
    accommodation_in_new_country: bool  
    flight_status:bool
    past_immigration_issue: Optional[str]
    criminal_record: bool
    
    
class NC_AgentResponse(BaseModel):
    topic: str
    user_profile_summary:str
    content:str
    retrived_content_metadata: List[str]
    tools_used: List[str]