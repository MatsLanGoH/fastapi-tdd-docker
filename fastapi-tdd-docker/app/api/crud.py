from typing import List, Optional

from app.models.pydantic import SummaryPayloadSchema
from app.models.tortoise import TextSummary


async def post(payload: SummaryPayloadSchema) -> int:
    summary = TextSummary(
        url=payload.url,
        summary="dummy summary",
    )
    await summary.save()
    return summary.id


async def get(id: int) -> Optional[TextSummary]:
    summary = await TextSummary.filter(id=id).first()
    if summary:
        return summary
    return None


async def get_all() -> List[Optional[TextSummary]]:
    summaries = await TextSummary.all()
    return summaries
