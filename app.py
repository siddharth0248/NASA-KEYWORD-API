from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI(
    title="NASA SMD Taxonomy API",
    description="NASA Science Mission Directorate Keyword Service",
    version="3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TAXONOMY_FILE = Path("nasa_smd_keyword.json")

with TAXONOMY_FILE.open("r", encoding="utf-8") as f:
    taxonomy: dict[str, list[str]] = json.load(f)


@app.get("/")
def home():
    return {
        "message": "NASA SMD Taxonomy API Running",
        "total_smds": len(taxonomy),
        "smds": list(taxonomy.keys()),
        "total_keywords": sum(len(keywords) for keywords in taxonomy.values())
    }


@app.get("/smds")
def get_smds():
    return {
        "count": len(taxonomy),
        "smds": list(taxonomy.keys())
    }


@app.get("/keywords/{smd}")
def get_keywords_by_smd(smd: str):
    if smd not in taxonomy:
        raise HTTPException(status_code=404, detail="SMD not found")

    keywords = taxonomy[smd]

    return {
        "smd": smd,
        "total_keywords": len(keywords),
        "keywords": keywords
    }


@app.get("/search")
def search_keywords(q: str = Query(..., min_length=1)):
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
        "results": results[:100]
    }


@app.get("/autocomplete")
def autocomplete(q: str = Query(..., min_length=1)):
    suggestions = set()

    for keywords in taxonomy.values():
        for keyword in keywords:
            if keyword.lower().startswith(q.lower()):
                suggestions.add(keyword)

    return {
        "query": q,
        "suggestions": sorted(suggestions)[:20]
    }


@app.get("/keyword/{keyword}")
def get_keyword_smds(keyword: str):
    matches = []

    for smd, keywords in taxonomy.items():
        for kw in keywords:
            if kw.lower() == keyword.lower():
                matches.append(smd)

    if not matches:
        raise HTTPException(status_code=404, detail="Keyword not found")

    return {
        "keyword": keyword,
        "smds": matches,
        "count": len(matches)
    }