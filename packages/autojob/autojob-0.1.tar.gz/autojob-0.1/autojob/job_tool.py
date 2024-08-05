from django.core.cache import cache

from autojob.models import JobList
import logging

logger = logging.getLogger(__name__)


def job_before(func):
    def wrapper(*args, **kwargs):
        from autojob.job_new import JobAction
        job_state = JobList.objects.filter(id=int(args[1])).values('job_state')[0]['job_state']
        if job_state == 1:
            job_value = cache.get(args[0])
            if job_value:
                JobAction.modify_job(args[0], job_value)
                cache.delete(args[0])
            if get_lock(args[0]):
                if args[2] == 'date' or (job_value and job_value[0] == 'date'):
                    JobList.objects.filter(id=int(args[1])).update(job_state=0)
                func(*args, **kwargs)
            else:
                JobAction.stop_job(args[0])
        else:
            JobAction.stop_job(args[0])

    return wrapper


def get_lock(lock_name):
    lock = cache.lock('lock.' + lock_name, timeout=5)
    return lock.acquire(blocking=False)


def job_control():
    global logger
    try:
        from autojob.job_new import JobAction
        from autojob import job_new
        from autojob.models import JobList
        import logging

        logger = logging.getLogger(__name__)

        job_list_ = JobList.objects.filter(job_state=1)
        logger.info('Program startup, start scheduled tasks : ' + str(job_list_.__len__()))
        job_new.start_scheduler()
        for job_ in job_list_:
            if hasattr(JobAction, 'start_%s_job' % job_.action_type):
                func = getattr(JobAction(), 'start_%s_job' % job_.action_type)
                func(job_.trigger.trigger_func, job_.job_rate, str(job_.id))
            else:
                logger.error('【start error】 ' + job_.trigger.trigger_func + ' does not exists!')
    except Exception as rel:
        logger.error("scheduler start error:" + str(rel))
