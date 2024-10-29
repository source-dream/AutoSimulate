import os
from log import logger
if not os.path.exists('config.py'):
    with open('config.py', 'w') as f:
        f.write(
            "# 线程池配置\nDELAY = 1\nMAX_CONCURRENT = 3\n\n# 数据参数配置\nSEARCH_SCOPE = {\n'region': '',\n'delay': '',\n'universe': '',\n'instrumentType': ''\n}\nDATASET_ID = ''\n\n# Alpha配置\nREGULAR = ''\nSETTINGS = {\n'instrumentType': '',\n'region': '',\n'universe': '',\n'delay': None,\n'decay': None,\n'neutralization': '',\n'truncation': None,\n'pasteurization': '',\n'unitHandling': '',\n'nanHandling': '',\n'language': '',\n'visualization': None,\n}\n\n## 其他配置\nBASE_URL = ''\n\n## 验证配置\nUSERNAME = ''\nPASSWORD = ''\n"
    )
    logger.error("已创建配置文件 请配置config.py文件后启动程序")
    exit(1)
from config import *

from login import login
from dataset import get_datafields
from time import sleep
import concurrent.futures
from simulate import simulate
import threading
import queue
import signal
import functools

# 线程池创建
executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT)
result_queue = queue.Queue()  # 用于保存任务结果的队列
terminate_flag = threading.Event()  # 用于控制任务终止的标志

def schedule_with_delay(tasks):
    """
    限制并发数量的任务调度器，任务完成后将结果放入队列。

    args:
        tasks: list, 待调度的任务列表
    """
    semaphore = threading.BoundedSemaphore(MAX_CONCURRENT)

    def limited_task(task):
        with semaphore:
            if not terminate_flag.is_set():
                result = task()
                result_queue.put(result)

    for task in tasks:
        if terminate_flag.is_set():
            break
        executor.submit(limited_task, task)
        sleep(DELAY)

def log_results():
    """
    日志输出线程，从队列中获取并输出任务结果。
    """
    logger.info("日志线程开始监听")
    while True:
        try:
            result = result_queue.get()  # 设置超时时间，避免一直阻塞
            if result is None:  # 当接收到 None 时退出
                logger.info("日志输出线程结束")
                break
            alpha_id, err = result
            if err:
                logger.info(f"Alpha回测失败: {err}")
            else:
                logger.info(f"Alpha回测成功 Alpha ID: {alpha_id}")
        except Exception as e:
            logger.error(f"任务出错: {e}")
        finally:
            result_queue.task_done()

def signal_handler(sig, frame):
    """
    信号处理函数，用于捕获 Ctrl+C 终止信号
    """
    logger.info("正在终止程序(等待进行中的任务结束)...")
    terminate_flag.set()  # 设置终止标志
    executor.shutdown()  # 等待线程池中的任务结束
    result_queue.put(None)  # 通知日志线程退出
    result_queue.join()  # 等待日志线程退出
    logger.info("程序终止")
    exit(0)

# 设置 Ctrl+C 信号处理
signal.signal(signal.SIGINT, signal_handler)

if __name__ == '__main__':
    sess, err = login()
    if err:
        logger.error(err)
        exit(1)
    logger.info(f"登录成功")
    
    # 获取数据字段
    dataset = get_datafields(sess=sess, searchScope=SEARCH_SCOPE, dataset_id=DATASET_ID)
    datafields_list = dataset['id'].values
    logger.info(f"获取数据字段完成")

    # 初始化Alpha列表
    alpha_list = []
    for datafield in datafields_list:
        simulation_data = {
            'type': 'REGULAR',
            'settings': SETTINGS,
            'regular': REGULAR.format(datafield)
        }
        alpha_list.append(simulation_data)
    logger.info(f"初始化Alpha列表完成")

    # 启动日志输出线程
    log_thread = threading.Thread(target=log_results, daemon=True)
    log_thread.start()

    # 发送Alpha进行回测
    logger.info(f"开始Alpha回测 共{len(alpha_list)}个")
    tasks = [functools.partial(simulate, sess, alpha) for alpha in alpha_list]
    
    try:
        schedule_with_delay(tasks)
    except KeyboardInterrupt:
        signal_handler(None, None)

    # 等待队列处理完所有项目
    result_queue.put(None)
    result_queue.join()
    
