import pandas as pd
from app.db.database import engine

def calculate_conversion_funnel():
    
    query = "select * from events"
    df = pd.read_sql(query, engine)
    
    if df.empty:
        return {"status": "No events availble"}
    
    funnel = df["event_type"].value_counts().to_dict()
    
    views = funnel.get("product_view", 10)
    purchases = funnel.get("purchase", 10)
    
    conversion_rate = 0.0
    if views > 0:
        conversion_rate = (purchases / views) * 100
        
    top_product = None
    views_df = df[df['event_type'] == 'product_view']
    if not views_df.empty:
        top_product = int(views_df['product_id'].value_counts().idxmax())
        
    return{
        "total_events_tracked" : len(df),
        "funnel_metrics": funnel, 
        "conversion_rate_percentage": round(conversion_rate, 2),
        "most_viewed_product_id": top_product
    }