#!/usr/bin/env python
# -*- coding: utf-8 -*-
import getopt
import os
import sys

from jacoco_increment import JacocoIncrement
from logger import get_logger

DEFAULT_SYS_NAME = "bpc"

logger = get_logger("increment_by_jira")

try:
    SYS_NAME = os.environ['SYS_NAME']
except:
    SYS_NAME = DEFAULT_SYS_NAME
logger.info("系统名称：{}".format(SYS_NAME))

try:
    DAYS_AGO = int(os.environ['DAYS_AGO'])
except:
    DAYS_AGO = 365
logger.info("查询天数：{}".format(DAYS_AGO))
try:
    JIRA_TASK = os.environ['JIRA_TASK']
    if JIRA_TASK.strip() == "":
        logger.error("jira任务号为空")
        raise Exception("jira任务号为空")
except Exception as e:
    logger.error("jira任务号不存在")
    raise Exception("jira任务号不存在")
logger.info("JIRA任务号：{}".format(JIRA_TASK))


def usage():
    print(' * usage:')
    print(' *  -s [val] | --sourcefiles=[val] : java source files path.')
    print(' *  -c [val] | --classfiles=[val] : java class files path.')
    print(' *  -r [val] | --report=[val] : jacoco report output path.')
    print(' *  --projectname=[val] : project name.')
    print(' *  --appname=[val] : app name.')
    print(' *  --envname=[val] : environment name of app.')
    print(' *  --timestr=[val] : Formatting time String.')
    print(' *  -h : help')


if __name__ == '__main__':
    execpath = ''
    sourcefiles = ''
    classfiles = ''
    report = ''
    project_name = ''
    app_name = ''
    env_name = ''
    time_str = ''
    # 对python增加额外参数
    # c: [c+冒号表示-c 后面有参数，h表示-h后面没参数,如果此时在-h 100加上参数，那么这个100的值是获取不到的]
    opts, args = getopt.getopt(sys.argv[1:], 'he:s:c:r:',
                               ['help', "execpath=", 'sourcefiles=', 'classfiles=', 'report=', 'projectname=',
                                'appname=', 'envname=', 'timestr='])
    for op, value in opts:
        # value = value.replace('\'', '').replace('\"', '')
        value = value.strip()
        if op in ('-e', '--execpath'):
            execpath = value
        elif op in ('-s', '--sourcefiles'):
            sourcefiles = value

        elif op in ('-c', '--classfiles'):
            classfiles = value

        elif op in ('-r', '--report'):
            report = value
        elif op in ('--projectname'):
            project_name = value
        elif op in ('--appname'):
            app_name = value
        elif op in ('--envname'):
            env_name = value
        elif op in ('--timestr'):
            time_str = value
        elif op in ('-h', '--help'):
            usage()
            sys.exit()
    if sourcefiles == "":
        print('sourcefiles is null')
        sys.exit()
    if classfiles == "":
        print('classfiles is null')
        sys.exit()
    if report == "":
        print('report is null')
        sys.exit()

    jacoco_increment = JacocoIncrement(SYS_NAME)
    uniquedata = jacoco_increment.get_jira_diff_uniquedata(JIRA_TASK, DAYS_AGO)
    stdout = jacoco_increment.exe_jacoco_report_increment(execpath=execpath, sourcefiles=sourcefiles,
                                                          classfiles=classfiles, report=report, diffcode=uniquedata,
                                                          project_name=project_name, app_name=app_name,
                                                          env_name=env_name, time_str=time_str)
    print(stdout)
    pass
