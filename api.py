# api.py
from fastapi import FastAPI
from pydantic import BaseModel
from recommender import recommend_assessments
from dataset import shl_catalog

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/recommend")
def get_recommendations(data: QueryInput):
    results = recommend_assessments(data.query, shl_catalog, top_n=10)
    return {"recommendations": results}
