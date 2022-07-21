from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def heart_beat():
    print("Heart Beating Task")
    logger.warning("Heart Beating Task")
