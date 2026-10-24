from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class CaseRecord(BaseModel):
    case_id: str
    title: str
    status: str
    summary: str


SAMPLE_CASES = [
    CaseRecord(
        case_id="CASE-1001",
        title="Synthetic invoice review",
        status="open",
        summary=(
            "A fabricated example where two sample invoices have different "
            "purchase-order references. A reviewer should verify the source records."
        ),
    ),
    CaseRecord(
        case_id="CASE-1002",
        title="Synthetic access-log review",
        status="closed",
        summary=(
            "A fabricated example documenting a routine access review and its "
            "recorded resolution."
        ),
    ),
]

app = FastAPI(
    title="Enterprise AI Investigation & Knowledge Assistant",
    version="0.1.0",
    description="Local learning API using fabricated sample records only.",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/cases", response_model=list[CaseRecord])
def list_cases() -> list[CaseRecord]:
    return SAMPLE_CASES


@app.get("/cases/{case_id}", response_model=CaseRecord)
def get_case(case_id: str) -> CaseRecord:
    for case in SAMPLE_CASES:
        if case.case_id == case_id:
            return case
    raise HTTPException(status_code=404, detail="Case not found")
