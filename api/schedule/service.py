from database.crud import fetch_activities_by_day, mark_activity_completed
from sqlalchemy.ext.asyncio import AsyncSession

async def get_daily_schedule_activities(day):
    """Fetch all scheduled activities from the database."""
    schedule = await fetch_activities_by_day(day=day)
    return schedule

async def update_daily_activity_as_completed(schedule_id):
    """Update scheduled activity as completed"""
    schedule = await mark_activity_completed(schedule_id=schedule_id)
    return schedule