from pydantic import BaseModel
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query

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

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

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
async def get_applications(session: SessionDep):
    return session.exec(select(Application)).all()



@app.post("/applications")
async def create_application(application: Application, session: SessionDep):
    session.add(application)
    session.commit()
    session.refresh(application)
    return application
   

@app.put("/applications/{application_id}")
async def update_app(application_id: int, status_update: StatusUpdate, session: SessionDep):
    application = session.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.status = status_update.status
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

    

@app.delete("/applications/{application_id}")
async def delete_app(application_id: int, session: SessionDep):
    application = session.get(Application, application_id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    session.delete(application)
    session.commit()
    return {"message": "Application deleted successfully"}
    