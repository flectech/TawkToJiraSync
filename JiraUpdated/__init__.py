import json
import logging
import azure.functions as func
from ..shared import settings
from ..shared.email import *
from ..shared.jira import *

COMMENT_CREATED = "comment_created"
ISSUE_UPDATED = "issue_updated"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('JIRA WebHook request received')

    # Parse the JSON
    data = json.loads(req.get_body())

    # What kind of event was it?
    eid   = data.get("id", None)
    etype = data.get("webhookEvent", None)
    logging.info("JIRA event type %s with ID %s", etype, eid)

    # Grab the JIRA Ticket Reference
    jref = extractJiraTicket(etype, data)

    # What should we send back?
    message = None
    if etype == COMMENT_CREATED:
        message = buildCommentMessage(jref, data)
    elif etype == ISSUE_UPDATED:
        logging.info("JIRA said: %s", json.dumps(data)) # TODO
        message = buildUpdateMessage(jref, data)
    else:
        return func.HttpResponse("Invalid event type '%s'"%etype, 
                                 status_code=400)

    # Grab the TAWK details
    (tawkSID, tawkHID) = getTawkDetails(etype, jref, data)
    if not tawkSID:
        logging.warn("Tawk Ticket Details missing from JIRA data: %s", data)
        return func.HttpResponse("No Tawk.To ticket details found, ignoring")
    logging.info("Matching Tawk.To ticket identified - %s <%s>", tawkHID, tawkSID)

    # Send the update
    recordJIRAUpdate(tawkHID, tawkSID, jref, message)

    return func.HttpResponse("Thank you JIRA! Tawk %s updated" % tawkHID)

def extractJiraTicket(etype, data):
    if etype == COMMENT_CREATED:
        return data["issue"]["key"]
    if etype == ISSUE_UPDATED:
        return data["key"] # Probably
    return None

def buildCommentMessage(jref, data):
    comment = data["comment"]
    author = comment["author"]["displayName"]
    text = extractText(comment["body"])
    return "%s has updated %s in JIRA:\n%s" % (author, jref, text)

def buildUpdateMessage(jref, data):
    # TODO
    return "TODO"

def getTawkDetails(etype, jref, data):
    # If this was a comment, fetch the full issue data
    if etype == COMMENT_CREATED:
        data = fetchTicketFromJIRA(jref)
    
    fields = data.get("fields", None)
    if not fields:
        return (None,None)

    cust_fields = [settings.jiraFieldTawkSystemID(),
                   settings.jiraFieldTawkHumanID()]
    vals = [fields.get("customfield_%s"%f,None) for f in cust_fields]
    return [int(v) if v.isdigit() else v for v in vals]