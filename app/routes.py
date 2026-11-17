from flask import Blueprint, flash, redirect, render_template, request, url_for
from .services import prediction_service as ps
from .services import history_service as hs
web=Blueprint('web', __name__)
def fmt(v):
    """Format whole rupees using Indian digit grouping (for example ₹85,00,000)."""
    digits = str(int(round(float(v))))
    if len(digits) <= 3:
        return f'₹{digits}'
    tail, head = digits[-3:], digits[:-3]
    groups = []
    while head:
        groups.append(head[-2:])
        head = head[:-2]
    return '₹' + ','.join(reversed(groups)) + ',' + tail
@web.app_template_filter('inr')
def inr(v): return fmt(v)
@web.route('/')
def index():
    try: records=hs.recent(5); db_error=False
    except Exception: records=[]; db_error=True
    return render_template('index.html', metrics=ps.metrics(), records=records, db_error=db_error)
@web.route('/predict', methods=['GET','POST'])
def predict():
    result=None
    if request.method=='POST':
        try:
            area,bedrooms,location=ps.validate(request.form); price=ps.predict(area,bedrooms,location); hs.save(area,bedrooms,location,price)
            result={'area':area,'bedrooms':bedrooms,'location':location,'price':price}
        except ps.ValidationError as exc: flash(str(exc),'error')
        except Exception: flash('Prediction could not be saved. Please try again shortly.','error')
    return render_template('predict.html', locations=ps.locations(), result=result)
@web.route('/performance')
def performance(): return render_template('performance.html', metrics=ps.metrics())
@web.route('/history')
def history():
    try: return render_template('history.html', records=hs.recent(50), db_error=False)
    except Exception: return render_template('history.html', records=[], db_error=True)
@web.route('/about')
def about(): return render_template('about.html')
@web.route('/health')
def health(): return {'status': 'ok'}, 200
