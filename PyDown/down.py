#!/usr/bin/python3
# coding=utf-8
# jiao.chen@outlook.com
# created on Aug 22, 2016

import urllib.request
import requests
import re
import os
import os.path
import logging
import util

class DownVideo:
    def __init__(self):
        self.video_list = []
        self.all_urls = []
        self.course_title = ''        

    def set_conf(self, url, dir = '', title_pattern = '',
                 index_pattern = '', video_pattern = ''):
        self.course_url = url
        self.course_dir = dir
        self.course_title_pattern = title_pattern
        self.course_index_pattern = index_pattern
        self.course_video_pattern = video_pattern

    def create_download_dir(self):
        if not self.course_dir:
            self.course_dir = os.getcwd()
        self.course_dir = os.path.join(self.course_dir, self.course_title)
        if not os.path.exists(self.course_dir):
            os.mkdir(self.course_dir)

    def url_open(self, url):
        req = urllib.request.Request(url)
        req.add_header('User_Agent', 
                       ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0)"
                        " Gecko/20100101 Firefox/23.0"))
        response = urllib.request.urlopen(req)
        data = response.read()
        return data.decode('utf-8')

    def get_course_title(self, data):
        self.course_title = re.findall(self.course_title_pattern,
                                       data, re.S)[0]
        self.course_title = self.course_title.strip()

    def get_all_urls(self, data):
        urls_info = re.findall(self.course_index_pattern, data, re.S)
        for url_info in urls_info:
            self.all_urls.append(list(url_info))

    def get_video_list(self, data):
        self.video_list = re.findall(self.course_video_pattern, data, re.S)

    def download(self, url, file):
        req = urllib.request.Request(url)
        req.add_header('User_Agent', 
                       ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0)"
                        " Gecko/20100101 Firefox/23.0"))
        response = urllib.request.urlopen(req)
        video_size = float(response.getheader('Content-Length'))
        if os.path.exists(file):
            file_size = os.path.getsize(file)
        else:
            file_size = 0

        while file_size < video_size:
            open_mode = 'wb'
            if file_size != 0:
                print('[download] Resuming download at byte %s(K)' 
                      % (file_size/1024))
                req.add_header('Range', 'bytes=%d-' % file_size)
                open_mode = 'ab'
            else:
                resume_len = 0

            response = urllib.request.urlopen(req)
            data = response.read(512*1024)
            with open(file, open_mode) as fp:
                fp.write(data)
                fp.flush()
                fp.close()
            file_size = os.path.getsize(file)

    def run(self):
        data = self.url_open(self.course_url)
        self.get_course_title(data)
        self.get_all_urls(data)
        self.create_download_dir()
        
        logging.debug('course name is %s have %d lessons'
                      % (self.course_title, len(self.all_urls)))
        logging.debug('all lessons will download in %s\n' % self.course_dir)

        for url_index in self.all_urls:
            title = url_index[1]
            url = 'http://www.maiziedu.com' + url_index[0]
            print(title,url)
            self.get_video_list(self.url_open(url))
            logging.debug('begin to download %s to %s'
                              % (title, self.course_dir))
            for video_url in self.video_list:
                video_name = os.path.basename(video_url)
                video_type = os.path.splitext(video_name)[1]
                file_name = os.path.join(self.course_dir,
                                        title + video_type)
                self.download(video_url, file_name)
            logging.debug('%s download complete\n' % title)
        logging.debug('all lessons download complete\n')

def main():
    logging = util.set_logging(file_name=os.path.join(os.getcwd(), 'pyDown_test.log'), 
                               file_mode='w+')

    url = 'http://www.maiziedu.com/course/21/';
    dir = 'H:\麦子学院'
    title_pattern = '<h1 class=".*?">(.*?)</h1>'
    index_pattern = ('<li><a href="(.*?)" target.*?'
                     '<span class="fl">(.*?)</span>')
    video_pattern = '<source src="(.*?)" type=\'video/mp4\' />'
    downloader = DownVideo();
    downloader.set_conf(url, dir, title_pattern, index_pattern, video_pattern)
    downloader.run();

if __name__ == '__main__':
    main();