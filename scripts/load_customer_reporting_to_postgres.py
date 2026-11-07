
from pathlib import Path

import pandas as pd
import numpy as np


# Locate the project and validated reporting dataset
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "customer_intelligence_reporting.parquet"
)


def load_reporting_data():
    """Load and validate the customer reporting dataset."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Reporting dataset not found: {DATA_PATH}"
        )

    df = pd.read_parquet(DATA_PATH)

    # Validate customer population and uniqueness
    assert len(df) == 78_100
    assert df.shape[1] == 14
    assert df["customer_unique_id"].is_unique
    assert df["customer_unique_id"].notna().all()

    # Validate historical purchasing outcomes
    assert df["repeat_purchase_60d"].sum() == 1_589

    assert np.isclose(
        df["initial_delivered_value"].sum(),
        10_395_105.68,
        atol=0.01
    )

    assert np.isclose(
        df["subsequent_60d_value"].sum(),
        211_295.19,
        atol=0.01
    )

    assert np.isclose(
        df["total_60d_merchandise_value"].sum(),
        10_606_400.87,
        atol=0.01
    )

    print("SOURCE DATA VALIDATION PASSED")
    print(f"Customers: {len(df):,}")
    print(f"Columns: {df.shape[1]}")
    print(f"Unique customers: {df['customer_unique_id'].nunique():,}")
    print(f"Source: {DATA_PATH}")

    return df

def connect_to_postgres():
    """Connect securely to the existing PostgreSQL database."""

    import getpass
    import pg8000.dbapi

    password = getpass.getpass("PostgreSQL password: ")

    connection = pg8000.dbapi.connect(
        user="postgres",
        password=password,
        host="localhost",
        port=5432,
        database="customer_intelligence_v2"
    )

    cursor = connection.cursor()

    try:
        cursor.execute("SELECT current_database(), current_user")
        database_name, database_user = cursor.fetchone()

        assert database_name == "customer_intelligence_v2"

        print("\nPOSTGRESQL CONNECTION SUCCESSFUL")
        print(f"Database: {database_name}")
        print(f"User: {database_user}")

    finally:
        cursor.close()

    return connection


def validate_reporting_table(connection):
    """Verify that the target reporting table is empty and correctly structured."""

    cursor = connection.cursor()

    expected_columns = [
        "customer_unique_id",
        "order_id",
        "order_purchase_timestamp",
        "order_status",
        "first_order_delivery_status",
        "first_order_item_value",
        "repeat_purchase_propensity",
        "propensity_segment",
        "initial_value_segment",
        "customer_profile",
        "repeat_purchase_60d",
        "initial_delivered_value",
        "subsequent_60d_value",
        "total_60d_merchandise_value",
    ]

    try:
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'customer_intelligence_reporting'
            ORDER BY ordinal_position
        """)

        actual_columns = [row[0] for row in cursor.fetchall()]

        assert actual_columns == expected_columns, (
            "Reporting table schema does not match the validated dataset."
        )

        cursor.execute("""
            SELECT COUNT(*)
            FROM public.customer_intelligence_reporting
        """)

        existing_records = cursor.fetchone()[0]

        assert existing_records == 0, (
            f"Import stopped: reporting table already contains "
            f"{existing_records:,} records."
        )

        print("\nPOSTGRESQL REPORTING TABLE VALIDATION PASSED")
        print(f"Table: public.customer_intelligence_reporting")
        print(f"Columns: {len(actual_columns)}")
        print(f"Existing records: {existing_records:,}")
        print("Ready for initial import.")

    finally:
        cursor.close()


def import_customer_reporting(connection, df):
    """Import customer records and commit only after reconciliation."""

    from decimal import Decimal

    table_name = "public.customer_intelligence_reporting"
    columns = df.columns.tolist()
    batch_size = 250

    # Convert Pandas values to PostgreSQL-compatible Python values
    def prepare_value(value):
        if pd.isna(value):
            return None
        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime()
        if isinstance(value, np.generic):
            return value.item()
        return value

    rows = [
        tuple(prepare_value(value) for value in row)
        for row in df.itertuples(index=False, name=None)
    ]

    column_sql = ", ".join(columns)
    row_placeholder = "(" + ", ".join(["%s"] * len(columns)) + ")"

    cursor = connection.cursor()

    try:
        print("\nSTARTING CUSTOMER REPORTING IMPORT")

        # Insert records in manageable batches
        for start in range(0, len(rows), batch_size):
            batch = rows[start:start + batch_size]

            placeholders = ", ".join(
                [row_placeholder] * len(batch)
            )

            insert_sql = (
                f"INSERT INTO {table_name} ({column_sql}) "
                f"VALUES {placeholders}"
            )

            parameters = [
                value
                for row in batch
                for value in row
            ]

            cursor.execute(insert_sql, parameters)

        print("All batches inserted. Validating before commit.")

        # Reconcile against the validated Notebook 11 results
        cursor.execute("""
            SELECT
                COUNT(*),
                COUNT(DISTINCT customer_unique_id),
                SUM(repeat_purchase_60d),
                SUM(initial_delivered_value),
                SUM(subsequent_60d_value),
                SUM(total_60d_merchandise_value),
                COUNT(*) FILTER (
                    WHERE first_order_item_value IS NULL
                )
            FROM public.customer_intelligence_reporting
        """)

        (
            customer_count,
            unique_customers,
            repeat_purchasers,
            initial_value,
            subsequent_value,
            total_value,
            missing_initial_values
        ) = cursor.fetchone()

        assert customer_count == 78_100
        assert unique_customers == 78_100
        assert repeat_purchasers == 1_589
        assert initial_value == Decimal("10395105.68")
        assert subsequent_value == Decimal("211295.19")
        assert total_value == Decimal("10606400.87")
        assert missing_initial_values == 642

        print("\nPOSTGRESQL RECONCILIATION PASSED")
        print(f"Customers: {customer_count:,}")
        print(f"Unique customers: {unique_customers:,}")
        print(f"Repeat purchasers: {repeat_purchasers:,}")
        print(f"Initial delivered value: R${initial_value:,.2f}")
        print(f"Subsequent value: R${subsequent_value:,.2f}")
        print(f"Total 60-day value: R${total_value:,.2f}")
        print(f"Missing initial basket values: {missing_initial_values:,}")

        # Make changes permanent only after all checks pass
        connection.commit()
        print("\nDATABASE IMPORT COMMITTED SUCCESSFULLY")

    except Exception:
        connection.rollback()
        print("\nIMPORT FAILED. TRANSACTION ROLLED BACK.")
        raise

    finally:
        cursor.close()



if __name__ == "__main__":
    reporting_data = load_reporting_data()

    connection = connect_to_postgres()

    try:
        validate_reporting_table(connection)
        import_customer_reporting(connection, reporting_data)
    finally:
        connection.close()
        print("\nDatabase connection closed successfully.")

