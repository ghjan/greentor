#coding:utf8
import logging
import psutil

from django.core.management.base import NoArgsCommand, BaseCommand
from message.utils import send_cron_email


def running(command_name):
        u'''
        判断当前脚本任务是否已经有进程再训营
        command_name - 脚本命令名
        '''
        ps = list(psutil.process_iter())
        count = 0
        for p in ps:
            if p.cmdline() and (command_name in p.cmdline()[0]):
                count += 1
            if count > 1:
                break
        # 进程数（包括本身）大于1的情况下说明已经存在一个进程在运行。
        if count > 1:
            return True
        return False
        

class CronNoArgsCommand(NoArgsCommand):
    
    logger = logging.getLogger('django.cron')
    
    email_body = ''
    success_msg = ''
    
    def handle_noargs(self, **options):
        
        if self.help == '':
            raise ValueError(u'must defined the help for this cron command.')
        
        self.logger.info('runing %s program.' % self.help)
        
        self.handle_cron()
        
        self.send_notify()
        
        self.logger.info("finish %s program." % self.help)
        
        
    def handle_cron(self):
        
        raise NotImplementedError()
    
    
    def send_notify(self):
        if self.email_body:
            send_cron_email.delay('Fuwo Crontab Error: %s' % self.help, self.email_body)
        else:
            send_cron_email.delay('Fuwo Crontab Sccess: %s'% self.help, "finish %s program.<br><br>%s" % (self.help, self.success_msg))
            

class CronArgsCommand(BaseCommand):
    
    logger = logging.getLogger('django.cron')
    
    email_body = ''
    success_msg = ''
    
    def handle(self, *args, **options):
        
        if self.help == '':
            raise ValueError(u'must defined the help for this cron command.')
        
        self.logger.info('runing %s program.' % self.help)
        
        self.handle_cron(*args, **options)
        
        self.send_notify()
        
        self.logger.info("finish %s program." % self.help)
        
    def handle_cron(self):
        
        raise NotImplementedError()
    
    def send_notify(self):
        if self.email_body:
            send_cron_email.delay('Fuwo Crontab Error: %s' % self.help, self.email_body)
        else:
            send_cron_email.delay('Fuwo Crontab Sccess: %s'% self.help, "finish %s program.<br><br>%s" % (self.help, self.success_msg))