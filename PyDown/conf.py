#!/usr/bin/python3
# coding=utf-8
# jiao.chen@outlook.com
# created on Aug 26, 2016

import json
import os.path
import logging
import util

# Global Constants
_CONF_FILE_NAME = 'DownConf.Json'
_URL = 'course url'
_DIR = 'course dir'
_TITLE_PATTERN = 'course title pattern'
_INDEX_PATTERN = 'course index pattern'
_VIDEO_PATTERN = 'course video pattern'


# Global Variables
_course_url = ''
_course_dir = ''
_course_title_pattern = '<h1 class=".*?">(.*?)</h1>'
_course_index_pattern = ('<li><a href="(.*?)" target.*?'
                         '<span class="fl">(.*?)</span>')
_course_video_pattern = '<source src="(.*?)" type=\'video/mp4\' />'


class JsonInfo:
    def __init__(self, file_path):
        self.file_path = file_path
        self.json_obj = []

    def set_json(self, json_obj, json_str):
        self.json_obj = json_obj

    def inquiry_json_value(self, key):
        if not key:
            return None
        if None == self.json_obj:
            return None
        for item in self.json_obj:
            return item[key]

    def retrieve_json_info(self):
        json_str = ''
        json_obj = []
        try:
            if os.path.isfile(self.file_path):
                file_obj = open(self.file_path,'rb')
                json_str = file_obj.read()
                json_str = json_str.decode('utf-8')
                if 0 != len(json_str):
                    json_obj = json.loads(json_str)
                file_obj.close()
                self.set_json(json_obj, json_str)
        except:
            logging.error("retrieve local json file(%s) fail" %self.file_path)
        return

    def update_conf(self):
        global _course_url
        global _course_dir
        global _course_title_pattern
        global _course_index_pattern
        global _course_video_pattern

        self.retrieve_json_info()
        _course_url = self.inquiry_json_value(_URL)
        _course_dir = self.inquiry_json_value(_DIR)
        logging.debug('Course Url is %s' % _course_url)
        logging.debug('Course Dir is %s' % _course_dir)

        pattern = self.inquiry_json_value(_TITLE_PATTERN)
        if pattern:
            _course_title_pattern = pattern
        logging.debug('Course Title Pattern is %s' % _course_title_pattern)

        pattern = self.inquiry_json_value(_INDEX_PATTERN)
        if pattern:
            _course_index_pattern = pattern
        logging.debug('Course Index Pattern is %s' % _course_index_pattern)

        pattern = self.inquiry_json_value(_VIDEO_PATTERN)
        if pattern:
            _course_video_pattern = pattern
        logging.debug('Course Video Pattern is %s' % _course_video_pattern)

        return

def main():
    logging = util.set_logging(file_name=os.path.join(os.getcwd(), 'conf_test.log'), 
                               file_mode='w+')
    json_file = JsonInfo(_CONF_FILE_NAME)
    json_file.update_conf()

if __name__ == '__main__':
    main();