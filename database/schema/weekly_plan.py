from sqlalchemy import ForeignKey, String, Integer, Column, Text
from sqlalchemy.orm import Mapped, mapped_column
from database.schema.Base import DBBase

class WeeklyPlan(DBBase):
    __tablename__ = "weekly_plan"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    category: Mapped[str] = mapped_column(String, nullable=False)
    activity: Mapped[str] = mapped_column(String, nullable=False)
    frequency: Mapped[str] = mapped_column(String, nullable=False)
    time: Mapped[str] = mapped_column(String, nullable=False)