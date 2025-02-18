from sqlalchemy import ForeignKey, String, Integer, Column, Text
from sqlalchemy.orm import Mapped, mapped_column
from database.schema.Base import DBBase

from sqlalchemy import ForeignKey, String, Integer, Column, Text
from sqlalchemy.orm import Mapped, mapped_column
from database.schema.Base import DBBase

class DailySchedule(DBBase):
    __tablename__ = "daily_schedule"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    day: Mapped[int] = mapped_column(nullable=False)
    activity_id: Mapped[str] = mapped_column(String, ForeignKey("weekly_plan.id"), nullable=False)
    completed: Mapped[bool] = mapped_column(Integer, default=0)