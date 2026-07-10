from datetime import date

from pydantic import BaseModel


class AnalyticsSummary(BaseModel):
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    average_completion_time: float


class DailyTaskCount(BaseModel):
    date: date
    count: int


class AnalyticsDashboardResponse(BaseModel):
    summary: AnalyticsSummary
    completion_rate: float
    tasks_created_by_day: list[DailyTaskCount]
    tasks_completed_by_day: list[DailyTaskCount]