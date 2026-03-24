from fastapi import FastAPI, BackgroundTasks, status
from app.schemas.event import EventCreate
from app.models.event import Event, Base
from app.db.database import engine, session_local
from app.services.analytics import calculate_conversion_funnel
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from app.services.analytics import calculate_conversion_funnel
from app.core.aggregator import run_analytics_aggregation
import time

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n Starting the Night Shift Background Scheduler...")
    scheduler = BackgroundScheduler()
    
    # Schedule the job to run exactly every 1 minute
    scheduler.add_job(run_analytics_aggregation, 'interval', minutes=1)
    scheduler.start()
    
    # We also force it to run once right now so we don't have to sit here for 60 seconds waiting!
    run_analytics_aggregation()
    
    yield  # This tells FastAPI: "Okay, start serving the API now!"
    
    print("\n Shutting down the background scheduler safely...")
    scheduler.shutdown()

app = FastAPI(title="EventFlow Analytics API")

def process_event_background(event_data: dict):
    db = session_local()
    try:
        new_event = Event(**event_data)
        db.add(new_event)
        db.commit()
        print(f"[BACKGROUND] Successfully saved event: {event_data['event_type']} with User id {event_data['user_id']}")
    except Exception as e:
        print(f"[ERROR] Could not save to database: {e}")
    finally:
        db.close()
        
@app.post("/events", status_code=status.HTTP_202_ACCEPTED)
async def ingest_event(event: EventCreate, background_tasks: BackgroundTasks):
    event_dict = event.model_dump()
    background_tasks.add_task(process_event_background, event_dict)
    return {"message": "Event received and is processing in the background."}

@app.get("/analytics/dashboard")
async def get_dashboard_metrics():
    
    metrics = calculate_conversion_funnel()
    return metrics