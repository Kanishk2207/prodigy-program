from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.sqlite import get_db
from api.schedule.service import get_daily_schedule_activities, update_daily_activity_as_completed
from api.schedule.models import MarkCompleted

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/all")
async def fetch_daily_schedule_rules(day: int):
    """Endpoint to fetch all scheduled activities."""

    schedule = await get_daily_schedule_activities(day=day)

    return {"data": schedule}

@router.post("/complete")
async def mark_complete_activity(request: MarkCompleted):
    """Endpoint mark activity completed"""

    schedule = await update_daily_activity_as_completed(schedule_id=request.schedule_id)

    return {"data": schedule}
