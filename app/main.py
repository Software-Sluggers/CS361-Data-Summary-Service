from fastapi import FastAPI


app = FastAPI(
    title="Data Summary Service",
    version="0.1.0"
)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Confirm that the service is running."""
    return {"status": "ok"}