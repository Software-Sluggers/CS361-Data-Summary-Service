from typing import Annotated

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


app = FastAPI(
    title="Data Summary Service",
    version="0.1.0",
)


Count = Annotated[int, Field(ge=0)]


class SummaryRequest(BaseModel):
    """Data supplied by a program requesting a summary."""

    data: dict[str, Count]


class SummaryResponse(BaseModel):
    """Natural-language summary returned by the service."""

    summary: str


@app.exception_handler(RequestValidationError)
async def handle_request_validation_error(
    _request: Request,
    _exception: RequestValidationError,
) -> JSONResponse:
    """Return a readable response for invalid summary requests."""

    return JSONResponse(
        status_code=400,
        content={
            "error": "Invalid request",
            "message": (
                "Provide a JSON body with a 'data' object containing non-negative integer counts."
            ),
        },
    )


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