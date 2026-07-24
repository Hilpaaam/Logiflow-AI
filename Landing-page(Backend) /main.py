import os
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from starlette.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

app = FastAPI()
security = HTTPBasic()
templates = Jinja2Templates(directory="templates")

# CORS so Next.js frontend can call the API
origins = [
    "http://localhost:3000",
    # add your deployed Next.js domain here later
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic auth password for /admin
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "logiflow123")

# Google Sheets setup
# 1) Create a service account & download JSON key
# 2) Share the target Sheet with the service account email
# 3) Point GOOGLE_APPLICATION_CREDENTIALS to that JSON path
GOOGLE_SHEET_NAME = os.getenv("GOOGLE_SHEET_NAME", "LogiFlow_Audit_Leads")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

creds = None
gc = None
sheet = None

def init_gsheet():
    global creds, gc, sheet
    if sheet is not None:
        return sheet
    cred_path = os.getenv("GOOGLE_CREDENTIALS_JSON", "service_account.json")
    creds = ServiceAccountCredentials.from_json_keyfile_name(cred_path, scope)
    gc = gspread.authorize(creds)
    sheet = gc.open(GOOGLE_SHEET_NAME).sheet1
    # Ensure header row
    if sheet.row_count == 0 or sheet.cell(1, 1).value in (None, ""):
        sheet.append_row([
            "Timestamp", "Name", "Role", "Company", "City",
            "Email", "Phone", "Employees", "Fleet",
            "Biggest Pain", "Goal"
        ])
    return sheet

class Lead(BaseModel):
    name: str
    role: str
    company: str
    city: str | None = None
    email: EmailStr
    phone: str
    employees: str | None = None
    fleet: str | None = None
    biggest_pain: str | None = None
    goal: str | None = None

# In-memory store for quick demo / admin view
leads_memory: List[Lead] = []

def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = credentials.username == ADMIN_USERNAME
    correct_password = credentials.password == ADMIN_PASSWORD
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.post("/api/leads")
async def create_lead(lead: Lead):
    # Append to in-memory list
    leads_memory.append(lead)

    # Append to Google Sheet
    s = init_gsheet()
    s.append_row([
        datetime.utcnow().isoformat(),
        lead.name,
        lead.role,
        lead.company,
        lead.city or "",
        lead.email,
        lead.phone,
        lead.employees or "",
        lead.fleet or "",
        lead.biggest_pain or "",
        lead.goal or "",
    ])

    return {"status": "ok"}

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, user: str = Depends(get_current_admin)):
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "leads": leads_memory, "user": user}
    )
