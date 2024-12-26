import os
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

load_dotenv()

database_url: str = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("database not defined")

backend_url: str = 'db+' + database_url

celery_app = Celery(
    'todo',
    broker='redis://localhost:6379/0', # Redis broker URL
    backend=backend_url # Datbase URL
)

celery_app.conf.update(
    result_expires=3600,
    beat_schedule = {
        'send-reminder-for-scheduled-items': {
            'task': 'api.api_v1.tasks.todo_tasks.send_reminder_for_scheduled_task',
            'schedule': crontab(hour=8, minute=0)
        },
        'mark-items-complete-every-morning': {
            'task': 'api.api_v1.tasks.todo_tasks.mark_tasks_as_complete',
            'schedule': crontab(hour=8, minute=0)
        },
    },
)
