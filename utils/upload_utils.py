import uuid
import pandas as pd
from io import StringIO
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert
from database.schema.weekly_plan import WeeklyPlan 
from database.schema.daily_schedule import DailySchedule 
from config import settings

async def upload_weekly_plan_to_db(db: AsyncSession):
    try:
        weekly_plan_csv_path = os.path.join(settings.DEFAULT_RESOURCE_PATH, "weekly_plan.csv")
        with open(weekly_plan_csv_path, 'r') as f:
            weekly_plan_csv = f.read()
        
        weekly_plan_df = pd.read_csv(StringIO(weekly_plan_csv))

        weekly_plan_df = weekly_plan_df.rename(columns={
            "ID": "id", 
            "Category": "category",
            "Activity": "activity",
            "Frequency": "frequency",
            "Time": "time"
        })

        weekly_plan_df = weekly_plan_df.where(pd.notnull(weekly_plan_df), None)

        weekly_plan_records = weekly_plan_df.to_dict(orient="records")

        query = insert(WeeklyPlan).values(weekly_plan_records)
        await db.execute(query)
        await db.commit()

        print("Weekly Plan data uploaded successfully!")

    except Exception as e:
        await db.rollback()
        print(f"An error occurred while uploading weekly plan data: {e}")

async def upload_daily_schedule_to_db(db: AsyncSession):
    try:
        daily_schedule_csv_path = os.path.join(settings.DEFAULT_RESOURCE_PATH, "daily_schedule.csv")
        with open(daily_schedule_csv_path, 'r') as f:
            daily_schedule_csv = f.read()

        daily_schedule_df = pd.read_csv(StringIO(daily_schedule_csv))

        daily_schedule_df = daily_schedule_df.rename(columns={
            "Day": "day",
            "Activity_ID": "activity_id" 
        })

        daily_schedule_df["completed"] = False

        daily_schedule_records = [
            {
                "id": str(uuid.uuid4()),
                "day": int(row["day"]),
                "activity_id": str(row["activity_id"]),  
                "completed": bool(row["completed"])
            }
            for _, row in daily_schedule_df.iterrows()
        ]

        query = insert(DailySchedule).values(daily_schedule_records)
        await db.execute(query)
        await db.commit()

        print("Daily Schedule data uploaded successfully!")

    except Exception as e:
        await db.rollback()
        print(f"An error occurred while uploading daily schedule data: {e}")

