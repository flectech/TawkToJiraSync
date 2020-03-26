import os
import json
import logging
import azure.functions as func
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from TicketCreated.settings import Settings
from TicketCreated.jira import createTicketInJIRA

# Load our settings from Application Settings / Local Settings
settings = Settings()

# Process the request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Tawk.To WebHook request received')

    # Parse the JSON
    data = verifyAndLoad(req.get_body())

    logging.info("Jira Project is %s", settings.jiraProject())
    return func.HttpResponse("TODO", status_code=500)

    # Get the ticket details
    ticket = data["ticket"]
    logging.info("%s - %s - %s", ticket["id"], ticket["humanId"], ticket["subject"])
    jref = createTicketInJIRA(ticket)

    if jref:
        sendUpdateEmail(ticket, jref)
        return func.HttpResponse(f"Ticket created in JIRA as %s" % jref)
    else:
        return func.HttpResponse("Error creating JIRA ticket", status_code=500)

def verifyAndLoad(body):
    # TODO Verify the HMAC
    return json.loads(body)

def generateTicketEmail(ticket):
    (before, after) = os.environ.get("TawkTo_TicketsEmail").split("@")
    plainId = ticket["id"].replace('-','')
    email = "%s%s@%s" % (before,plainId,after)
    logging.info("Generated ticket email <%s> for ticket <%d>", email, ticket["humanId"])
    return email

def sendUpdateEmail(ticket, jref):
    toaddr = generateTicketEmail(ticket)
    subject = "[#%d] %s" % (ticket["humanId"], ticket["subject"])
    viewurl = os.environ.get("JiraInstance") + "browse/" + jref
    message = """
This ticket has been logged in JIRA as %s.

To view more details or check the latest status, please visit %s""" % (jref, viewurl)
    sendEmail(toaddr, subject, message)

def sendEmail(toaddress, subject, message):
    logging.info("Sending test email - %s", subject)

    message = Mail(
        from_email=os.environ.get("EmailFrom"),
        to_emails=toaddress,
        subject=subject,
        plain_text_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('Sendgrid_API_Key'))
        response = sg.send(message)
        logging.info("%d - %s", response.status_code, response.body)
    except Exception as e:
        logging.error(e.message)