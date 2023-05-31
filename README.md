# TawkToJiraSync
Azure Function that will create a ticket in JIRA when a ticket is created 
in Tawk.to, and attach that JIRA reference to the Tawk.to ticket.

Optionally, it can also update the Tawk.to ticket when the JIRA ticket is
updated or commented on.

It runs as an Azure Function, a serverless environment from Microsoft Azure.
You don't need to write any code, only create accounts and configure things.

However, some experience with Azure / serverless python / JIRA will certainly
help you with setting things up to run on Azure!

## How it works
This needs to be registered as a Webhook in your Tawk.to configuration, so
that it gets notified when a ticket is created there. It then uses the JIRA
REST API to create a matching ticket in JIRA. Finally, it sends an email
back to Tawk.to, to update the ticket there with details of the JIRA
version. 

If you want, it can also be regsitered as a JIRA webhook, and then emails 
Tawk.to to update the ticket there when JIRA is updated.

This should probably work for an on-premise JIRA instance too, but is more
typically for JIRA Cloud use.

The code for this runs on Azure Functions, a serverless code hosting 
environment on Microsoft Azure. You will need to have an Azure account,
though a free 1 year trial ought to be more than enough!

# Getting started
If you are new to deploying Python-based Functions on Azure, you may well
find the tutorials at
https://www.sentinelone.com/blog/azure-functions-in-python-a-simple-introduction/
and
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python
helpful!

Generally, you need Visual Studio Code installed, with the Azure Functions 
add-in installed+enabled, and the Azure Functions SDK installed.

See also
https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python

## Creating Accounts
You will need to create a new email address on your domain, to use for ticket
updates.

Next, create an agent account in Tawk.to for that new email address. This is so
that the webhook has permissions to update the Tickets in Tawk.to and they
come through as a known agent.

Finally, create a user in Jira for the new email address, and assign it
permissions to your support project. This is so that the webhook can create
new tickets in JIRA, and read them.

# Secrets, Keys, Settings etc
Before you can install + configure this function, you need to get a load of
secrets and keys to hand.

### Tawk.To
You need your Tawk.To ticket creation/update email address, so that the
Tawk.To ticket can be updated with the JIRA ticket reference. This is the
same email you send to in order to create new tickets, typically 
something like `tickets@your-tenant.tawk.email`

### JIRA
You need:
 * An API key - see https://id.atlassian.com/manage/api-tokens
 * Your username
 * The short code of project you want to create tickets in
 * Your base URL

If you want to have the webhook update the Tawk.to ticket when updates are
done in JIRA, you also need to create two custom fields for your project,
to store the Tawk.to IDs in. These should be single-line text fields.

### SendGrid
Sending emails directly isn't allowed from Azure Functions. So, you need to
sign up for an account with SendGrid, then create an API key.

When logged into Azure, if you search for Sendgrid, you will be able to
create a free account and be logged into Sendgrid. From there, create and
save the key.

You should also disable the various tracking features, so that the JIRA URL
doesn't get changed when sending back to Tawk.To

## Local Configuration
Copy local.settings.json.example to local.settings.json, then populate 
the values with the secret and values above.

## Remote Configuration
Once you have deployed the code to Azure, go to the Function in Azure, 
go to Configuration, then Application Settings. For each key/value pair
in the local settings file, define an Application Setting. Don't forget to
save once they are all defined!

## Tawk.To Configuration
In Azure, go to Function then the Method for `TicketCreated`, then copy 
the Function URL.

In Tawk, setup a new Webhook for Ticket Creation, and paste in the
Function URL. Make sure to specify the full URL including the code
parameter.

Finally, copy the secret, and populate this in your settings

## JIA Configuration (optional)
In Azure, get the Function URL for `JiraUpdated`. 

In JIRA, setup a new Webhook for Issue Updated and Commented, for your
support project only, with the `JiraUpdated` function URL.

Ensure that you have created the two fields for the Tawk.to IDs, and
configured those.

## Testing / tracing
Once you have deployed your Function from Visual Studio Code, pick the
options to follow the live logs. This will bring up the `Live Metrics`
page for the deployed function.

By watching the logs in the `Sample Telemetry` section of the page, you
can see what is going on, why things are failing or not being processed
etc.

Additionally, you can run the functions locally with `func start`, but
you then need sample JSON files of the webhook requests to feed to
the functions to debug.

## Based on
 * https://developer.tawk.to/webhooks/
 * https://blog.developer.atlassian.com/creating-a-jira-cloud-issue-in-a-single-rest-call/
