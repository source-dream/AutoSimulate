import logging
from rich.logging import RichHandler

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    # format="%(asctime)s %(levelname)s: %(message)s",
    format="%(message)s",
    # datefmt="[%Y-%m-%d %H:%M:%S]",
    handlers=[RichHandler()]
)
logger = logging.getLogger("log")