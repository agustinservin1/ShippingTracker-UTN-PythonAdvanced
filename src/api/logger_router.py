from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/")
def get_logs():
    log_file = Path("logs/shipping_logs.txt")
    
    if not log_file.exists():
        raise HTTPException(status_code=404, detail="Log file not found")
    
    structured_logs = []
    
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
           
                parts = line.strip().split(" | ")
                timestamp = parts[0][1:-1] 
                client = parts[1].split(": ")[1]
                level = parts[2].split(": ")[1]
                service = parts[3].split(": ")[1]
                message = parts[4].split(": ")[1]
                
                extra = {}
                if "Extra: " in line:
                    extra_part = line.split("Extra: ")[1].strip()
                    extra = json.loads(extra_part)
                
                structured_logs.append({
                    "timestamp": timestamp,
                    "client": client,
                    "level": level,
                    "service": service,
                    "message": message,
                    "extra": extra
                })
                
            except Exception as e:
                structured_logs.append({"raw_log": line.strip()})
    
    return {"logs": structured_logs}