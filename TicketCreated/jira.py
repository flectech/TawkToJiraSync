import os
import logging
import requests
from requests.auth import HTTPBasicAuth
from TicketCreated.settings import Settings

# Load our settings from Application Settings / Local Settings
settings = Settings()

def buildNewTicketData(ticket):
  # TODO Custom fields
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
  # TODO Custom fields
  return data

def createTicketInJIRA(ticket):
    url = settings.jiraInstance() + "rest/api/3/issue"
    data = buildNewTicketData(ticket)

    r = requests.post(url, json=data,
            auth=HTTPBasicAuth(settings.jiraUsername, settings.jiraAPIKey()))

    if (r.status_code < 200 or r.status_code > 299):
        logging.error("JIRA ticket creation failed: %d", r.status_code)
        logging.error(r.json())
        return None

    jref = r.json()["key"]
    logging.info("Ticket created in JIRA for %d as %s", ticket["humanId"], jref)
    return jref
