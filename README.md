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
Before you can install + configure this function, you need to get a load of
secrets and keys to hand.

### Tawk.To
You need your Tawk.To ticket creation/update email address, so that the
Tawk.To ticket can be updated with the JIRA ticket reference. This is the
same email you send to in order to create new tickets

### JIRA
You need:
 * An API key - see https://id.atlassian.com/manage/api-tokens
 * Your username
 * The short code of roject you want to create tickets in
 * Your base URL

### SendGrid
Sending emails directly isn't allowed from Azure Functions. So, you need to
sign up for an account with SendGrid (eg via Azure), then create an API
key

## Local Configuration
Copy local.settings.json.example to local.settings.json, then populate 
the values with the secrets above

## Remote Configuration
Once you have deployed the code to Azure, go to the Function in Azure, 
go to Configuration, then Application Settings. For each key/value pair
i the local settings file, define an Application Setting. Don't forget to
save once they are all defined!

## Tawk.To Configuration
In Azure, go to Function then the Method, then copy the Function URL.

In Tawk, setup a new Webhook for Ticket Creation, and paste in the
Function URL. Make sure to specify the full URL including the code
parameter.

## Based on
https://developer.tawk.to/webhooks/
https://blog.developer.atlassian.com/creating-a-jira-cloud-issue-in-a-single-rest-call/
