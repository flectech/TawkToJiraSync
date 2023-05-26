import json
import logging
import azure.functions as func
from . import settings
from ..shared.jira import createTicketInJIRA
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

    # Create the matching ticket in JIRA
    jref = createTicketInJIRA(ticket)

    # If possible, send an email to Tawk.To with the JIRA detials in
    if jref == "Ticket exists":
        return func.HttpResponse("Ticket already exists")
    elif jref:
        attachJIRAReference(ticket, jref)
        return func.HttpResponse(f"Ticket created in JIRA as %s" % jref)
    else:
        return func.HttpResponse("Error creating JIRA ticket", status_code=500)

def verifyAndLoad(body):
    # TODO Verify the HMAC
    return json.loads(body)
