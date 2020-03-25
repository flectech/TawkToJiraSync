# TawkToJiraSync
Azure Function that will create a ticket in Jira when a ticket is created 
in Tawk.to

This needs to be registered as a Webhook in your Tawk.to configuration, so
that it gets notified when a ticket is created there. It then uses the JIRA
REST API to create a matching ticket in JIRA. Finally, it sends an email
back to Tawk.to, to update the ticket there with details of the JIRA
version.

This should probably work for an on-premise JIRA instance too, but is more
typically for JIRA Cloud use.

## Installation
*TODO*

## Configuration
*TODO*

## JIRA Configuration
You need to get a JIRA API Token, eg from 
https://id.atlassian.com/manage/api-tokens

## Based on
https://www.scalyr.com/blog/azure-functions-in-python-a-simple-introduction/
https://developer.tawk.to/webhooks/
