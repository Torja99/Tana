import wolframalpha
from dotenv import load_dotenv
import os
import custom_logger
load_dotenv()
app_id = os.environ.get("api-token")
client = wolframalpha.Client(app_id)


def wolfram_query(question):
    response = client.query(question)
    try:
        wolfram_res = next(response.results).text
    except Exception as ex:

        custom_logger.log.info("Wolfram Unknown Error")
        return ("Sorry I don't know that")
    return wolfram_res
