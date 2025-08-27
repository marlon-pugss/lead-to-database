from fastapi import FastAPI
from src.leads.lead import router as leads_router
import uvicorn

app = FastAPI(title="Leads API", version="1.0.0")

app.include_router(leads_router, prefix="/api/v1", tags=["leads"])

@app.get("/")
async def root():
    return {"message": "Leads API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)