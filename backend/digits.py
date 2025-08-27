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

async def process_data(contents, filename: str, db: AsyncSession): 
    try:
        with open(f"data/{filename}.csv", "wb") as f:
            f.write(contents)
        df = pd.read_csv(f"data/{filename}.csv")
        rows, cols = df.shape
        if 'target' not in df.columns:
            await update_data(Data(name=filename, filename=f"{filename}.csv", rows=rows, cols=cols, status="error", error="No target column provided"), db)
            return {"filename": filename, "rows": rows, "cols": cols, "status": "error"}
        await update_data(Data(name=filename, filename=f"{filename}.csv", rows=rows, cols=cols, status="done"), db)
        return {"filename": filename, "rows": rows, "cols": cols, "status": "processed"}
    except Exception as e:
        print(e)
        await update_data(Data(name=filename, filename=f"{filename}.csv", rows=0, cols=0, status="error", error="Error occurred during upload"), db)
        return {"filename": filename, "rows": 0, "cols": 0, "status": "error"}

def train_model(filename: str, db: Session, test_size: float = 0.2, random_state: int = datetime.now().microsecond):
    if filename not in data_cache:
        data_cache[filename] = pd.read_csv(f'data/{filename}.csv')
    data = data_cache[filename]


    X_train, X_test, y_train, y_test = train_test_split(data.drop(columns=['target']), data['target'], test_size=test_size, random_state=random_state)
    
    model = sklearn.svm.LinearSVC(dual='auto') 
    model.fit(X_train, y_train)
    # save model to models folder
    # use pickle

    # put into database
    model_name = f"{filename}_svm"
    model_record = Model(
        name = model_name,
        datafile = filename, 
        algorithm = "SVM"
    )
    status = insert_model(model_record, db)
    if status is None:
        return None
    
    jl.dump(model, f'{model_name}.joblib')
    return status



async def predict_with_model(filename: str, data: list[list[float]]):
    # load model from models folder
    pass 


