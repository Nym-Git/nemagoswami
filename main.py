import os
import smtplib
from email.message import EmailMessage
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Load environment variables from a .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.1.35:6996", "https://nemachandragoswami.netlify.app"],  # Change to frontend domain in production
    allow_credentials=False,
    allow_methods=["POST","GET"],
)

# Get SMTP credentials from environment variables
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    message: str

@app.post("/send_email")
async def send_email(request: EmailRequest):
    if not SMTP_USERNAME or not SMTP_PASSWORD:
        raise HTTPException(status_code=500, detail="SMTP credentials not configured")

    try:
        # Create email message
        msg = EmailMessage()
        msg["From"] = FROM_EMAIL
        msg["To"] = request.to_email
        msg["Subject"] = f"Response to Your Inquiry on 'nemachandragoswami.netlify.app'"
        msg["Cc"] = "nemagoswami00@gmail.com"
        
        email_body = f'''
        <html>
        <body>
            <p>Dear {request.subject},</p>

            <p>I hope this email finds you well.</p>
            <p>Thank you for reaching out to me. I have received your message and appreciate the time you took to connect.</p>
            <p>For your reference, I am including the details of your message below:</p>
            <blockquote><i>{request.message}</i></blockquote>
            <p>We will review your inquiry and get back to you as soon as possible.</p>
            <br>
            <div class="signature" style="font-family: Arial, sans-serif; font-size: 12.6px; line-height: 1.08; border-left: 3.6px solid #0073b1; padding-left: 9px; padding-top: 6.3px; padding-bottom: 6.3px;">
                <div class="name" style="font-size: 15.3px; font-weight: bold; color: #0073b1; padding: 2.7px 0;">Nema Chandra Goswami</div>
                <div class="role" style="font-size: 11.3px; font-weight: bold; color:rgb(98, 106, 106); padding: 2.7px 0;">Software Development Engineer, SDE - I</div>
                <hr class="separator" style="border: 0; height: 0.9px; background-color: #ccc; margin: 6.3px 0; width: 20%;">
                <div class="contact" style="padding: 1.8px 0; color: #0073b1; font-size: 11.7px;">
                    <a href="tel:+919369841533" style="text-decoration: none; color: #0073b1;">+91 9369841533</a> |
                    Andheri East, Mumbai, Maharashtra
                </div>
                <div class="icons" style="margin-top: 0.5%;">
                    <a href="https://www.instagram.com/" style="text-decoration: none;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/a/a5/Instagram_icon.png" alt="Instagram" style="width: 16.2px; height: 16.2px; margin-right: 5.4px;">
                    </a>
                    <a href="https://www.linkedin.com/in/" style="text-decoration: none;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" alt="LinkedIn" style="width: 16.2px; height: 16.2px; margin-right: 5.4px;">
                    </a>
                    <a href="https://nemachandragoswami.netlify.app/" style="text-decoration: none;">
                        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Paris_transit_icons_-_Train_P.svg/640px-Paris_transit_icons_-_Train_P.svg.png" alt="Portfolio" style="width: 16.2px; height: 16.2px;">
                    </a>
                </div>
            </div>
        </body>
        </html>
        '''
        
        msg.set_content(email_body, subtype='html')
        
        # Connect to SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

        return {"success": True, "message": "Email has been sent successfully. Please check your inbox or spam folder for confirmation. We will revert to you soon."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Add a root endpoint for health checks
@app.get("/")
async def root():
    return {"status": "Email service is running"}

if __name__ == "__main__":
    # Get port from environment variable (Render sets this)
    port = int(os.getenv("PORT", 8000))
    
    # Run the application on 0.0.0.0 (all network interfaces)
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)