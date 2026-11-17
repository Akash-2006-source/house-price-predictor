import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
import pandas as pd
from ml.train_model import clean, sqft

def test_sqft_range_and_cleaning():
    assert sqft('1000 - 1200') == 1100
    raw = pd.DataFrame({'location': ['A', 'A', 'B'], 'size': ['2 BHK', '2 BHK', 'bad'], 'total_sqft': ['1000', '1000', '1200'], 'price': [50, 50, 70]})
    df, before = clean(raw)
    assert before == 3 and len(df) == 1 and df.price_inr.iloc[0] == 5000000

def test_sqft_invalid_is_nan():
    assert np.isnan(sqft('not numeric'))
