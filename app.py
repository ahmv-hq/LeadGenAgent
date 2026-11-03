import os
import json
import datetime
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import tamimah_agent

app = FastAPI(title="Tamimah Prospecting Intelligence")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
INDEX_FILE = TEMPLATES_DIR / "index.html"

# Daily Background Scheduler for 8:00 AM Oman Time
scheduler = BackgroundScheduler()
scheduler.add_job(
    tamimah_agent.run_daily_cycle,
    trigger="cron",
    hour=8,
    minute=0,
    timezone="Asia/Muscat",
    id="daily_morning_prospecting"
)
scheduler.start()

class ActivityInput(BaseModel):
    calls_made: str
    meetings_demos: str = ""
    follow_ups: str = ""

@app.get("/", response_class=FileResponse)
async def read_root():
    return FileResponse(str(INDEX_FILE))

@app.get("/api/dashboard")
async def get_dashboard():
    latest_report = None
    if tamimah_agent.REPORTS_FILE.exists():
        try:
            with open(tamimah_agent.REPORTS_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
                if reports:
                    latest_report = reports[0]
        except Exception:
            pass

    activity = tamimah_agent.load_daily_activity()
    pool_stats = tamimah_agent.get_pool_stats()

    return {
        "latest_report": latest_report,
        "activity": activity,
        "pool_stats": pool_stats
    }

@app.post("/api/run")
async def trigger_run():
    success, text, top_10 = tamimah_agent.run_daily_cycle()
    status_msg = f"Dispatched {len(top_10)} prospects! WhatsApp message sent." if success else f"Generated {len(top_10)} prospects from pool. (Scan QR code if WhatsApp is not yet linked)."
    return {
        "success": success,
        "message": status_msg,
        "prospects_found": len(top_10)
    }

@app.post("/api/refill-pool")
async def refill_pool():
    new_items = tamimah_agent.discover_and_replenish_pool()
    stats = tamimah_agent.get_pool_stats()
    return {
        "success": True,
        "added": len(new_items),
        "pool_stats": stats
    }

@app.post("/api/activity")
async def update_activity(data: ActivityInput):
    act_dict = data.model_dump()
    with open(tamimah_agent.ACTIVITY_FILE, "w", encoding="utf-8") as f:
        json.dump(act_dict, f, indent=2, ensure_ascii=False)
    updated_text = tamimah_agent.refresh_latest_report(act_dict)
    return {"success": True, "updated_text": updated_text}

@app.post("/api/send-whatsapp")
async def send_whatsapp_now():
    if not tamimah_agent.REPORTS_FILE.exists():
        return {"success": False, "error": "No report generated yet."}
    try:
        with open(tamimah_agent.REPORTS_FILE, "r", encoding="utf-8") as f:
            reports = json.load(f)
            if not reports:
                return {"success": False, "error": "No report found."}
            text = reports[0]["text"]
            success, res = tamimah_agent.dispatch_whatsapp_report(text)
            return {"success": success, "result": res}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
