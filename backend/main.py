from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .db import *

class PostSite(BaseModel):
    name: str 
    link: str
    review: str | None = None


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
def add_link(site: PostSite, db: Session = Depends(get_db)):
    website = Website(name=site.name, link=site.link, review=site.review)
    db.add(website)
    db.commit()   # saves changes, we have to do this manually because I specified as such
    db.refresh(website) # refreshes changes after db does changes to it (such as generated IDs)
    return {"id": website.id, "name": website.name, "link": website.link, "review": website.review}
