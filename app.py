from fastapi import FastAPI
from typing import List
import json

app = FastAPI(
    title="NASA SMD Keyword Service",
    description="API for NASA SMD taxonomy keywords",
    version="1.0"
)

# Load JSON
with open("nasa_smd_classified_keywords.json", "r") as f:
    taxonomy = json.load(f)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "NASA SMD Keyword API running",
        "smds": list(taxonomy.keys())
    }


# Get all SMDs
@app.get("/smds")
def get_smds():
    return {
        "smds": list(taxonomy.keys())
    }


# Get keywords by SMD
@app.get("/keywords/{smd}")
def get_keywords(smd: str):

    if smd not in taxonomy:
        return {"error": "SMD not found"}

    return {
        "smd": smd,
        "total_keywords": len(taxonomy[smd]),
        "keywords": taxonomy[smd]
    }


# Search keywords
@app.get("/search")
def search_keywords(q: str):

    results = []

    for smd, keywords in taxonomy.items():

        for keyword in keywords:

            if q.lower() in keyword.lower():

                results.append({
                    "keyword": keyword,
                    "smd": smd
                })

    return {
        "query": q,
        "count": len(results),
        "results": results[:50]
    }
@app.get("/autocomplete")
def autocomplete(q: str):

    suggestions = []

    for smd, keywords in taxonomy.items():

        for keyword in keywords:

            if keyword.lower().startswith(q.lower()):

                suggestions.append(keyword)

    return {
        "suggestions": suggestions[:20]
    }