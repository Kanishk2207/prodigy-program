from sqlalchemy.ext.asyncio import AsyncSession
from database.schema.daily_schedule import DailySchedule
from database.schema.weekly_plan import WeeklyPlan
from sqlalchemy import select
from database.sqlite import get_db


async def fetch_activities_by_day(day):
    query = (
        select(DailySchedule.id, DailySchedule.day, WeeklyPlan.activity, DailySchedule.completed)
        .join(WeeklyPlan, DailySchedule.activity_id == WeeklyPlan.id)
        .where(DailySchedule.day == day)
    )
    
    async with get_db() as db:
        query_result = (await db.execute(query))

    # rules_list = [rule.__dict__ for rule in results]
    return [result._asdict() for result in query_result]


async def mark_activity_completed(schedule_id):
    query = (
            select(DailySchedule)
            .where(DailySchedule.id == schedule_id)
        )
    
    async with get_db() as db:
        result = await db.execute(query)
        activity = result.scalars().first()
    
        if activity:
            if activity.completed == 1:
                return {"message": "Activity already completed"}
            activity.completed = 1  # Mark as completed
            await db.commit()
            return {"message": "Activity marked as completed"}
        return {"message": "Activity not found"}
    