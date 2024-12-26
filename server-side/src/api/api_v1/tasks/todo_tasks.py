import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from celery import shared_task
from datetime import datetime, timedelta, timezone
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from session import engine
from models.todo import ToDo
from models.users import User
from dotenv import load_dotenv
import os

load_dotenv()

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')

logger = logging.getLogger(__name__)

@shared_task
def send_reminder_for_scheduled_task():
    session_local = sessionmaker(bind=engine)
    db = session_local()
    try:
        start_time = datetime.now(timezone.utc) + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        tasks = db.query(ToDo).filter(
            and_(
                ToDo.completed == False,
                ToDo.scheduled_for > start_time,
                ToDo.scheduled_for <= end_time
            )
        ).all()
        
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        for task in tasks:
            user = db.query(User).get({ 'id': task.user_id })  #we need to use back ref in ToDo model to avoid this line.
            #NOTE: need to revisit the html content once, task.scheduled_for.strftime("%Y-%m-%d %H:%M")
            try:
                message = Mail(
                    from_email=FROM_EMAIL,
                    to_emails=user.email,
                    subject='Reminder for Task: {}'.format(task.title),
                    html_content=f"""
                    <html>
                    <body>
                    <b> Reminder for your task: {task.title}</b><br><br>
                    <p> This email has been sent to because you've an upcoming task schduled for {task.scheduled_for} </p><br> 
                    <p> If you do not complete this task on or before the scheduled time, it'll be automatically marked as completed after {task.scheduled_for}</p><br> 
                    <i><u> You can always find the auto updated task by filtering it based on 'Auto Updated' filter,
                    and if you wish to procrastinate and push this task to some other date you can change the scehduled time 
                    </i></u>
                    </body>
                    </html"""
                )
                sg.send(message)
                task.notification_sent_at = datetime.now()
                logger.info("Email sent for task: {}, to user: {}".format(task.id, task.user_id))
            
            except Exception as email_error:
                logger.error("Error in sending email: {} for task: {}, of user: {}".format(email_error, task.id, task.user_id), exc_info=True)
    
    except Exception as error:
        print("Error in sending reminder for scheduled task: {}".format(error))
        raise error
    finally:
        db.close()


@shared_task
def mark_tasks_as_complete():
    session_local = sessionmaker(bind=engine)
    db = session_local()
    try:
        # fetch all the todo which are incomplete and notification period has elapsed
        items = db.query(ToDo).filter(
            and_ (
                ToDo.completed == False,
                ToDo.notification_sent_at.is_not(None),
                ToDo.notification_sent_at <= datetime.now(timezone.utc) - timedelta(days=1)
            )
        ).all()

        # mark auto_updated as True, complete as False
        for item in items:
            item.completed = True
            item.auto_updated = True
        
        db.commit()

    except Exception as error:
        db.rollback()
        print("Error while marking the task as complete: {}".format(error))
        raise error
    finally:
        db.close()

