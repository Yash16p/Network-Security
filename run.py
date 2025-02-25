import pandas as pd
import pymongo

MONGO_DB_URL = "mongodb+srv://yash_1626:Yash123@cluster0.vw0ym.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(MONGO_DB_URL)
db = client["YASHAI"]
collection = db["NetworkData"]

# Convert MongoDB documents to Pandas DataFrame
data = list(collection.find())  # Get all records
df = pd.DataFrame(data).drop(columns=['_id'])  # Remove MongoDB's default ID

print(df.head())  # Display first 5 rows
