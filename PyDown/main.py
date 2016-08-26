#!/usr/bin/python3
# coding=utf-8
# jiao.chen@outlook.com
# created on Aug 26, 2016

import os
import down
import conf
import util

def main():
    log_file = os.path.join(os.getcwd(), 'pyDownMaiziCourse.log')
    logging = util.set_logging(log_file, 'a+')
    
    json_file = conf.JsonInfo(conf._CONF_FILE_NAME)
    json_file.update_conf()
    
    downloader = down.DownVideo();
    downloader.set_conf(conf._course_url, conf._course_dir, conf._course_title_pattern, conf._course_index_pattern, conf._course_video_pattern)
    downloader.run();
    return

if __name__ == '__main__':
    main()