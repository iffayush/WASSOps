from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, UUID4
from uuid import uuid4
import subprocess
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

app = FastAPI()
origins = [
    "https://wass-ebon.vercel.app"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or use ["*"] for development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Request schema
class ScanRequest(BaseModel):
    url: str
    user_id: UUID4
    project_id: UUID4

@app.post("/api/scan")
async def start_scan(data: ScanRequest):
    # Generate scan_id
    scan_id = str(uuid4())

    # Create 'queued' scan record in Supabase
    response = supabase.table("scans").insert({
        "id": str(scan_id),
        "user_id": str(data.user_id),
        "project_id": str(data.project_id),
        "status": "queued",
        "url": data.url  
    }).execute()


    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to queue scan.")

    # Launch scanner.py as background subprocess
    print("Launching scanner.py...", flush=True)
    try:
        subprocess.Popen(
        ["python3", "scanner.py", scan_id, str(data.user_id), str(data.project_id), str(data.url)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start scan: {e}")

    return { "status": "queued", "scan_id": scan_id }

# 📥 Get scan result/status
@app.get("/api/scan/{scan_id}")
async def get_scan_result(scan_id: UUID4 = Path(...)):
    response = supabase.table("scans").select("*").eq("id", str(scan_id)).single().execute()

    if not response.data:
        raise HTTPException(status_code=404, detail="Scan not found")

    return response.data