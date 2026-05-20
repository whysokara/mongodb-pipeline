import pymongo
import certifi
import pandas as pd

ca = certifi.where()

uri = "mongodb+srv://imhkara_db_user:ydlWD7YBXWFRKR6S@my-cluster.ho8yevg.mongodb.net/"
client = pymongo.MongoClient(uri, tlsCAFile=ca)
db = client["sample_mflix"]
movies_collection = db["movies"]

cursor = movies_collection.find({})

cursor_df = pd.DataFrame(list(cursor))

column_to_keep = ["title", "year", "runtime","released","rated"]
df = cursor_df[column_to_keep]
print(df.head())