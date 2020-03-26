import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from TicketCreated.settings import Settings

# Load our settings from Application Settings / Local Settings
settings = Settings()

def generateTawkTicketEmail(ticket):
    (before, after) = settings.tawkTicketsEmail().split("@")
    plainId = ticket["id"].replace('-','')
    email = "%s%s@%s" % (before,plainId,after)
    logging.info("Generated ticket email <%s> for ticket <%d>", email, ticket["humanId"])
    return email

def attachJIRAReference(ticket, jref):
    toaddr = generateTawkTicketEmail(ticket)
    subject = "[#%d] %s" % (ticket["humanId"], ticket["subject"])
    viewurl = os.environ.get("JiraInstance") + "browse/" + jref
    message = """
This ticket has been logged in JIRA as %s.

To view more details or check the latest status, please visit %s""" % (jref, viewurl)
    sendEmail(toaddr, subject, message)

def recordJIRAUpdate(tawkHumanID, tawkSystemID, update):
    # TODO
    return

def sendEmail(toaddress, subject, message):
    logging.info("Sending email to <%s> - %s", toaddress, subject)

    message = Mail(
        from_email=settings.emailFrom(),
        to_emails=toaddress,
        subject=subject,
        plain_text_content=message)
    try:
        sg = SendGridAPIClient(settings.sendgridAPIKey())
        response = sg.send(message)
        logging.info("Email sent via SendGrid: %d - %s", response.status_code, response.body)
    except Exception as e:
        logging.error(e.message)
