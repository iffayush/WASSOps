import subprocess
import json

def run_nuclei_scan(target: str):
    try:
        # Run nuclei with -je (JSON export) and capture output
        result = subprocess.run(
             [
                "nuclei",
                "-u", target,
                "-je",
                "-t", "/nuclei-templates"
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=600
        )
        
        print("NUCLEI STDOUT:", result.stdout)
        print("NUCLEI STDERR:", result.stderr)
       

        # Nuclei with -je outputs JSON lines, so parse each line
        output_lines = result.stdout.strip().splitlines()
        severity_counts = {"critical": 0, "medium": 0, "low": 0}

        for line in output_lines:
            line = line.strip()
            if not line:
                continue

            try:
                # Try parsing JSON line
                finding = json.loads(line)
                severity = finding.get("info", {}).get("severity", "").lower()
                if severity in severity_counts:
                    severity_counts[severity] += 1
                else:
                    # Treat unknown or missing severity as 'low'
                    severity_counts["low"] += 1
            except json.JSONDecodeError:
                # Handle non-JSON lines like: [...][info] ...
                if "[info]" in line.lower():
                    severity_counts["low"] += 1
                else:
                    print("Non-JSON line from nuclei (ignored):", line)

        return severity_counts



    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Nuclei scan failed: {e.stderr}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")
