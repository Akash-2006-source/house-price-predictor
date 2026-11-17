import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import joblib
import pytest
from app import create_app

class FakePipeline:
    def predict(self, frame):
        return [8500000.0]

@pytest.fixture
def client(tmp_path):
    artifact = tmp_path / 'model.joblib'
    joblib.dump({'pipeline': FakePipeline(), 'locations': ['Indiranagar']}, artifact)
    app = create_app({'TESTING': True, 'DATABASE_URL': f"sqlite:///{tmp_path / 'test.db'}", 'ARTIFACT_PATH': artifact, 'METRICS_PATH': tmp_path / 'none.json', 'SECRET_KEY': 'test'})
    return app.test_client()

def test_pages(client):
    for path in ['/', '/predict', '/performance', '/history', '/about']:
        assert client.get(path).status_code == 200

def test_valid_prediction_saves_history(client):
    response = client.post('/predict', data={'area_sqft': '1200', 'bedrooms': '2', 'location': 'Indiranagar'})
    assert '₹85,00,000'.encode() in response.data
    assert b'Indiranagar' in client.get('/history').data

@pytest.mark.parametrize('data', [
    {'area_sqft': '-1', 'bedrooms': '2', 'location': 'Indiranagar'},
    {'area_sqft': 'bad', 'bedrooms': '2', 'location': 'Indiranagar'},
    {'area_sqft': '200', 'bedrooms': '0', 'location': 'Indiranagar'},
    {'area_sqft': '200', 'bedrooms': '2', 'location': 'Unknown'},
])
def test_invalid_input(client, data):
    assert b'alert' in client.post('/predict', data=data).data
