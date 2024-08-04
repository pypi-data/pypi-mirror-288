from fastapi import FastAPI, HTTPException, Body, UploadFile, File
from pydantic import BaseModel
from datetime import datetime
from typing import Union
import pandas as pd
from io import StringIO
import json

app = FastAPI()


class Metrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    mean_metrics: float


true_accounts = [100045839024578, 10006682693457, 104357349436, 10000643765876, 6720496739507, 100476457672]
false_accounts = [10004587658558, 10475296598275, 1000528957265, 10000004352786, 10456298726, 1137289347]


@app.get("/true_accounts")
async def get_accounts_true():
    return {"accounts": true_accounts}


@app.get("/false_accounts")
async def get_accounts_false():
    return {"accounts": false_accounts}


@app.post("/processed_df")
async def posted_df(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(StringIO(content.decode("utf-8")))
    # Convert DataFrame to dictionary
    data_dict = df.to_dict(orient="records")
    # Save to JSON file
    json_filename = file.filename.rsplit('.', 1)[0] + "_received_to_fastapi.json"
    with open(json_filename, 'w') as json_file:
        json.dump(data_dict, json_file)
    print(f"Received metrics: {data_dict}")
    return {"filename": file.filename, "data": data_dict}


@app.post("/metrics")
async def receive_metrics(metrics: Metrics):
    try:
        file_path = f"received metrics_to_fastapi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        # Save the metrics to a JSON file
        with open(file_path, "w") as f:
            json.dump(metrics.dict(), f, indent=4)
        print(f"Received metrics: {metrics}")
        return {"message": "Metrics successfully received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
