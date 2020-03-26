# Azure Functions load settings from Environment Variables
# On production, these come from "Application Settings"
# When developing locally, these come from local.settings.json
#
# This makes it easy to verify that required ones are defined,
#  then read them

import os

class _Setting(object):
    def __init__(self, addto, envstr, optional=False):
        self.envstr = envstr
        self.optional = optional
        addto.append(self)
    def valid(self):
        if self.optional:
            return True
        return os.environ.get(self.envstr) != None
    def get(self):
        return os.environ.get(self.envstr)

class Settings(object):
    _AS = []
    _JIRA_PROJECT = _Setting(_AS, "JiraProject")

    def jiraProject(self):
        return self._JIRA_PROJECT.get()