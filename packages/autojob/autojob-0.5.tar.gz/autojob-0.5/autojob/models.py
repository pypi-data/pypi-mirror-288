from django.db import models
from django.utils import timezone


class JobListTrigger(models.Model):
    trigger_name = models.CharField('trigger_name', max_length=25)
    trigger_func = models.CharField('trigger_func', max_length=25)
    func_desc = 'e.p.：from autojob.test_job import test_job'
    func_path = models.CharField('func_path', help_text=func_desc, max_length=255)
    description = models.CharField('description', max_length=50)

    def __str__(self):
        return self.trigger_name

    class Meta:
        verbose_name = '定时任务触发器'
        verbose_name_plural = verbose_name


class JobList(models.Model):
    job_name = models.CharField('job_name', max_length=25)
    trigger = models.ForeignKey(JobListTrigger, on_delete=models.SET_NULL, null=True)
    type_choices = (('date', 'date'), ('cron', 'cron'))
    type_content = '''Parameter corresponding to scheduling type (execution frequency) ：<br/>
        1、date：Execute task at 1am on August 30, 2019<br/>value：2019-8-30 01:00:00 <br/>
        2、cron：Execute tasks at 2:00 am every day(second minute hour day month week year (The parameters must 
        be in this order))<br/>value：0 0 2 * * * *'''
    action_type = models.CharField('scheduling type', choices=type_choices, max_length=25, default='cron')
    gender_choices = ((0, 'stop'), (1, 'start'),)
    job_state = models.IntegerField('job status', choices=gender_choices, default=0)
    job_rate = models.CharField('frequency', help_text=type_content, max_length=50)
    time = models.IntegerField('number of times', default=0)
    help_text_update_time = '''The task status change before the time is updated<br/>
                    start job: The current time must be greater than one minute from the last time it was changed<br/>
                    stop job: No need to wait to restart'''
    update_time = models.DateTimeField('update time', auto_now_add=timezone.now(), help_text=help_text_update_time)

    def __str__(self):
        return self.job_name

    class Meta:
        verbose_name_plural = '定时任务'
