from fastapi import APIRouter, HTTPException
import os
import re
from datetime import datetime

# Initialization and Logs File Directory Finding
router = APIRouter()
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LOG_FILE = os.path.join(BASE_DIR, "logs", "monitoring.txt")

# Write Log Request
def log_request(request_id: str, tokens: int, response_time: float, status: str):
    log_entry = f"{datetime.utcnow()} | request_id: {request_id} | tokens: {tokens} | time: {response_time:.2f}s | status: {status}\n"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as file:
        file.write(log_entry)

# Get Statistics
def analyze_logs():
    total_requests = 0
    success_count = 0
    failure_count = 0
    total_response_time = 0.0
    token_usage = 0

    try:
        with open(LOG_FILE, "r") as file:
            for line in file:
                total_requests += 1
                match = re.search(r"time: ([\d.]+)s \| status: (\w+)", line)
                if match:
                    response_time = float(match.group(1))
                    status = match.group(2)

                    total_response_time += response_time
                    if status.lower() == "success":
                        success_count += 1
                        token_usage += 1
                    else:
                        failure_count += 1

        avg_response_time = total_response_time / total_requests if total_requests else 0
        success_rate = (success_count / total_requests) * 100 if total_requests else 0
        failure_rate = (failure_count / total_requests) * 100 if total_requests else 0

        return {
            "total_requests": total_requests,
            "success_rate": success_rate,
            "failure_rate": failure_rate,
            "avg_response_time": avg_response_time,
            "total_token_usage": token_usage
        }
    except FileNotFoundError:
        return {"error": "Log file not found."}

# API Logs Call
@router.get("/")
async def analyze_logs_endpoint():
    import os
    print("Expected log file path:", os.path.abspath(LOG_FILE))
    result = analyze_logs()
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
