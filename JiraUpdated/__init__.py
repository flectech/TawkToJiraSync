import json
import logging
import azure.functions as func
from ..shared import settings

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('JIRA WebHook request received')

    # Parse the JSON
    data = json.loads(req.get_body())

    # TODO Make sense of it
    logging.info("JIRA said: %s", data)

    return func.HttpResponse("Thank you JIRA!")
