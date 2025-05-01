from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserState(BaseModel):
    user_name: Optional[str]
    user_email: Optional[EmailStr]
    age: Optional[int]
    gender: Optional[str]
    address: Optional[str]
    phone: Optional[str]
    intended_country_of_study: Optional[str]
    intended_university: Optional[str]
    intended_degree: Optional[str]
    preferred_language_of_study: Optional[str]
    intended_program: Optional[str]
    intended_course: Optional[str]
    intended_session: Optional[str]
    intended_year: Optional[str]
    latest_grade_point: Optional[str]
    medical_conditions: Optional[str]
    english_proficiency: Optional[str]
    research_interests: Optional[List[str]]
    resarch_experience: Optional[str]
    research_publications: Optional[List[str]]
    visa_status: Optional[str]
    work_experience: Optional[str]
    
    
class NC_AgentResponse(BaseModel):
    topic: str
    summary: str
    user_profile_summary:str
    suitable_countries: str
    reasoning: str
    pros:str
    cons:str
    suggestions: str
    sources: List[str]
    tools_used: List[str]