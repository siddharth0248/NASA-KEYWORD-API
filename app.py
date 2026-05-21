from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(
    title="NASA SMD Taxonomy API",
    description="NASA Science Mission Directorate Topic and Keyword Service",
    version="2.0"
)

# Enable browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load taxonomy
with open("nasa_smd_full_topic_keywords.json", "r") as f:
    taxonomy = json.load(f)


@app.get("/")
def home():
    return {
        "message": "NASA SMD Taxonomy API Running",
        "total_smds": len(taxonomy),
        "smds": list(taxonomy.keys())
    }

# ----------------------------------------
# Get all SMDs
# ----------------------------------------
@app.get("/smds")
def get_smds():
    return {
        "smds": list(taxonomy.keys())
    }


# ----------------------------------------
# Get topics for an SMD
# ----------------------------------------
@app.get("/topics/{smd}")
def get_topics(smd: str):

    if smd not in taxonomy:
        return {"error": "SMD not found"}

    topics = list(taxonomy[smd]["topics"].keys())

    return {
        "smd": smd,
        "topics": topics,
        "count": len(topics)
    }
# ----------------------------------------
# Get keywords for topic
# ----------------------------------------
@app.get("/keywords/{smd}/{topic}")
def get_keywords(smd: str, topic: str):

    if smd not in taxonomy:
        return {"error": "SMD not found"}

    topics = taxonomy[smd]["topics"]

    if topic not in topics:
        return {"error": "Topic not found"}

    keywords = topics[topic]

    return {
        "smd": smd,
        "topic": topic,
        "total_keywords": len(keywords),
        "keywords": keywords
    }

# ----------------------------------------
# Global keyword search
# ----------------------------------------
@app.get("/search")
def search_keywords(q: str):

    results = []

    for smd, smd_data in taxonomy.items():

        for topic, keywords in smd_data["topics"].items():

            for keyword in keywords:

                if q.lower() in keyword.lower():

                    results.append({
                        "keyword": keyword,
                        "topic": topic,
                        "smd": smd
                    })

    return {
        "query": q,
        "count": len(results),
        "results": results[:100]
    }


# ----------------------------------------
# Autocomplete
# ----------------------------------------
@app.get("/autocomplete")
def autocomplete(q: str):

    suggestions = []

    for smd, smd_data in taxonomy.items():

        for topic, keywords in smd_data["topics"].items():

            for keyword in keywords:

                if keyword.lower().startswith(q.lower()):
                    suggestions.append(keyword)

    unique_suggestions = list(set(suggestions))

    return {
        "query": q,
        "suggestions": sorted(unique_suggestions)[:20]
    }