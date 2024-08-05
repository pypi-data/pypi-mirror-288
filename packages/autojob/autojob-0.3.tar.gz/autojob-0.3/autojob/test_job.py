# coding=utf-8
import datetime
import logging

from autojob.job_tool import job_before

logger = logging.getLogger(__name__)


@job_before
def test_job(*args):
    # This is the task you need to perform
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(now + '__This is a timed task for testing:' + args[0])
