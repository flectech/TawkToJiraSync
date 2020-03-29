# Azure Functions load settings from Environment Variables
# On production, these come from "Application Settings"
# When developing locally, these come from local.settings.json
#
# This makes it easy to verify that required ones are defined,
#  then read them

import os

_ALL_SETTINGS = []

class _Setting(object):
    def __init__(self, envstr, optional=False):
        self.envstr = envstr
        self.optional = optional
        _ALL_SETTINGS.append(self)
    def valid(self):
        if self.optional:
            return True
        val = os.environ.get(self.envstr)
        return val != None and repr(val) != ""
    def get(self):
        return os.environ.get(self.envstr)

class Settings(object):
    _JIRA_PROJECT  = _Setting("Jira_Project")
    _JIRA_INSTANCE = _Setting("Jira_Instance")
    _JIRA_ISSUE_TYPE = _Setting("Jira_IssueType")
    _JIRA_FIELD_SID  = _Setting("Jira_CustomField_TawkSID", True)
    _JIRA_FIELD_HID  = _Setting("Jira_CustomField_TawkHID", True)
    _JIRA_USERNAME = _Setting("Jira_Username")
    _JIRA_APIKEY   = _Setting("Jira_APIKey")
    _TAWKTO_EMAIL  = _Setting("TawkTo_TicketsEmail")
    _TAWKTO_SECRET = _Setting("TawkTo_Secret")
    _SENDGRID_APIKEY = _Setting("Sendgrid_APIKey")
    _EMAIL_FROM = _Setting("EmailFrom")

    def __init__(self):
        for s in _ALL_SETTINGS:
            if not s.valid():
                raise Exception("Missing required setting '%s' - must be added to Application Settings to run function" % s.envstr)

    def jiraProject(self):
        """
        What is the Project Key of the Project to work with?
        """
        return self._JIRA_PROJECT.get()
    def jiraInstance(self):
        """
        What is the URL of the JIRA Instance to talk to?
        """
        return self._JIRA_INSTANCE.get()
    def jiraIssueType(self):
        return self._JIRA_ISSUE_TYPE.get()
    def jiraFieldTawkSystemID(self):
        return self._JIRA_FIELD_SID.get()
    def jiraFieldTawkHumanID(self):
        return self._JIRA_FIELD_HID.get()
    def jiraUsername(self):
        return self._JIRA_USERNAME.get()
    def jiraAPIKey(self):
        return self._JIRA_APIKEY.get()
    def tawkTicketsEmail(self):
        return self._TAWKTO_EMAIL.get()
    def tawkSecret(self):
        return self._TAWKTO_SECRET.get()
    def sendgridAPIKey(self):
        return self._SENDGRID_APIKEY.get()
    def emailFrom(self):
        return self._EMAIL_FROM.get()