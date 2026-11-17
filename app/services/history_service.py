from sqlalchemy import select
from ..database import session
from ..models import Prediction
def save(area, bedrooms, location, price):
    db=session()
    try:
        record=Prediction(area_sqft=area, bedrooms=bedrooms, location=location, predicted_price_inr=price); db.add(record); db.commit(); return record
    except Exception:
        db.rollback(); raise
    finally: db.close()
def recent(limit):
    db=session()
    try: return db.scalars(select(Prediction).order_by(Prediction.created_at.desc()).limit(limit)).all()
    finally: db.close()
