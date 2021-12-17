#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import os

import hjson
import requests
from logger import get_logger

logger = get_logger("jacoco_increment")

config_path = os.path.join(os.path.dirname(__file__), 'resources/config.hjson')


class JacocoIncrement:

    def __init__(self, sys_name):
        self.sys_name = sys_name
        with open(config_path, 'r', encoding="utf-8") as f:
            self.config = hjson.load(f)
        self.code_diff_url = self.config['code_diff']['url']
        self.code_diff_svn_jira_api = self.config['code_diff']['code_diff_svn_jira_api']
        self.code_diff_svn_date_api = self.config['code_diff']['code_diff_svn_date_api']
        self.vcs_type = self.config['sys_info'][self.sys_name]['vcs_type']
        self.vcs_url = self.config['sys_info'][self.sys_name]['vcs_url']
        self.vcs_username = self.config['sys_info'][self.sys_name]['vcs_username']
        self.vcs_password = self.config['sys_info'][self.sys_name]['vcs_password']
        pass

    def get_jira_diff_uniquedata(self, jira_task, days_ago=365) -> str:
        """调用code-diff获取jira任务号对应的差异代码"""
        url = self.code_diff_url + self.code_diff_svn_jira_api
        json_data = {
            "jiraTasks": jira_task,
            "svnUrl": self.vcs_url,
            "dayAgo": str(days_ago),
            "svnUserName": str(self.vcs_username),
            "svnPassWord": str(self.vcs_password),

        }
        logger.info("获取jira差异代码")
        response = requests.get(url, params=json_data)
        res_json = json.loads(response.text)
        if res_json['code'] != 10000:
            logger.error("错误代码： {} ，错误信息：{}".format(res_json['code'], res_json['msg']))
            raise Exception("错误代码： {} ，错误信息：{}".format(res_json['code'], res_json['msg']))
        return json.dumps(res_json['uniqueData']).replace(" ", "")
        pass

    def get_date_diff_uniquedata(self, start_date, end_date) -> str:
        """调用code-diff获取jira任务号对应的差异代码"""
        url = self.code_diff_url + self.code_diff_svn_date_api
        json_data = {
            "startDate": start_date,
            "endDate": end_date,
            "svnUrl": self.vcs_url,
            "svnUserName": str(self.vcs_username),
            "svnPassWord": str(self.vcs_password),

        }
        logger.info("获取日期区间差异代码")
        response = requests.get(url, params=json_data)
        res_json = json.loads(response.text)
        if res_json['code'] != 10000:
            logger.error("错误代码： {} ，错误信息：{}".format(res_json['code'], res_json['msg']))
            raise Exception("错误代码： {} ，错误信息：{}".format(res_json['code'], res_json['msg']))
        if res_json['uniqueData'] == '[]':
            logger.error("不存在差异代码")
            raise Exception("不存在差异代码")

        return json.dumps(res_json['uniqueData']).replace(" ", "")
        pass

    def exe_jacoco_report_increment(self, execpath, sourcefiles, classfiles, report, diffcode, project_name, app_name,
                                    env_name, time_str) -> int:
        """根据修改后的jacoco jar生成增量报告"""
        if time_str.strip() == '':
            # 日期为空时，默认生成当天日期
            time_str = datetime.datetime.now().strftime('%Y-%m-%d')
        jar_path = os.path.join(os.path.dirname(__file__), 'resources/org.jacoco.cli-0.8.7-SNAPSHOT-nodeps.jar')
        command = r'java -jar {jar_path} report {jacocoexec_path} --classfiles {classfiles} --sourcefiles {sourcefiles} --html {html_report_path} --diffCode {diffcode} --projectName {projectName} --appName {appName} --envName {envName} --timeStr {timeStr} --encoding=utf8'.format(
            jar_path=jar_path, jacocoexec_path=execpath, sourcefiles=sourcefiles, classfiles=classfiles,
            html_report_path=report, projectName=project_name, appName=app_name, envName=env_name, timeStr=time_str,
            diffcode=diffcode)

        status = os.system(command)

        if status != 0:
            logger.error("执行命令失败")
            raise Exception("执行命令失败")
        logger.info("执行成功")
        return status
        pass

    pass
