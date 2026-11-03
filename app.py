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

class SendWhatsAppInput(BaseModel):
    report_id: str = None
    text: str = None

@app.get("/", response_class=FileResponse)
async def read_root():
    return FileResponse(str(INDEX_FILE))

@app.get("/api/dashboard")
async def get_dashboard():
    reports = []
    if tamimah_agent.REPORTS_FILE.exists():
        try:
            with open(tamimah_agent.REPORTS_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
        except Exception:
            pass

    latest_report = reports[0] if reports else None
    activity = tamimah_agent.load_daily_activity()

    return {
        "latest_report": latest_report,
        "reports": reports[:30],
        "activity": activity
    }

@app.get("/api/report/{report_id}")
async def get_single_report(report_id: str):
    if tamimah_agent.REPORTS_FILE.exists():
        try:
            with open(tamimah_agent.REPORTS_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
            for r in reports:
                if r.get("id") == report_id:
                    return {"report": r}
        except Exception:
            pass
    return JSONResponse(status_code=404, content={"error": "Report not found"})

@app.get("/api/whatsapp-status")
async def get_wa_status():
    import requests
    try:
        r = requests.get(f"{tamimah_agent.GATEWAY_URL}/status", timeout=3)
        return r.json()
    except Exception:
        return {"status": "offline"}

@app.get("/api/whatsapp-qr", response_class=HTMLResponse)
async def get_wa_qr():
    import requests
    try:
        r = requests.get(f"{tamimah_agent.GATEWAY_URL}/qr", timeout=3)
        return HTMLResponse(content=r.text)
    except Exception:
        return HTMLResponse(content="<p>Gateway Offline</p>")

@app.post("/api/run")
async def trigger_run():
    success, text, top_10 = tamimah_agent.run_daily_cycle()
    status_msg = f"Dispatched {len(top_10)} prospects! WhatsApp message sent." if success else f"Generated {len(top_10)} prospects from pool. (Scan QR code if WhatsApp is not yet linked)."
    return {
        "success": success,
        "message": status_msg,
        "prospects_found": len(top_10)
    }

@app.post("/api/activity")
async def update_activity(data: ActivityInput):
    act_dict = data.model_dump()
    with open(tamimah_agent.ACTIVITY_FILE, "w", encoding="utf-8") as f:
        json.dump(act_dict, f, indent=2, ensure_ascii=False)
    updated_text = tamimah_agent.refresh_latest_report(act_dict)
    return {"success": True, "updated_text": updated_text}

@app.post("/api/send-whatsapp")
async def send_whatsapp_now(data: SendWhatsAppInput = None):
    text_to_send = None
    if data and data.text:
        text_to_send = data.text
    elif data and data.report_id:
        if tamimah_agent.REPORTS_FILE.exists():
            try:
                with open(tamimah_agent.REPORTS_FILE, "r", encoding="utf-8") as f:
                    reports = json.load(f)
                for r in reports:
                    if r.get("id") == data.report_id:
                        text_to_send = r.get("text")
                        break
            except Exception:
                pass

    if not text_to_send:
        if not tamimah_agent.REPORTS_FILE.exists():
            return {"success": False, "error": "No report generated yet."}
        try:
            with open(tamimah_agent.REPORTS_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
                if not reports:
                    return {"success": False, "error": "No report found."}
                text_to_send = reports[0]["text"]
        except Exception as e:
            return {"success": False, "error": str(e)}

    success, res = tamimah_agent.dispatch_whatsapp_report(text_to_send)
    return {"success": success, "result": res}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)
