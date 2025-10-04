from pydantic import BaseModel, ConfigDict

class AuditLogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    entity: str
    entity_id: int
    action: str
    detail: str
