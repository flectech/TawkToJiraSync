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

  # TODO Can we pass along additional Tawk.To metadata, such as tags?
  # Do they come through as properties? https://developer.tawk.to/webhooks/#chatstartevent

  # All done!
  return data

def extractText(body):
    # Is it a nice, simple plain text?
    if isinstance(body, str):
        return body
    logging.warn("TODO: Support body: %s", body)
    return "TODO: Parse body"

def fetchTicketFromJIRA(jref):
    logging.info("Fetching ticket from JIRA - %s", jref)

    url = settings.jiraInstance() + "rest/api/3/issue/%s" % jref
    auth = HTTPBasicAuth(settings.jiraUsername(), settings.jiraAPIKey())
    r = requests.get(url, auth=auth)

    if (r.status_code < 200 or r.status_code > 299):
        logging.error("JIRA ticket fetching failed: %d", r.status_code)
        logging.error(r.json())
        return None
    return r.json()

def ticketPresentInJira(ticket):
    pickerUrl = settings.jiraInstance() + "rest/api/3/issue/picker"
    ticketId = ticket["humanId"]
    auth = HTTPBasicAuth(settings.jiraUsername(), settings.jiraAPIKey())
    jql = "description ~ '%d' in Tawk.to'" % ticketId
    query = {
      'query': '',
      'currentJQL': jql

    }
    pickResponse = requests.request(
       "GET",
       pickerUrl,
       params=query,
       auth=auth
    )
    logging.info("pick found: %s", pickResponse.json())
    return bool(pickResponse.json()['sections'][0]['issues'])

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
