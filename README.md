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

## Getting started
If you are new to deploying Python-based Functions on Azure, you may well
find the tutorial at
https://www.scalyr.com/blog/azure-functions-in-python-a-simple-introduction/
helpful!

Generally, you need Visual Studio Code installed, with the Azure Functions 
add-in installed+enabled, and the Azure Functions SDK installed.

See also
https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python

## Secrets, Keys etc

## Installation
*TODO*

## Configuration
*TODO*

## JIRA Configuration
You need to get a JIRA API Token, eg from 
https://id.atlassian.com/manage/api-tokens

## Based on
https://developer.tawk.to/webhooks/
https://blog.developer.atlassian.com/creating-a-jira-cloud-issue-in-a-single-rest-call/
