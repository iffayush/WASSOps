import sys
import json
import subprocess
import os
from datetime import datetime
from supabase import create_client, Client

# Supabase setup
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Debug start
print("\n✅ scanner.py has started")
print("Arguments received:", sys.argv)

if len(sys.argv) != 5:
    raise Exception("Expected 4 arguments: scan_id, user_id, project_id, url")

scan_id, user_id, project_id, url = sys.argv[1:]
output_path = f"scan-{scan_id}.json"

# Run Nuclei with JSON export
cmd = [
    "nuclei",
    "-u", url,
    "-json-export", output_path
]

print("Running command:", " ".join(cmd))

try:
    result = subprocess.run(cmd, timeout=1200, capture_output=True, text=True)
    print("STDOUT:\n", result.stdout)
    print("STDERR:\n", result.stderr)

    if result.returncode != 0:
        raise Exception(f"Nuclei exited with code {result.returncode}")
except subprocess.TimeoutExpired:
    error_msg = "Scan timed out."
    print(error_msg)
    supabase.table("scans").update({
        "status": "error",
        "report": error_msg
    }).eq("id", scan_id).execute()
    sys.exit(1)
except Exception as e:
    error_msg = f"Error running scan: {e}"
    print(error_msg)
    supabase.table("scans").update({
        "status": "error",
        "report": error_msg
    }).eq("id", scan_id).execute()
    sys.exit(1)

# Read and parse the output
if not os.path.exists(output_path):
    raise Exception(f"Output file {output_path} not found")

with open(output_path, "r") as f:
    report_content = f.read()
    print("Raw output:\n", report_content)

# Convert to JSON list
findings = json.loads(report_content) if report_content.strip() else []

# Calculate score
def calculate_score(findings):
    severity_weights = {
        "critical": 30,
        "high": 20,
        "medium": 10,
        "low": 5,
        "info": 1
    }

    total_impact = 0
    for finding in findings:
        severity = finding.get("info", {}).get("severity", "info").lower()
        total_impact += severity_weights.get(severity, 1)

    score = round(max(100 - total_impact, 10.0), 1)
    return score

score = calculate_score(findings)


# Update scan result
supabase.table("scans").update({
    "status": "completed",
    "report": report_content,
    "score": score,
    "created_at": datetime.now().isoformat()
}).eq("id", scan_id).execute()

print(f"✅ Scan completed and stored. Score: {score}")
