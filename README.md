# House Price Predictor

🌐 **Live Deployed Application:** [https://house-price-predictor-482i.onrender.com](https://house-price-predictor-482i.onrender.com)  
📦 **Container Registry (GHCR):** [`ghcr.io/akash-2006-source/house-price-predictor:v1`](https://github.com/Akash-2006-source/house-price-predictor/pkgs/container/house-price-predictor) (`podman pull ghcr.io/akash-2006-source/house-price-predictor:v1`)

A Flask + scikit-learn capstone for 21CSE216P. It predicts Bengaluru property **asking/sale-price estimates** from area, BHK, and locality, and saves successful predictions in PostgreSQL.

## Honest dataset status

The application is trained from the public **Bengaluru House Price Data** dataset by Amitabh Ajoy on Kaggle (commonly distributed as `Bengaluru_House_Data.csv`; Kaggle terms apply). The current development run used 12,329 cleaned records and records its actual MAE, RMSE, locations, artifact, and plot. The CSV and generated model remain Git-ignored; obtain the dataset and run `python -m ml.train_model` before making a new image. See [DATASET.md](DATASET.md) for provenance, cleaning, results, and limitations.

Raw fields used: `location`, `size` (first integer becomes bedrooms), `total_sqft` (numeric values/ranges are accepted), and `price` (dataset values in lakh INR, converted to INR). Missing/invalid rows and duplicates are removed. This listing dataset can be incomplete, geographically biased, and may reflect asking rather than transacted prices; estimates are not valuations.

## Local development

```powershell
py -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt -r requirements-dev.txt
Copy-Item .env.example .env
python -m ml.train_model     # after adding the licensed dataset
flask --app app:create_app run --debug
pytest
```

Without an artifact, the UI shows an explicit unavailable state; it never invents a price. For local SQLite-only demo/testing set `DATABASE_URL=sqlite:///history.db`. Production uses PostgreSQL. Train before `podman build` because the trained Git-ignored artifact is deliberately copied into the local runtime image.

## Podman

On Windows, install Podman Desktop and initialize the Linux VM with `podman machine init; podman machine start` before running the container commands below. The image, network, and persistence checks require that local Podman machine.

```powershell
podman compose up --build
# or manual, to demonstrate network and volume concepts
podman network create house-price-net
podman volume create house-price-pgdata
podman run -d --name house-price-db --network house-price-net --network-alias db --volume house-price-pgdata:/var/lib/postgresql/data --env POSTGRES_DB=houseprices --env POSTGRES_USER=houseapp --env POSTGRES_PASSWORD=change-me postgres:16-alpine
podman build -t house-price-predictor:v1 .
podman run -d --name house-price-app --network house-price-net -p 5000:5000 --env DATABASE_URL=postgresql+psycopg://houseapp:change-me@db:5432/houseprices house-price-predictor:v1
```

Do not publish the database port. Removing `house-price-db` does **not** delete `house-price-pgdata`; `podman volume rm house-price-pgdata` does. Verify persistence by create prediction → `podman rm -f house-price-db` → re-run the DB command → refresh History.

Useful troubleshooting: `podman ps -a`, `podman images`, `podman logs house-price-app`, `podman inspect house-price-app`, `podman network inspect house-price-net`, `podman volume inspect house-price-pgdata`. For port conflicts change `APP_PORT`; if the app starts before the DB is ready, Compose health checks gate it and the app returns a safe history-unavailable notice. Missing artifact? train it and rebuild. Registry: `podman login docker.io`; `podman tag house-price-predictor:v1 docker.io/<your-namespace>/house-price-predictor:v1`; `podman push docker.io/<your-namespace>/house-price-predictor:v1`; then `podman pull ...`.

To publish source: `git init; git add .; git commit -m "House price predictor"; git remote add origin https://github.com/<you>/house-price-predictor.git; git push -u origin main`.
