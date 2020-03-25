import os
import json
import logging
import requests
import azure.functions as func
from requests.auth import HTTPBasicAuth
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# What Environment / Application settings we require
required_keys = ["JiraInstance"] # TODO Rest

# Process the request
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Tawk.To WebHook request received')

    # TODO Verify the HMAC

    # Parse the JSON
    data = json.loads(req.get_body())

    # Get the ticket details
    ticket = data["ticket"]
    logging.info("%s - %s - %s", ticket["id"], ticket["humanId"], ticket["subject"])
    jref = createTicketInJIRA(ticket)

    if jref:
        sendUpdateEmail(ticket, jref)
        return func.HttpResponse(f"Ticket created in JIRA as %s" % jref)
    else:
        return func.HttpResponse("Error creating JIRA ticket", status_code=500)

def sendUpdateEmail(ticket, jref):
    subject = "[#%d] %s" % (ticket["humanId"], ticket["subject"])
    viewurl = os.environ.get("JiraInstance") + "browse/" + jref
    message = """
This ticket has been logged in JIRA as %s.

To view more details or check the latest status, please visit %s""" % (jref, viewurl)
    sendEmail(subject, message)

def sendEmail(subject, message):
    logging.info("Sending test email - %s", subject)

    message = Mail(
        from_email=os.environ.get("EmailFrom"),
        to_emails=os.environ.get("TawkTo_TicketsEmail"),
        subject=subject,
        plain_text_content=message)
    try:
        sg = SendGridAPIClient(os.environ.get('Sendgrid_API_Key'))
        response = sg.send(message)
        logging.info("%d - %s", response.status_code, response.body)
    except Exception as e:
        logging.error(e.message)

def createTicketInJIRA(ticket):
    data = {
    "fields": {
        "summary": ticket["subject"],
        "issuetype": {
            "id": "10004"
        },
        "project": {
            "key": os.environ.get("JiraProject"),
        },
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                "type": "paragraph",
                "content": [
                    {
                    "text": ticket["message"],
                    "type": "text"
                    }
                ]
                },
                {
                "type": "paragraph",
                "content": [
                    {
                    "text": "Note - for further details, including any possible screenshots, "+
                            "please refer to Ticket %d in Tawk.to" % ticket["humanId"],
                    "type": "text"
                    }
                ]
                }
            ]
        }
    }}

    url = os.environ.get("JiraInstance") + "rest/api/3/issue"

    r = requests.post(url, json=data,
            auth=HTTPBasicAuth(os.environ.get("JiraUsername"),
                                os.environ.get("JiraKey")))

    if (r.status_code < 200 or r.status_code > 299):
        logging.error(r.status_code)
        logging.error(r.json())
        return None

    jref = r.json()["key"]
    logging.info("Ticket created in JIRA for %d as %s", ticket["humanId"], jref)
    return jref