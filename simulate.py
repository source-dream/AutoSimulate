import requests
from time import sleep
from typing import Optional
from log import logger

def simulate(sess: requests.Session, alpha) -> tuple[Optional[str], Optional[str]]:
    logger.info(f"Start Simulation: {alpha}")
    res = sess.post(
        'https://api.worldquantbrain.com/simulations',
        json=alpha
    )
    url = res.headers.get('Location')
    if not url:
        return None, "Failed to retrieve simulation URL from response headers."
    while True:
        sim_progress_resp = sess.get(url)
        retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
        if retry_after_sec == 0:
            break
        logger.info(f"Alpha is still in progress. Waiting for {retry_after_sec} seconds.")
        sleep(retry_after_sec)
    if sim_progress_resp.json()["status"] == "ERROR":
        return None, sim_progress_resp.json()["error"]
    alpha_id = sim_progress_resp.json()["alpha"]
    return alpha_id, None