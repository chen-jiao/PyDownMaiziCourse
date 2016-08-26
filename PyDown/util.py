#!/usr/bin/python3
# coding=utf-8
# jiao.chen@outlook.com
# created on Aug 26, 2016

import logging

log_format = '%(levelname)-7s - %(filename)-15s[line:%(lineno)3d]: %(message)s'

def set_logging(file_name, file_mode):
    logging.basicConfig(filename = file_name,
                        filemode = file_mode,
                        format = log_format,
                        level = logging.DEBUG)
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(log_format)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    return logging

