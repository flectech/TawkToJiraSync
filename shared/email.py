import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from . import settings

def generateTawkTicketEmail(ticketId, humanId=None):
    if (isinstance(ticketId, dict)):
        ticket = ticketId
        ticketId = ticket["id"]
        humanId = ticket["humanId"]

    (before, after) = settings.tawkTicketsEmail().split("@")
    plainId = ticketId.replace('-','')
    email = "%s%s@%s" % (before,plainId,after)
    logging.info("Generated ticket email <%s> for ticket <%d>", email, humanId)
    return email

def generateJiraViewURL(jref):
    return settings.jiraInstance() + "browse/" + jref

def attachJIRAReference(ticket, jref):
    toaddr = generateTawkTicketEmail(ticket)
    viewurl = generateJiraViewURL(jref)
    subject = "[#%d] %s" % (ticket["humanId"], ticket["subject"])

    viewtext = "To view more details or check the latest status, please visit "
    if settings.yourCompany():
        viewtext = "%s internal team reference: " % settings.yourCompany()

    message = "This ticket has been logged in JIRA as %s.\n\n%s %s" % (jref, viewtext, viewurl)
    sendEmail(toaddr, subject, message)

def recordJIRAUpdate(tawkHumanID, tawkSystemID, jref, message):
    toaddr = generateTawkTicketEmail(tawkSystemID, tawkHumanID)
    viewurl = generateJiraViewURL(jref)
    subject = "[#%d] %s" % (tawkHumanID, jref)
    sendEmail(toaddr, subject, message)

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
