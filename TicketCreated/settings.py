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
    _JIRA_ISSUE_ID = _Setting("Jira_IssueID")
    _JIRA_FIELD_SID = _Setting("Jira_CustomField)TawkSID", True)
    _JIRA_FIELD_HID = _Setting("Jira_CustomField_TawkHID", True)

    def __init__(self):
        for s in _ALL_SETTINGS:
            if not s.valid():
                raise Exception("Missing required setting '%s' - must be added to Application Settings to run function" % s.envstr)

    def jiraProject(self):
        return self._JIRA_PROJECT.get()