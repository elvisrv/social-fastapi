from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import models
from database import engine
from routers import post, user, auth, vote
from config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    # "https://www.google.com"
    "*"
]
# fetch('http://localhost:8000/').then(res => res.json()).then(console.log)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Hello": "World"}

# ORM Structure.
# └── sql_app
#     ├── __init__.py
#     ├── crud.py
#     ├── database.py
#     ├── main.py
#     ├── models.py
#     └── schemas.py

# source venv/bin/activate
# uvicorn main:app --reload

# pwd
# /Users/elvisramosvasconcelos/social/app
# ../venv/bin/uvicorn main:app --reload