#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


def get_logger(name=__name__):
    """获取日志"""
    # logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)
    # filehandler = logging.FileHandler("logger.log")  # Handler用于将日志记录发送至合适的目的地，如文件、终端等
    # filehandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(process)d:%(thread)d - %(name)s - %(levelname)s - %(message)s')
    # filehandler.setFormatter(formatter)

    console = logging.StreamHandler()  # 日志信息显示在终端terminal
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # logger.addHandler(filehandler)
    logger.addHandler(console)
    return logger


if __name__ == '__main__':
    get_logger().info("Start log")
