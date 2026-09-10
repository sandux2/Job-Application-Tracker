from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select

app = FastAPI()

class Application(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: str
    company: str
    location: str
    salary: str
    status: str

class StatusUpdate (BaseModel):
    status : str


sqlite_file_name = "applications.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


applications = [
    {"id": 1, "role": "Backend Developer" , "company": "Sage", "location": "Newcastle", "salary":"£30,000", "status": "Ongoing"}, 
    {"id": 2, "role": "Software Engineer" , "company": "Amazon", "location": "London", "salary":"£45,000", "status": "Declined"}
    ]

@app.get("/applications")
async def get_applications():
    return applications



@app.post("/applications")
async def create_application(application: Application):
    ids = []
    for app in applications:
        ids.append(app["id"])
    new_id = max(ids) + 1
    save_id = application.dict()
    save_id["id"] = new_id
    applications.append(save_id)
    return save_id

@app.put("/applications/{application_id}")
async def update_app(application_id: int, status_update: StatusUpdate):
    for n in applications:
        if n["id"] == application_id:
            n["status"] = status_update.status
            return n

@app.delete("/applications/{application_id}")
async def delete_app(application_id: int):
    for n in applications:
        if n["id"] == application_id:
            applications.remove(n)
            return {"message": "Application deleted successfully"}
    return {"message": "Application not found"}
