# project/app/api/crud.py


from typing import Union

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


#  @router.post("/", response_model=SummaryResponseSchema, status_code=201)
async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()
    return summary.id


async def get(id: int) -> Union[dict, None]:
    summary = await TextSummary.filter(id=id).first().values()
    if summary:
        return summary
    return None


async def get_all() -> Union[list, None]:
    summaries = await TextSummary.all().values()
    if summaries:
        return summaries
    return None


async def delete(id: int) -> int:
    summary = await TextSummary.filter(id=id).first().delete()
    return summary



async def update(id: int, payload: SummaryPayloadSchema) -> int:
    summary = await TextSummary.filter(id=id).first()
    summary.url = payload.url
    summary.summary = payload.summary
    await summary.save()
    return summary