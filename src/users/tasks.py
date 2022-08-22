from celery.utils.log import get_task_logger

from app.base.celery_decorators import task

logger = get_task_logger(__name__)


@task()
def heart_beat():
    print("Heart Beating Task")
    logger.warning("Heart Beating Task")
