from fastapi import FastAPI, Query
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["Outbound"]  # Your database name
collection = db["outbound"]  # Your collection name

@app.get("/shipments")
def get_shipments(customer: str = None, postcode: str = None):
    query = {}

    if customer:
        query["Customer"] = {"$regex": customer, "$options": "i"}  # Case-insensitive search
    if postcode:
        query["SHORT_POSTCODE"] = postcode.upper()

    results = collection.find(query)

    response = []
    for doc in results:
        response.append({
            "PROD_TYPE": doc.get("PROD_TYPE"),
            "Customer": doc.get("Customer"),
            "SHIPPED_DATE": doc.get("SHIPPED_DATE"),
            "Total_Orders": doc.get("Total_Orders"),
            "Total_Pallets": doc.get("Total_Pallets"),
            "Distance": doc.get("Distance"),
            "Cost": doc.get("Cost"),
            "SHORT_POSTCODE": doc.get("SHORT_POSTCODE")
        })

    return response