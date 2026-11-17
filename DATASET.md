# Dataset record

## Selected data

- **Name:** Bengaluru House Price Data
- **Original source:** [Kaggle: amitabhajoy/bengaluru-house-price-data](https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data)
- **Workspace download mirror:** [abhishek-msh/Bengaluru-House-Price-Prediction](https://github.com/abhishek-msh/Bengaluru-House-Price-Prediction)
- **Local filename:** `data/raw/Bengaluru_House_Data.csv` (Git-ignored)
- **License/usage:** The public mirror does not declare a license. Treat it as an educational dataset; follow the original Kaggle dataset terms and do not redistribute it in this repository or container image.

## Training run performed on 3 November 2026

The downloaded CSV held **13,320** records. The pipeline used **12,329** records, trained on **9,863**, and evaluated on a held-out **2,466** records (random seed 42). The generated artifact records the following true held-out metrics:

- MAE: ₹45,07,703
- RMSE: ₹1,18,32,327

`location` is categorical locality, `size` supplies the first BHK number, `total_sqft` supplies the property area (ranges are averaged), and `price` is the target in lakh INR, converted to INR. Rows with missing or invalid selected values, nonpositive area/price, invalid BHK, and exact duplicates are dropped.

The data likely represents listings rather than confirmed sale prices and has locality/market-time coverage bias. It should not be used for a financial or valuation decision.
