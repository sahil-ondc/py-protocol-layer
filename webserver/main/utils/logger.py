import logging
import logging_loki


def handle_logError(record):
    print(record)

def get_logger():


    handler = logging_loki.LokiHandler(
        url="http://34.131.143.119:3100/loki/api/v1/push", 
        tags={"app": "buyer-stage"},
        version='1',

    )
    handler.handleError = handle_logError
    logger = logging.getLogger("loki")
    logger.addHandler(handler)
    logger.log(level=1,msg="hello")
    return logger