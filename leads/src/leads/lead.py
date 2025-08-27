from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import src.controller.lead as controller
import logging
from src.exception import CreateLeadException, NotFoundException
from src.io.http.helper import build_lead_out
from src.schema.lead import Lead

router = APIRouter()
logger = logging.getLogger()

@router.post("/leads")
async def create(lead: Lead) -> JSONResponse:
    try:
        lead_out = controller.create(lead)
        if lead_out:
            return JSONResponse(status_code=201, content=lead_out.model_dump())
        else:
            return JSONResponse(status_code=202, content={})
    except CreateLeadException as e:
        logger.error(str(e))
        raise HTTPException(status_code=e.args[0].status_code, detail=e.args[0].detail)
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Error create Lead")


@router.get("/leads/{lead_id}")
async def get(lead_id: str) -> JSONResponse:
    try:
        lead = controller.get(lead_id)
        return JSONResponse(status_code=200, content=build_lead_out(lead).model_dump(mode='json'))

    except NotFoundException as e:
        logger.error(str(e))
        raise HTTPException(status_code=404, detail=e.args[0])
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Error get Lead")