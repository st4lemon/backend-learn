import sklearn
import pandas as pd
import numpy as np
import joblib as jl
import os
from datetime import datetime
from sklearn import datasets
from sklearn.model_selection import train_test_split
from fastapi import UploadFile, File, Form
from .db import *

model_cache = {}
data_cache = {}

# assume all data is pandas for now

async def process_data(file: UploadFile, filename: str, db: Session):
    contents = await file.read()
    with open(f"../data/{filename}.csv", "wb") as f:
        f.write(contents)
    df = pd.read_csv(f"../data/{filename}.csv")
    rows, cols = df.shape
    update_data(Data(name=filename, filename=f"{filename}.csv", rows=rows, cols=cols, status="done"), db)
    return {"filename": filename, "rows": rows, "cols": cols, "status": "processed"}

async def train_model(filename: str | None = None, test_size: float = 0.2, random_state: int = datetime.now().microsecond):
    if filename:
        # load dataset from data folder, append csv
        pass
    else:
        data = datasets.load_digits()

    X_train, X_test, y_train, y_test = train_test_split(data['data'], data['target'], test_size=test_size, random_state=random_state)
    
    model = sklearn.svm.LinearSVC(dual='auto')
    model.fit(X_train, y_train)
    # save model to models folder
    # use pickle


async def predict_with_model(filename: str, data: list[list[float]]):
    # load model from models folder
    pass 


