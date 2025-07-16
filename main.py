from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scan import run_nuclei_scan

app = FastAPI()

origins = [
    "https://wass-nu.vercel.app"  # Next.js dev server
    # Add your production domain here when deploying
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    target: str

@app.post("/scan")
def scan_endpoint(request: ScanRequest):
    try:
        result = run_nuclei_scan(request.target)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
