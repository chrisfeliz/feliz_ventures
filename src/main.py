from typing import Any
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime
import os
import uvicorn
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI(title="Feliz Ventures LLC")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# Add url_for to template environment for dynamic URLs
def url_for(name: str, **path_params):
    """Helper function for generating URLs in templates"""
    if name == "static":
        path = path_params.get("path", "")
        return f"/static/{path}"
    # For other routes, return empty string or handle as needed
    return ""


templates.env.globals["url_for"] = url_for


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main homepage"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Serve the about page"""
    return templates.TemplateResponse("about.html", {"request": request})


@app.get("/sell-your-land", response_class=HTMLResponse)
async def sell_your_land(request: Request):
    """Serve the sell your land page"""
    success = request.query_params.get("success")
    error = request.query_params.get("error")
    return templates.TemplateResponse(
        "sell_land.html", {"request": request, "success": success, "error": error}
    )


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Serve the contact page"""
    return templates.TemplateResponse("contact.html", {"request": request})


@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    """Serve the privacy policy page"""
    return templates.TemplateResponse("privacy.html", {"request": request})

def send_email(contents: dict[str, Any]):
    """Send email with lead data."""
    password = os.getenv("EMAIL_PASSWORD", "")
    sender_email = os.getenv("EMAIL_SENDER", "")
    receiver_email = os.getenv("EMAIL_RECEIVER", "")
    creds_check = False if not all([password, sender_email, receiver_email]) else True
    if not creds_check:
        print("Missing credentials!")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "New Lead Received!"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    text = f"Hi there,\nNew lead received: {json.dumps(contents, indent=4)}!"
    msg.attach(MIMEText(text, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

@app.post("/sell-your-land", response_class=RedirectResponse)
async def collect_form_data(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    street: str = Form(...),
    city: str = Form(...),
    state: str = Form(...),
    zipcode: str = Form(...),
):
    """Collect and process form submission data from sell your land page"""

    # Collect form data
    form_data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": f"{street}, {city}, {state} {zipcode}",
        "submitted_at": datetime.now().isoformat(),
    }

    try:
        send_email(form_data)
        # Redirect back to the form with a success message
        return RedirectResponse(url="/sell-your-land?success=true", status_code=303)

    except Exception as e:
        print(f"Error saving form data: {e}")
        # Redirect back with error message
        return RedirectResponse(url="/sell-your-land?error=true", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
