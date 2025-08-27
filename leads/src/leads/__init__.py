import sys
import os
import subprocess
from pathlib import Path

if __name__ == "__main__":
    root_path = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(root_path))
    
    # Mata qualquer processo rodando na porta 8000
    try:
        subprocess.run("lsof -ti:8000 | xargs kill -9", shell=True, capture_output=True)
        print("🔄 Porta 8000 liberada")
    except:
        pass
    
    # Inicializa o banco de dados se necessário
    try:
        from src.db import engine, Base
        from src.model import lead  # Importa para registrar os modelos
        Base.metadata.create_all(bind=engine)
        print("🗃️ Banco de dados inicializado")
    except Exception as e:
        print(f"⚠️ Erro ao inicializar banco: {e}")

from fastapi import FastAPI
import uvicorn

if __name__ == "__main__":
    from src.leads.lead import router as leads_router
else:
    from .lead import router as leads_router

app = FastAPI(title="Leads API", version="1.0.0")

app.include_router(leads_router, prefix="/api/v1", tags=["leads"])

@app.get("/")
async def root():
    return {"message": "Leads API is running!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


#{"FirstName":"João","LastName":"Silva","Email":"casa@test.com","Phone":"+5511999999999","LeadSource":"WEBSITE","OptIn__c":true}
#http://localhost:8000/api/v1/leads/f9479ee0-0dbe-4b70-b8e5-8fadb9b4c11e