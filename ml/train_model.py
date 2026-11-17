"""Train only from a user-supplied, documented Bengaluru CSV; never synthesize production data."""
import json, re
from pathlib import Path
import joblib, matplotlib.pyplot as plt, numpy as np, pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
ROOT=Path(__file__).resolve().parent.parent; RAW=ROOT/'data/raw/Bengaluru_House_Data.csv'; ART=ROOT/'artifacts'; PLOT=ROOT/'app/static/images/actual_vs_predicted.png'
def sqft(value):
    try:
        nums=[float(x) for x in re.findall(r'\d+(?:\.\d+)?', str(value))]
        return sum(nums)/len(nums) if nums else np.nan
    except ValueError: return np.nan
def clean(raw):
    required={'location','size','total_sqft','price'}
    if not required.issubset(raw.columns): raise ValueError(f'Dataset must contain {sorted(required)}.')
    df=raw[['location','size','total_sqft','price']].copy(); before=len(df)
    df['bedrooms']=pd.to_numeric(df['size'].astype(str).str.extract(r'(\d+)')[0],errors='coerce'); df['area_sqft']=df['total_sqft'].map(sqft); df['price_inr']=pd.to_numeric(df['price'],errors='coerce')*100000
    df['location']=df['location'].astype(str).str.strip(); df=df.drop(columns=['size','total_sqft','price']).replace([np.inf,-np.inf],np.nan).dropna().drop_duplicates()
    df=df[(df.area_sqft>100)&(df.bedrooms.between(1,20))&(df.price_inr>0)]
    return df, before
def train(dataset=RAW):
    raw=pd.read_csv(dataset); df,before=clean(raw)
    if len(df)<20: raise ValueError('Need at least 20 valid records after cleaning.')
    x=df[['area_sqft','bedrooms','location']]; y=df.price_inr
    xtr,xte,ytr,yte=train_test_split(x,y,test_size=.2,random_state=42)
    prep=ColumnTransformer([('numeric',SimpleImputer(strategy='median'),['area_sqft','bedrooms']),('location',OneHotEncoder(handle_unknown='ignore'),['location'])])
    pipe=Pipeline([('preprocess',prep),('regression',LinearRegression())]).fit(xtr,ytr); pred=pipe.predict(xte)
    ART.mkdir(exist_ok=True); PLOT.parent.mkdir(parents=True,exist_ok=True)
    joblib.dump({'pipeline':pipe,'locations':sorted(df.location.unique())},ART/'model.joblib')
    report={'model':'Linear Regression','source_file':str(dataset.name),'records_loaded':int(before),'records_used':int(len(df)),'training_records':int(len(xtr)),'testing_records':int(len(xte)),'mae_inr':float(mean_absolute_error(yte,pred)),'rmse_inr':float(root_mean_squared_error(yte,pred)),'cleaning':'Dropped duplicate, missing, nonpositive, invalid area/BHK/price rows; sqft ranges averaged; price lakh converted to INR.'}
    (ART/'metrics.json').write_text(json.dumps(report,indent=2))
    lo,hi=min(yte.min(),pred.min()),max(yte.max(),pred.max()); plt.figure(figsize=(7,5)); plt.scatter(yte,pred,alpha=.65,color='#157a6e'); plt.plot([lo,hi],[lo,hi],'--',color='#17243b'); plt.xlabel('Actual price (INR)'); plt.ylabel('Predicted price (INR)'); plt.title('Actual vs predicted: held-out test set'); plt.tight_layout(); plt.savefig(PLOT,dpi=150); plt.close(); return report
if __name__=='__main__': print(json.dumps(train(),indent=2))
