from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Data Summary Service",
    version="0.1.0"
)


class SummaryRequest(BaseModel):
    """Data supplied by a program requesting a summary."""

    data: dict[str, int]


class SummaryResponse(BaseModel):
    """Natural-language summary returned by the service."""

    summary: str


def build_summary(data: dict[str, int]) -> str:
    """Convert attribute counts into a basic natural-language sentence."""

    entries = [
        f"{count} {attribute}"
        for attribute, count in data.items()
    ]

    if not entries:
        return "No data was provided."

    if len(entries) == 1:
        return f"There are {entries[0]}."

    joined_entries = ", ".join(entries[:-1])
    return f"There are {joined_entries} and {entries[-1]}."


@app.get("/health")
def health_check() -> dict[str, str]:
    """Confirm that the service is running."""
    return {"status": "ok"}


@app.post("/summary", response_model=SummaryResponse)
def create_summary(request: SummaryRequest) -> SummaryResponse:
    """Return a basic sentence describing the supplied counts."""

    return SummaryResponse(
        summary=build_summary(request.data)
    )