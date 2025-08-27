from fastapi import FastAPI, File, Depends, Form, BackgroundTasks, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .db import *
from .digits import *

import json


async def lifespan(app: FastAPI):
    print("Starting up!")
    # insert db initialization
    initialize_db()

    yield
    print("Shutting down!")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/sites")
def add_link(site: Website, db: Session = Depends(get_db)):
    website = insert_website(site, db)
    return {"id": website.id, "name": website.name, "link": website.link, "review": website.review}

@app.post("/data/upload")
async def upload_data(background_tasks: BackgroundTasks, filename: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_async_db)):
    # create record
    data = Data(name=filename, filename=f"{filename}.csv")
    insert = insert_data(data, db)
    contents = await file.read()
    if not await insert:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Data with this name already exists."}
        )
    background_tasks.add_task(process_data, contents, filename, db)
    # add to background tasks
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"filename": filename, "status": "processing"}
    )

@app.get("/data")
def get_data(db: Session = Depends(get_db)):
    ret = get_all_data(db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': ret
        }
    )
    
@app.get("/data/name")
def get_data_by_name(dname: str = Form(...), db: Session = Depends(get_db)):
    print(dname)
    ret = get_by_name(dname, db)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': ret
        }
    )

@app.post("/model/train")
def init_model_train(background_tasks: BackgroundTasks, data: str, db: Session = Depends(get_db)):
    # verify data exists
    current_data = get_by_name(data, db)
    if not current_data:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                'error': "Data does not exist"
            }
        )
    elif current_data[0]['status'] == 'error':
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                'error': "Data upload encountered an error"
            }
        )
    elif current_data[0]['status'] == 'error':
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                'error': "Data is currently processing, please wait"
            }
        )

    background_tasks.add_task(train_model, data, db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': data
        }
    )

@app.get("/model")
def get_models(db: Session = Depends(get_db)):
    ret = get_all_models(db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': ret
        }
    )

@app.get("/model/data")
def get_models_by_data(dataname: str, db: Session = Depends(get_db)):
    ret = get_model_by_data(dataname, db)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'data': ret
        }
    )

@app.post("/model/predict")
def predict(req: Sample, db: Session = Depends(get_db)):
    # verify data exists
    # verify sample has correct number of columns
    # verify model exists
    # predict

    pass

