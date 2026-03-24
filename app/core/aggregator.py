from app.db.database import session_local
from app.models.summary import DashboardSummary
from app.services.analytics import calculate_conversion_funnel

def run_analytics_aggregation():
    print("\n [CRON JOB] Waking up to pre-calculate dashboard metrics...")
    
    # 1. Run the heavy Pandas math we built earlier
    metrics = calculate_conversion_funnel()
    
    # If the database is completely empty, don't do anything
    if "status" in metrics:
        print("[CRON JOB] No events to analyze. Going back to sleep.")
        return

    # 2. Open a private tunnel to the database
    db = session_local()
    try:
        # 3. Save the math into the lightning-fast summary table
        new_summary = DashboardSummary(
            total_events=metrics["total_events_tracked"],
            conversion_rate=metrics["conversion_rate_percentage"],
            top_product_id=metrics["most_viewed_product_id"]
        )
        db.add(new_summary)
        db.commit()
        print(f"[CRON JOB] Success! Conversion Rate ({metrics['conversion_rate_percentage']}%) cached.")
    except Exception as e:
        print(f"[CRON JOB ERROR] Could not save summary: {e}")
    finally:
        db.close() # Always close the door!