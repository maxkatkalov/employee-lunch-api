import datetime
import logging

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from .models import Poll

logger = logging.getLogger(__name__)


@shared_task
def close_and_open_poll():
    current_date = datetime.datetime.now().date()
    logger.info(
        f"Attempting to find Poll created at "
        f"{current_date - datetime.timedelta(days=50)}"
    )

    try:
        yesterday_poll = Poll.objects.get(
            created_at=current_date - datetime.timedelta(days=1)
        )
    except ObjectDoesNotExist:
        logger.warning("Poll matching query does not exist.")
    else:
        logger.info("Found yesterday's poll. Closing it...")
        yesterday_poll.is_closed = True
        yesterday_poll.save()

    logger.info("Creating a new poll...")
    try:
        Poll.objects.create()
    except IntegrityError:
        logger.warning("Poll matching query already exists.")
    else:
        logger.info("Poll created successfully.")
