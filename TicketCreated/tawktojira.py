import json
import logging
import azure.functions as func
from . import settings
from ..shared.jira import createTicketInJIRA, ticketPresentInJira
from ..shared.email import attachJIRAReference, recordJIRAUpdate

# Process the request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Tawk.To WebHook request received')

    # Parse the JSON
    data = verifyAndLoad(req.get_body())

    # Get the ticket details
    ticket = data["ticket"]
    logging.info("Tawk.To new ticket: %s - %s - %s", ticket["id"], ticket["humanId"], ticket["subject"])

    # TODO Check to see if JIRA already knows about this ticket
    # Every so often, Tawk.To will ping us multiple times for the same ticket

    # Check for existing ticket in JIRA
    ticketExists = ticketPresentInJira(ticket)
    # Create the matching ticket in JIRA, if it doesn't aleready exist
    if ticketExists == False:
        jref = createTicketInJIRA(ticket)

    # If possible, send an email to Tawk.To with the JIRA detials in
    if ticketExists:
        return func.HttpResponse("Ticket already exists")
    elif jref:
        attachJIRAReference(ticket, jref)
        return func.HttpResponse(f"Ticket created in JIRA as %s" % jref)
    else:
        return func.HttpResponse("Error creating JIRA ticket", status_code=500)

def verifyAndLoad(body):
    # TODO Verify the HMAC
    return json.loads(body)
