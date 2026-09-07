from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Application(BaseModel):
    role: str
    company: str
    location: str
    salary: str
    status: str

applications = [
    {"role": "Backend Developer" , "company": "Sage", "location": "Newcastle", "salary":"£30,000", "status": "Ongoing"}, 
    {"role": "Software Engineer" , "company": "Amazon", "location": "London", "salary":"£45,000", "status": "Declined"}
    ]

@app.get("/applications")
async def get_applications():
    return applications

@app.post("/applications")
async def create_application(application: Application):
    applications.append(application.dict())
    return application