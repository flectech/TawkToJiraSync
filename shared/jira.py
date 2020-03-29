import logging
import requests
from requests.auth import HTTPBasicAuth
from . import settings

def buildNewTicketData(ticket):
  # Build the standard "new ticket" request
  data = {
    "fields": {
        "summary": ticket["subject"],
        "issuetype": {
            "id": settings.jiraIssueType(),
        },
        "project": {
            "key": settings.jiraProject(),
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
    }
  }

  # If custom fields are defined, store the Tawk.To ticket IDs in them
  if settings.jiraFieldTawkSystemID():
      cf = "customfield_%s" % settings.jiraFieldTawkSystemID()
      data["fields"][cf] = ticket["id"]
  if settings.jiraFieldTawkHumanID():
      # Human ID from Tawk is an int, force to String
      cf = "customfield_%s" % settings.jiraFieldTawkHumanID()
      data["fields"][cf] = "%d" % ticket["humanId"]

  # All done!
  return data

def createTicketInJIRA(ticket):
    url = settings.jiraInstance() + "rest/api/3/issue"
    data = buildNewTicketData(ticket)
    logging.info("Creating new ticket in JIRA, using %s", data)

    auth = HTTPBasicAuth(settings.jiraUsername(), settings.jiraAPIKey())
    r = requests.post(url, json=data, auth=auth)

    if (r.status_code < 200 or r.status_code > 299):
        logging.error("JIRA ticket creation failed: %d", r.status_code)
        logging.error(r.json())
        return None

    jref = r.json()["key"]
    logging.info("Ticket created in JIRA for %d as %s", ticket["humanId"], jref)
    return jref
