from fastapi import FastAPI, File, Depends, Form, BackgroundTasks, UploadFile
from sqlalchemy.orm import Session
from .db import *
from .digits import *


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
async def upload_data(background_tasks: BackgroundTasks, file: UploadFile = File(...), filename: str = Form(...), db: Session = Depends(get_db)):
    # create record
    data = Data(name=filename, filename=f"{filename}.csv")
    insert_data(data, db)
    background_tasks.add_task(process_data, file, filename, db)
    # add to background tasks
    return {"filename": filename, "status": "processing"}


