from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = PROCESSED_DATA_DIR / "dataset_inventory.csv"


def create_dataset_inventory() -> pd.DataFrame:
    csv_files = sorted(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            f"No CSV files were found in: {RAW_DATA_DIR}"
        )

    inventory = []

    for file_path in csv_files:
        dataframe = pd.read_csv(file_path)

        inventory.append(
            {
                "file_name": file_path.name,
                "row_count": dataframe.shape[0],
                "column_count": dataframe.shape[1],
                "missing_values": int(dataframe.isna().sum().sum()),
                "duplicate_rows": int(dataframe.duplicated().sum()),
                "column_names": ", ".join(dataframe.columns),
            }
        )

    return pd.DataFrame(inventory)


if __name__ == "__main__":
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    inventory_df = create_dataset_inventory()
    inventory_df.to_csv(OUTPUT_FILE, index=False)

    print(inventory_df.to_string(index=False))
    print(f"\nDataset inventory saved to:\n{OUTPUT_FILE}")
