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
    }
  }
  # TODO Custom fields
  return data

def createTicketInJIRA(ticket):
    url = settings.jiraInstance() + "rest/api/3/issue"
    data = buildNewTicketData(ticket)

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
