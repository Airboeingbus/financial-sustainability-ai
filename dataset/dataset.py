import pandas as pd
import numpy as np
from pathlib import Path

np.random.seed(42)

rows = 200
OUTPUT_DIR = Path(__file__).resolve().parent


def generate_dataset(type_name):
    
    if type_name == "good":
        decline_rate = np.random.uniform(0.5, 2.5, rows)
        delay_hours = np.random.uniform(0.1, 0.8, rows)
        carbon_intensity = np.random.uniform(20, 50, rows)
        esg_score = np.random.uniform(80, 95, rows)

    elif type_name == "medium":
        decline_rate = np.random.uniform(3, 7, rows)
        delay_hours = np.random.uniform(1, 2, rows)
        carbon_intensity = np.random.uniform(60, 90, rows)
        esg_score = np.random.uniform(55, 75, rows)

    else:  # bad
        decline_rate = np.random.uniform(10, 20, rows)
        delay_hours = np.random.uniform(3, 6, rows)
        carbon_intensity = np.random.uniform(110, 160, rows)
        esg_score = np.random.uniform(20, 45, rows)

    txn_volume = np.random.randint(7000, 15000, rows)

    sustainability_score = (
        esg_score * 0.6
        + (100 - carbon_intensity) * 0.2
        + (100 - decline_rate * 3) * 0.1
        + (100 - delay_hours * 10) * 0.1
    )

    df = pd.DataFrame({
        "txn_volume": txn_volume,
        "decline_rate": decline_rate,
        "delay_hours": delay_hours,
        "carbon_intensity": carbon_intensity,
        "esg_score": esg_score,
        "sustainability_score": sustainability_score.round(2)
    })

    return df


if __name__ == "__main__":
    good_df = generate_dataset("good")
    medium_df = generate_dataset("medium")
    bad_df = generate_dataset("bad")

    good_df.to_csv(OUTPUT_DIR / "good_finance_data.csv", index=False)
    medium_df.to_csv(OUTPUT_DIR / "medium_finance_data.csv", index=False)
    bad_df.to_csv(OUTPUT_DIR / "bad_finance_data.csv", index=False)

    print("Datasets generated successfully.")