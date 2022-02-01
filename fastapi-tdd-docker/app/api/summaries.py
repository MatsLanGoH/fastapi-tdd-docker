"""Endpoints for summaries
/summaries      GET     get all summaries
/summaries/:id  GET     get a single summary
/summaries      POST    add a summary
"""

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.api import crud
from app.models.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from app.models.tortoise import SummarySchema


router = APIRouter()


@router.post(
    "/",
    response_model=SummaryResponseSchema,
    status_code=HTTP_201_CREATED,
)
async def create_summary(payload: SummaryPayloadSchema) -> SummaryResponseSchema:
    summary_id = await crud.post(payload)

    response_object = {
        "id": summary_id,
        "url": payload.url,
    }
    return response_object


@router.get(
    "/{id}",
    response_model=SummarySchema,
)
async def read_summary(id: int) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Summary not found",
        )

    return summary
