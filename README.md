# TawkToJiraSync
Azure Function that will create a ticket in Jira when a ticket is created 
in Tawk.to

This needs to be registered as a Webhook in your Tawk.to configuration, so
that it gets notified when a ticket is created there. It then uses the JIRA
REST API to create a matching ticket in JIRA. Finally, it sends an email
back to Tawk.to, to update the ticket there with details of the JIRA
version.

## Installation
*TODO*

## Configuration
*TODO*

## Based on
https://www.scalyr.com/blog/azure-functions-in-python-a-simple-introduction/
https://developer.tawk.to/webhooks/
