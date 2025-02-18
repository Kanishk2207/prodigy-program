from pydantic import BaseModel

class MarkCompleted(BaseModel):
    schedule_id: str