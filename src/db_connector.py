"""
Hapi 4.1 — Lidhja me MongoDB (Dev D).

Koleksionet e propozuara:
- raw_uploads
- monthly_analytics
- recommendations_log
- kpi_history
"""

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("MONGO_DB_NAME", "online_retail_analytics")


def get_db():
    """Kthen objektin e databazës MongoDB. TODO: error handling, connection pooling."""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]
