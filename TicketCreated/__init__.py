import os
import json
import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Tawk.To WebHook request received')

    # TODO Verify the HMAC

    # Parse the JSON
    data = json.loads(req.get_body())

    # Get the ticket details
    ticket = data["ticket"]
    logging.info("%s - %s - %s", ticket["id"], ticket["humanId"], ticket["subject"])

    sendEmail("Testing", "Sent via Sendgrid")
    return func.HttpResponse(f"Ticket created in JIRA for %s" % ticket["subject"])

def sendEmail(subject, message):
    logging.info("Sending test email - %s", subject)

    message = Mail(
        from_email=os.environ.get("EmailFrom"),
        to_emails='nick.burch@flectch.uk',
        subject=subject,
        plain_text_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('Sendgrid_API_Key'))
        response = sg.send(message)
        logging.info("%d - %s", response.status_code, response.body)
    except Exception as e:
        logging.error(e.message)

def createJIRATicket(todo):
    pass