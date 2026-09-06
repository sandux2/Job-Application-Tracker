from fastapi import FastAPI

app = FastAPI()

applications = [
    {"role": "Backend Developer" , "company": "Sage", "location": "Newcastle", "salary":"£30,000", "status": "Ongoing"}, 
    {"role": "Software Engineer" , "company": "Amazon", "location": "London", "salary":"£45,000", "status": "Declined"}
    ]

@app.get("/applications")
async def get_applications():
    return applications