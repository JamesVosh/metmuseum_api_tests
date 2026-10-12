import logging
import httpx

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)

handler = logging.FileHandler(f"py_test.log", mode="w", encoding="utf-8")
formatter = logging.Formatter("%(name)s | %(filename)s | %(asctime)s | %(levelname)-7s | %(message)s")

handler.setFormatter(formatter)
logger.addHandler(handler)

def log_request(request: httpx.Request):
    logger.info("REQUEST  | %3s | %3s | %s" ,request.method, "", request.url)

def log_response(response: httpx.Response):
    if response.status_code >=  500:
        logger.error("RESPONSE | %3s | %3s | %s", response.request.method, response.status_code, response.request.url)
    elif response.status_code >= 400:
        logger.warning("RESPONSE | %3s | %3s | %s", response.request.method, response.status_code, response.request.url)
    else:
        logger.info("RESPONSE | %3s | %3s | %s", response.request.method, response.status_code, response.request.url)
