import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_snowflake_connection():
    """
    Establishes a connection to Snowflake using credentials from the .env file.
    """
    return snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        role=os.getenv("SNOWFLAKE_ROLE")
    )

def load_data_to_snowflake(df, table_name):
    """
    Loads a pandas DataFrame into a Snowflake table.
    If the table doesn't exist, it will be created automatically.
    """
    # 1. Prepare the DataFrame
    # Convert all data to string to avoid conversion errors in the RAW layer.
    # We will handle type casting in dbt.
    df = df.astype(str)
    
    # Snowflake prefers uppercase column names
    df.columns = [col.upper() for col in df.columns]
    table_name = table_name.upper()

    # 2. Connect and Load
    conn = get_snowflake_connection()
    try:
        print(f"Starting load to Snowflake table: {table_name}...")
        
        # write_pandas is the most efficient way to upload data.
        # auto_create_table=True means you DO NOT need to run SQL manually.
        # overwrite=True will replace the table if it exists (good for raw refreshes).
        success, nchunks, nrows, _ = write_pandas(
            conn=conn,
            df=df,
            table_name=table_name,
            auto_create_table=True,
            overwrite=True 
        )

        if success:
            print(f"✅ Success! Loaded {nrows} rows into {table_name}.")
        else:
            print("❌ The load failed.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # This block is for testing purposes only
    print("Snowflake Loader script initialized.")
    # Example:
    # test_df = pd.DataFrame({'COL1': [1, 2], 'COL2': ['A', 'B']})
    # load_data_to_snowflake(test_df, 'TEST_TABLE')
