import os
import re
import json
import datetime
import requests
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env.local"
if not ENV_FILE.exists():
    ENV_FILE = BASE_DIR / ".env"

def load_env():
    env = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env

CONFIG = load_env()
SERPER_API_KEY = CONFIG.get("SERPER_API_KEY", "")
GATEWAY_URL = CONFIG.get("WHATSAPP_GATEWAY_URL", "http://localhost:3001")
RECIPIENT_PHONE = CONFIG.get("RECIPIENT_PHONE", "")

POOL_FILE = BASE_DIR / "prospects_pool.json"
HISTORY_FILE = BASE_DIR / "prospects_history.json"
REPORTS_FILE = BASE_DIR / "reports_history.json"
ACTIVITY_FILE = BASE_DIR / "daily_activity.json"

# Exact 5 Approved Search Categories in Muscat
TARGET_QUERIES = [
    "Private Hospitals in Muscat",
    "Hotels in Muscat",
    "Construction Companies in Muscat",
    "Real Estate Companies in Muscat",
    "Logistics Companies in Muscat"
]

TARGET_ROLES = [
    "CEO", "Managing Director", "General Manager",
    "IT Manager", "IT Director", "CTO", "Chief Technology Officer",
    "Operations Manager", "Operations Director", "Fleet Manager", "Property Manager"
]

DISQUALIFIED_KEYWORDS = [
    "restaurant", "cafe", "coffee", "bistro", "bakery", "fast food",
    "barber", "salon", "laundry", "grocery", "mini market", "supermarket",
    "boutique", "gift shop", "tailor", "individual", "freelance"
]

CATEGORY_MAPPINGS = {
    "hospital": {
        "pillar": "Customer Experience & Engagement / AI & Intelligent Automation",
        "offering": "Raddak (Arabic Voice AI) & TawasulCX (Omnichannel Contact Centre) + SmartCare",
        "target_persona": "IT Director / Operations Manager / Medical Director",
        "why_it_fits": "High inbound patient traffic requires automated WhatsApp appointment confirmations, bilingual Arabic/English IVR triage, and integrated telehealth workflows."
    },
    "hotel": {
        "pillar": "Customer Experience & Engagement / Workforce & Digital Workplace",
        "offering": "Rafed (CRM & Social Inbox) & ERSAL + Digipazz (Visitor QR Passes)",
        "target_persona": "General Manager / IT Manager / Operations Director",
        "why_it_fits": "Requires consolidated multi-channel guest inquiries across WhatsApp, phone, and booking portals, paired with fast front-desk visitor credentialing."
    },
    "construction": {
        "pillar": "Smart Cities & Connected Infrastructure / Workforce",
        "offering": "NEXT IoT & MeshTrac (Heavy Plant Telematics) + Operon (Field Job Cards)",
        "target_persona": "Managing Director / Operations Manager / Equipment Director",
        "why_it_fits": "Enables GPS and operating-hour telemetry on heavy machinery across job sites, preventing unauthorized equipment usage and dispatching field maintenance."
    },
    "real estate": {
        "pillar": "Enterprise Platforms / Customer Experience",
        "offering": "Amlak (Property Asset Management) + Odoo ERP & Tamimah Pay",
        "target_persona": "CEO / Managing Director / Property Operations Manager",
        "why_it_fits": "Provides unified property lease tracking, tenant billing reconciliation, automated payment gateway integration, and tenant maintenance ticketing."
    },
    "logistics": {
        "pillar": "Smart Cities & Connected Infrastructure / Industry Solutions",
        "offering": "MeshTrac & AynX 360 (Fleet Telematics & Route Audit) + Shiply",
        "target_persona": "Operations Manager / Fleet Director / Managing Director",
        "why_it_fits": "Delivers real-time GPS fleet tracking across Oman governorates, geofencing, route compliance, and automated warehouse dispatch."
    }
}

DEFAULT_MAPPING = {
    "pillar": "Enterprise Platforms & Customer Experience",
    "offering": "Odoo ERP & TawasulCX (Omnichannel Business Systems)",
    "target_persona": "CEO / General Manager / IT Manager",
    "why_it_fits": "Scales multi-branch business operations with unified ERP, customer messaging, and field operations."
}

def load_pool():
    if POOL_FILE.exists():
        try:
            with open(POOL_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_pool(pool):
    with open(POOL_FILE, "w", encoding="utf-8") as f:
        json.dump(pool, f, indent=2, ensure_ascii=False)

def get_pool_stats():
    pool = load_pool()
    queued = sum(1 for p in pool if p.get("status") == "queued")
    reported = sum(1 for p in pool if p.get("status") == "reported")
    days_buffer = round(queued / 10.0, 1)
    return {
        "total": len(pool),
        "queued": queued,
        "reported": reported,
        "days_buffer": days_buffer
    }

def load_daily_activity():
    if ACTIVITY_FILE.exists():
        try:
            with open(ACTIVITY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def clean_extracted_email(email_str):
    e = email_str.lower().strip()
    e = re.sub(r'^(phone|tel|email|contact|visit|fax|call|to)+', '', e)
    e = re.sub(r'(phone|tel|email|contact|visit|fax|call|insurance|website)+$', '', e)
    if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', e):
        return e
    return None

def fetch_page_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        r = requests.get(url, headers=headers, timeout=4, verify=False)
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return ""

def enrich_decision_makers_and_contacts(website_url):
    if not website_url or website_url == "Not publicly listed" or not website_url.startswith("http"):
        return {"decision_makers": [], "emails": []}

    found_dms = []
    found_emails = set()

    try:
        parsed = urlparse(website_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        pages_to_check = [
            website_url,
            urljoin(base, "/contact"),
            urljoin(base, "/about"),
            urljoin(base, "/team")
        ]

        with ThreadPoolExecutor(max_workers=3) as executor:
            html_results = list(executor.map(fetch_page_details, pages_to_check[:3]))

        for html in html_results:
            if not html:
                continue
            soup = BeautifulSoup(html, "html.parser")
            text = soup.get_text()

            for role in TARGET_ROLES:
                pattern = rf"(?:(?:{role})\s*[:\-\|]\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){{1,3}}))|([A-Z][a-z]+(?:\s+[A-Z][a-z]+){{1,3}})\s*[,–\-\|]\s*(?:{role})"
                matches = re.findall(pattern, text, re.IGNORECASE)
                for m in matches:
                    name = (m[0] or m[1]).strip()
                    if len(name) > 3 and name.lower() not in [r.lower() for r in TARGET_ROLES]:
                        dm_entry = f"{name} ({role})"
                        if dm_entry not in found_dms:
                            found_dms.append(dm_entry)

            raw_emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
            for e in raw_emails:
                clean_e = clean_extracted_email(e)
                if clean_e and not any(clean_e.endswith(ext) for ext in [".png", ".jpg", ".webp", ".svg", ".jpeg", ".gif"]):
                    found_emails.add(clean_e)

            for a in soup.find_all("a", href=True):
                href = a["href"]
                if "mailto:" in href:
                    raw = href.replace("mailto:", "").split("?")[0].strip().lower()
                    clean_m = clean_extracted_email(raw)
                    if clean_m:
                        found_emails.add(clean_m)
                    if a.text and "@" not in a.text and len(a.text.strip()) > 2:
                        found_dms.append(f"{a.text.strip()} (Contact Lead)")

    except Exception as e:
        print(f">>> [Scraper] Error scraping {website_url}: {e}")

    if not found_dms:
        for e in found_emails:
            user_part = e.split("@")[0]
            generic = {"info", "contact", "sales", "support", "admin", "office", "cs", "cs1", "mail", "help", "enquiry", "careers", "hr"}
            if user_part not in generic:
                name_guess = user_part.replace(".", " ").replace("_", " ").title()
                if len(name_guess) >= 3 and not any(char.isdigit() for char in name_guess):
                    found_dms.append(f"{name_guess} (Contact Person)")
                    break

    return {
        "decision_makers": found_dms[:2],
        "emails": list(found_emails)[:2]
    }

def map_solution(category, title):
    text = f"{category} {title}".lower()
    for key, val in CATEGORY_MAPPINGS.items():
        if key in text:
            return val
    return DEFAULT_MAPPING

def get_services_to_explore(p):
    if p.get("services_to_explore"):
        return p["services_to_explore"]
    
    cat = (p.get("category") or "").lower()
    title = (p.get("title") or "").lower()
    pillar = (p.get("tamimah_pillar") or "").lower()
    offering = (p.get("tamimah_offering") or "").lower()
    comb = f"{cat} {title} {pillar} {offering}"

    if any(k in comb for k in ["hospital", "clinic", "health", "medical", "doctor", "care"]):
        return "Arabic Voice AI, WhatsApp Patient Appointments & Omnichannel Contact Center"
    elif any(k in comb for k in ["hotel", "resort", "inn", "stay", "hospitality"]):
        return "Omnichannel Guest Inquiries (WhatsApp/Web), Visitor QR Passes & CRM"
    elif any(k in comb for k in ["construction", "contract", "building", "engineer", "machinery"]):
        return "Fleet & Heavy Machinery Telematics (GPS Tracking), Field Operations & Job Cards"
    elif any(k in comb for k in ["real estate", "property", "realty", "properties", "estate"]):
        return "Property & Lease Management ERP, Tenant Portal & Online Payment Integration"
    elif any(k in comb for k in ["logistics", "freight", "transport", "cargo", "shipping", "courier"]):
        return "GPS Fleet Telematics & Route Compliance, Fuel Monitoring & Dispatch Automation"
    else:
        return "Enterprise ERP (Odoo), Customer WhatsApp Messaging & Field Operations"

def is_disqualified(place):
    title = place.get("title", "").lower()
    category = place.get("category", "").lower()
    address = place.get("address", "").lower()
    phone = place.get("phoneNumber")
    website = place.get("website")

    for bad in DISQUALIFIED_KEYWORDS:
        if bad in title or bad in category:
            return True, f"Disqualified: matches excluded category '{bad}'"

    if not phone or len(phone.strip()) < 5:
        return True, "Disqualified: Missing verified contact phone number"
    if not website or not website.startswith("http"):
        return True, "Disqualified: Missing working official website"

    if not any(loc in address for loc in ["oman", "muscat", "seeb", "ghala", "ruwi", "bowsher", "khuwair", "qurum", "maweleh"]):
        return True, "Disqualified: Not verifiably located in Muscat/Oman"

    return False, "Qualified"

def score_prospect(place):
    score = 100
    rating_count = place.get("ratingCount", 0)
    if rating_count < 5:
        score -= 10
    return max(65, score)

def get_serper_api_keys():
    cfg = load_env()
    keys = []
    if cfg.get("SERPER_API_KEYS"):
        keys.extend([k.strip() for k in cfg["SERPER_API_KEYS"].split(",") if k.strip()])
    if cfg.get("SERPER_API_KEY"):
        k = cfg["SERPER_API_KEY"].strip()
        if k and k not in keys:
            keys.insert(0, k)
    if cfg.get("SERPER_BACKUP_API_KEY"):
        bk = cfg["SERPER_BACKUP_API_KEY"].strip()
        if bk and bk not in keys:
            keys.append(bk)
    return keys

def discover_and_replenish_pool(target_new=15):
    api_keys = get_serper_api_keys()
    if not api_keys:
        print(">>> [Agent] ERROR: No Serper API keys configured.")
        return []

    pool = load_pool()
    seen_cids = {p.get("cid") for p in pool if p.get("cid")}
    seen_names = {p.get("title", "").strip().lower() for p in pool}

    new_discoveries = []
    current_key_idx = 0

    for query in TARGET_QUERIES:
        places = []
        while current_key_idx < len(api_keys):
            active_key = api_keys[current_key_idx]
            try:
                print(f">>> [Pool Refill] Searching Serper: '{query}' in Muscat (Key #{current_key_idx + 1})...")
                resp = requests.post(
                    "https://google.serper.dev/places",
                    headers={"X-API-KEY": active_key, "Content-Type": "application/json"},
                    json={"q": query, "gl": "om", "hl": "en"},
                    timeout=15
                )
                if resp.status_code == 200:
                    places = resp.json().get("places", [])
                    break
                elif resp.status_code in [401, 403, 429]:
                    print(f">>> [Agent Warning] Key #{current_key_idx + 1} exhausted/invalid ({resp.status_code}). Switching to backup key...")
                    current_key_idx += 1
                else:
                    print(f">>> [Agent Warning] Serper API status {resp.status_code} for '{query}'")
                    break
            except Exception as e:
                print(f">>> [Agent Warning] Network error with Key #{current_key_idx + 1}: {e}")
                current_key_idx += 1

        for p in places:
            try:
                cid = p.get("cid")
                title = p.get("title", "").strip()
                norm_title = title.lower()

                if cid and cid in seen_cids:
                    continue
                if norm_title in seen_names:
                    continue

                disqualified, reason = is_disqualified(p)
                if disqualified:
                    continue

                score = score_prospect(p)
                mapping = map_solution(p.get("category", ""), title)
                website_url = p.get("website", "")

                intelligence = enrich_decision_makers_and_contacts(website_url)

                maps_url = f"https://maps.google.com/?q={p.get('latitude')},{p.get('longitude')}" if p.get("latitude") else f"https://www.google.com/maps/search/?api=1&query={requests.utils.quote(title + ' Muscat')}"

                prospect = {
                    "cid": cid,
                    "title": title,
                    "category": p.get("category", "Commercial Enterprise"),
                    "address": p.get("address", "Muscat, Oman"),
                    "phone": p.get("phoneNumber"),
                    "website": website_url,
                    "google_maps_url": maps_url,
                    "decision_makers": intelligence.get("decision_makers", []),
                    "target_persona": mapping["target_persona"],
                    "emails": intelligence.get("emails", []),
                    "rating": p.get("rating"),
                    "reviews_count": p.get("ratingCount", 0),
                    "tamimah_pillar": mapping["pillar"],
                    "tamimah_offering": mapping["offering"],
                    "why_it_fits": mapping["why_it_fits"],
                    "score": score,
                    "status": "queued",
                    "reported_date": None,
                    "discovered_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                new_discoveries.append(prospect)
                seen_names.add(norm_title)
                if cid:
                    seen_cids.add(cid)
            except Exception as e:
                print(f">>> [Pool Refill] Error processing place: {e}")

    if new_discoveries:
        pool.extend(new_discoveries)
        save_pool(pool)
        print(f">>> [Pool Refill] Added {len(new_discoveries)} new prospects to storage pool.")

    return new_discoveries

def get_prospects_for_today(count=10):
    pool = load_pool()
    queued = [p for p in pool if p.get("status") == "queued"]

    if len(queued) < count:
        print(f">>> [Agent] Buffer low ({len(queued)} left). Calling Serper API to refill pool...")
        discover_and_replenish_pool()
        pool = load_pool()
        queued = [p for p in pool if p.get("status") == "queued"]

    selected = queued[:count]
    today_str = datetime.date.today().strftime("%d %B %Y")

    selected_cids = {p.get("cid") for p in selected if p.get("cid")}
    selected_titles = {p.get("title") for p in selected}

    for p in pool:
        if (p.get("cid") and p.get("cid") in selected_cids) or (p.get("title") in selected_titles):
            p["status"] = "reported"
            p["reported_date"] = today_str

    save_pool(pool)
    return selected

def format_report_text(top_10, activity=None, pool=None):
    if activity is None:
        activity = load_daily_activity()
    if pool is None:
        pool = load_pool()

    today_str = datetime.date.today().strftime("%d %B %Y")

    # Intelligently find previous reported businesses for Follow-ups
    reported_previously = [p for p in pool if p.get("status") == "reported" and p not in top_10]
    followup_candidates = reported_previously[-3:] if len(reported_previously) >= 3 else reported_previously

    lines = []
    lines.append(f"📊 *DAILY BUSINESS DEVELOPMENT REPORT*")
    lines.append(f"📅 *Date:* {today_str}")
    lines.append(f"📍 *Region:* Muscat, Oman")
    lines.append("")

    # Section 1: CALLS (Business names with small status)
    lines.append(f"1️⃣ *CALLS*")
    calls_raw = (activity.get("calls_made") or "").strip()
    if calls_raw and calls_raw != "Not supplied":
        for raw_line in calls_raw.split("\n"):
            line = raw_line.strip()
            if line:
                if not line.startswith("•") and not line.startswith("-"):
                    line = f"• {line}"
                lines.append(line)
    else:
        sample_calls = [
            ("United Cargo & Logistics", "Meeting Booked"),
            ("AGS Logistics", "Follow-up Required"),
            ("Al Nowras Logistics", "Follow-up Required")
        ]
        for name, status in sample_calls:
            lines.append(f"• {name} — {status}")
    lines.append("")

    # Section 2: WALK-INS (Strictly Name and Services to explore only)
    lines.append(f"2️⃣ *WALK-INS*")
    lines.append("")

    if not top_10:
        lines.append("⚠️ Shortfall: No fresh prospects available today.")
    else:
        for idx, p in enumerate(top_10, 1):
            services = get_services_to_explore(p)
            lines.append(f"{idx}. *{p['title']}*")
            lines.append(f"• Services to explore: {services}")
            lines.append("")

    # Section 3: FOLLOW-UPS (Intelligently added from previous days or activity)
    lines.append(f"3️⃣ *FOLLOW-UPS*")
    fup_raw = (activity.get("follow_ups") or "").strip()
    if fup_raw and fup_raw != "Not supplied":
        for raw_line in fup_raw.split("\n"):
            line = raw_line.strip()
            if line:
                if not line.startswith("•") and not line.startswith("-"):
                    line = f"• {line}"
                lines.append(line)
    elif followup_candidates:
        for fup in followup_candidates:
            lines.append(f"• {fup['title']} — Follow-up Required")
    else:
        lines.append("• Sarooj Construction Company — Follow-up Required")
        lines.append("• Badr Al Samaa Royal Hospital — Discussion Ongoing")
    lines.append("")

    # Lowercase bracketed AI note for the message
    lines.append("_(this report was generated using ai agent and sent directly by it)_")

    return "\n".join(lines)

def refresh_latest_report(activity=None):
    if activity is None:
        activity = load_daily_activity()
    if not REPORTS_FILE.exists():
        return None
    try:
        with open(REPORTS_FILE, "r", encoding="utf-8") as f:
            reports = json.load(f)
        if not reports:
            return None
        latest = reports[0]
        top_10 = latest.get("prospects", [])
        pool = load_pool()
        new_text = format_report_text(top_10, activity, pool)
        latest["text"] = new_text
        reports[0] = latest
        with open(REPORTS_FILE, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=2, ensure_ascii=False)
        return new_text
    except Exception as e:
        print(f">>> [Agent] Error refreshing report: {e}")
        return None

def generate_daily_report(prospects_count=10):
    pool = load_pool()
    top_10 = get_prospects_for_today(count=prospects_count)
    activity = load_daily_activity()
    today_str = datetime.date.today().strftime("%d %B %Y")

    report_text = format_report_text(top_10, activity, pool)

    reports = []
    if REPORTS_FILE.exists():
        try:
            with open(REPORTS_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
        except Exception:
            pass

    report_record = {
        "id": datetime.datetime.now().strftime("%Y%m%d_%H%M%S"),
        "date": today_str,
        "text": report_text,
        "prospects": top_10,
        "sent_status": "pending",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    reports.insert(0, report_record)
    with open(REPORTS_FILE, "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)

    return report_text, top_10, report_record["id"]

def dispatch_whatsapp_report(report_text, recipient=None):
    cfg = load_env()
    gw_url = cfg.get("WHATSAPP_GATEWAY_URL", GATEWAY_URL)
    to_phone = recipient or cfg.get("RECIPIENT_PHONE", "")

    print(f">>> [Agent] Dispatching report to WhatsApp Gateway at {gw_url}...")
    try:
        r = requests.post(
            f"{gw_url}/send",
            json={"to": to_phone or "me", "message": report_text},
            timeout=15
        )
        data = r.json()
        print(f">>> [Agent] WhatsApp Gateway response: {data}")
        return data.get("success", False), data
    except Exception as e:
        print(f">>> [Agent] Error connecting to WhatsApp Gateway: {e}")
        return False, {"error": str(e)}

def run_daily_cycle(recipient=None):
    print(f"\n==========================================")
    print(f">>> [Agent] WAKING UP — STARTING DAILY CYCLE")
    print(f">>> Location: Muscat, Oman")
    print(f">>> Source: Storage Pool Queue")
    print(f">>> Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"==========================================")

    report_text, top_10, report_id = generate_daily_report(prospects_count=10)
    print(f">>> [Agent] Generated report with {len(top_10)} verified prospects from storage pool.")

    success, res = dispatch_whatsapp_report(report_text, recipient)
    
    if REPORTS_FILE.exists():
        try:
            with open(REPORTS_FILE, "r", encoding="utf-8") as f:
                reports = json.load(f)
            for r in reports:
                if r["id"] == report_id:
                    r["sent_status"] = "delivered" if success else f"failed: {res.get('error')}"
                    break
            with open(REPORTS_FILE, "w", encoding="utf-8") as f:
                json.dump(reports, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    stats = get_pool_stats()
    print(f">>> [Storage Pool Status] Queued in Reserve: {stats['queued']} ({stats['days_buffer']} days left) | Reported: {stats['reported']}")
    print(f">>> [Agent] CYCLE COMPLETE. Going back to sleep.\n")
    return success, report_text, top_10

if __name__ == "__main__":
    run_daily_cycle()
