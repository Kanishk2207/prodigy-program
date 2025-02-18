from fastapi import FastAPI, HTTPException, status, UploadFile
from contextlib import asynccontextmanager
import uvicorn
from sqlalchemy import text
from config import settings

from database.sqlite import get_db
from database.migration.migration import run_migrations
from utils.upload_utils import upload_daily_schedule_to_db, upload_weekly_plan_to_db

from api.schedule.router import router as schedule_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    # Run migrations
    try:
        async with get_db() as db:
            await run_migrations(db=db, script_path=settings.MIGRATION_SCRIPT_PATH)
            print(f"Migration script ran")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Migration error")

    # upload weekly plan rules to DB
    try:
        async with get_db() as db:
            await upload_weekly_plan_to_db(db=db)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in uploading weekly plan")

    # Upload daily schedule to db
    try:
        async with get_db() as db:
            await upload_daily_schedule_to_db(db=db)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error in uploading daily schedule")
    
    yield

    # clear DB before exiting the app(as this is just a poc, 
    # I am implimenting this as a quickfix for unique constraint issue, 
    # there can be a better approch to handle this like introducing a api to upload the data rather than this function)
    try:
        async with get_db() as db:
            await db.execute(text('DELETE FROM weekly_plan;'))  
            await db.execute(text('DELETE FROM daily_schedule;'))  
        print("Database cleared.")
    except Exception as ex:
        print(f"Error during cleanup: {ex}")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"message": "app is healthy"}

app.include_router(schedule_router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=9000,
        reload=False,
    )
