import json, math
import joblib
import pandas as pd
from flask import current_app
class ValidationError(ValueError): pass
def model_data():
    path=current_app.config['ARTIFACT_PATH']
    return joblib.load(path) if path.exists() else None
def metrics():
    path=current_app.config['METRICS_PATH']
    return json.loads(path.read_text()) if path.exists() else None
def locations():
    item=model_data()
    return item['locations'] if item else []
def validate(form):
    try: area=float(form.get('area_sqft',''))
    except (ValueError, TypeError): raise ValidationError('Area must be a valid number.')
    if not math.isfinite(area) or area <= 0: raise ValidationError('Area must be a positive finite number.')
    try: bedrooms=int(form.get('bedrooms',''))
    except (ValueError, TypeError): raise ValidationError('Bedrooms must be a whole number.')
    if not 1 <= bedrooms <= 20: raise ValidationError('Bedrooms must be between 1 and 20.')
    location=form.get('location','').strip()
    if location not in locations(): raise ValidationError('Choose a location supported by this trained model.')
    return area, bedrooms, location
def predict(area, bedrooms, location):
    item=model_data()
    if not item: raise RuntimeError('A trained model artifact is unavailable.')
    value=float(item['pipeline'].predict(pd.DataFrame([{'area_sqft':area,'bedrooms':bedrooms,'location':location}]))[0])
    if not math.isfinite(value): raise RuntimeError('The model returned an invalid result.')
    return max(value, 0)
