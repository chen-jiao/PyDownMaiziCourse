#!/usr/bin/python3
# coding=utf-8
# jiao_chen@realsil.com.cn
# created on Nov 21, 2014

import urllib.request
import requests
import re
import os
import os.path

class DownVideo:
    def __init__(self, url):
        self.index_url = url
        self.video_list = []
        self.all_urls = []
        self.all_video_urls = []
        self.course_title = ''
        self.course_title_pattern = '<h1 class=".*?">(.*?)</h1>'
        self.course_link_pattern = ('<li><a href="(.*?)" target.*?'
                                    '<span class="fl">(.*?)</span>')
        self.video_link_pattern = '<source src="(.*?)" type=\'video/mp4\' />'

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
        urls_info = re.findall(self.course_link_pattern, data, re.S)
        for url_info in urls_info:
            self.all_urls.append(list(url_info))

    def get_video_list(self, data):
        self.video_list = re.findall(self.video_link_pattern, data, re.S)

    def download(self, url, file):
        req = urllib.request.Request(url)
        req.add_header('User_Agent', 
                       ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0)"
                        " Gecko/20100101 Firefox/23.0"))
        response = urllib.request.urlopen(req)
        video_size = float(response.getheader('Content-Length'))
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
        data = self.url_open(self.index_url)
        self.get_course_title(data)
        self.get_all_urls(data)
        if not os.path.exists(self.course_title):
            os.mkdir(self.course_title)
        
        for url_index in self.all_urls:
            title = url_index[1]
            url = 'http://www.maiziedu.com' + url_index[0]
            print(title,url)
            self.get_video_list(self.url_open(url))
            for video_url in self.video_list:
                video_name = os.path.basename(video_url)
                video_type = os.path.splitext(video_name)[1]
                file_name = os.path.join(self.course_title,
                                        title + video_type)
                self.download(video_url, file_name)
                

def main():
    url = "http://www.maiziedu.com/course/21/";
    downloader = DownVideo(url);
    downloader.run();

if __name__ == '__main__':
    main();