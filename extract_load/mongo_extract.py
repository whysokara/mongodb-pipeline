import pymongo
import certifi
import pandas as pd
import os
from dotenv import load_dotenv
from snowflake_load import load_data_to_snowflake

# Load environment variables
load_dotenv()

ca = certifi.where()
uri = os.getenv("MONGO_URI")

if not uri:
    raise ValueError("MONGO_URI not found in .env file")

client = pymongo.MongoClient(uri, tlsCAFile=ca)
db = client["sample_mflix"]
movies_collection = db["movies"]

cursor = movies_collection.find({})

cursor_df = pd.DataFrame(list(cursor))

column_to_keep = ["title", "year", "runtime","released","rated"]
df = cursor_df[column_to_keep]
# print(df.head())

load_data_to_snowflake(df, "RAW_MOVIES")