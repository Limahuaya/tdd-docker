# project/app/api/summaries.py

from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models import pydantic
from app.models.tortoise import SummarySchema

router = APIRouter()


@router.post("/", response_model=pydantic.SummaryResponseSchema, status_code=201)
async def create_summary(
    payload: pydantic.SummaryPayloadSchema,
) -> pydantic.SummaryResponseSchema:
    summary_id = await crud.post(payload)
    response_object = {"id": summary_id, "url": payload.url}
    return response_object


@router.get("/{id}/", response_model=SummarySchema)
async def read_summary(id: int = Path(..., gt=0)) -> SummarySchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary


@router.get("/", response_model=List[SummarySchema])
async def read_summaries():
    summaries = await crud.get_all()
    if not summaries:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summaries


@router.delete("/{id}/", response_model=pydantic.SummaryResponseSchema)
async def delete_summary(id: int = Path(..., gt=0)) -> pydantic.SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    await crud.delete(id)
    return summary


@router.put("/{id}/", response_model=pydantic.SummaryResponseUpdateSchema)
async def update_summary(
    payload: pydantic.SummaryUpdatePayloadSchema,
    id: int = Path(..., title="holaa", gt=0),
) -> pydantic.SummaryResponseSchema:
    summary = await crud.get(id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return await crud.update(id, payload)
