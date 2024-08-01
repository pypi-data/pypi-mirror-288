from typing import Optional
from pydantic import BaseModel

class CreatePartnerDTO(BaseModel):
    id: Optional[int] = None
    description: str
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    