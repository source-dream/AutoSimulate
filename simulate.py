import requests
from time import sleep
from typing import Optional
from log import logger
from db import add_record_memory

def simulate(sess: requests.Session, alpha) -> tuple[Optional[str], Optional[str]]:
    try:
        # 开始模拟
        logger.info(f"Start Simulation: {alpha}")
        res = sess.post(
            'https://api.worldquantbrain.com/simulations',
            json=alpha
        )
        url = res.headers.get('Location')
        if not url:
            return None, "Failed to retrieve simulation URL from response headers."
        
        # 等待模拟结果
        while True:
            sim_progress_resp = sess.get(url)
            retry_after_sec = float(sim_progress_resp.headers.get("Retry-After", 0))
            if retry_after_sec == 0:
                break
            logger.info(f"Alpha is still in progress. Waiting for {retry_after_sec} seconds.")
            sleep(retry_after_sec)
        
        # 获取模拟结果
        data = sim_progress_resp.json()
        if data["status"] == "ERROR":
            return None, data["message"]
        alpha_id = data["alpha"]
        simulate_id = data["id"]
        # 保存模拟结果
        add_record_memory(alpha, alpha_id, simulate_id)
        return alpha_id, None
    except Exception as e:
        return None, str(e)