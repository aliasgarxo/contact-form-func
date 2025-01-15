import logging
import azure.functions as func
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = func.FunctionApp()

@app.route(route="contact-form", methods=["POST"])
@app.function_name(name="ContactFormFunction")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing contact form submission...")

    try:
        # Parse JSON body from the incoming request
        req_body = req.get_json()
        name = req_body.get("name")
        email = req_body.get("email")
        subject = req_body.get("subject")
        message = req_body.get("message")

        # Validate required fields
        if not name or not email or not subject or not message:
            return func.HttpResponse(
                "All fields (name, email, subject, message) are required.",
                status_code=400
            )

        # Prepare email details
        sender_email = os.getenv("SENDER_EMAIL")
        receiver_email = os.getenv("RECEIVER_EMAIL")
        email_body = f"""
        <p><strong>Name:</strong> {name}</p>
        <p><strong>Email:</strong> {email}</p>
        <p><strong>Subject:</strong> {subject}</p>
        <p><strong>Message:</strong></p>
        <p>{message}</p>
        """

        # Send the email
        send_email(sender_email, receiver_email, subject, email_body)

        return func.HttpResponse(
            "Thank you for your message! We will get back to you shortly.",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error processing contact form: {e}")
        return func.HttpResponse(
            "An error occurred while processing your request.",
            status_code=500
        )


def send_email(sender_email, receiver_email, subject, body):
    """Send email using SendGrid."""
    try:
        sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
        email = Mail(
            from_email=sender_email,
            to_emails=receiver_email,
            subject=subject,
            html_content=body,
        )
        sg.send(email)
        logging.info("Email sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        raise
