import requests
import utils
import time
import json
import os
import logging
import sys
import send_email
import execjs
import traceback

logging.getLogger("requests").setLevel(logging.WARNING)

def get_time():
    return str(hex(int(time.time())).replace('0x', ''))

#读取js文件
with open('token.js',encoding='utf-8') as f:
    js = f.read()
#通过compile命令转成一个js对象
tokenjs = execjs.compile(js)

tokenKey = "5ec029c599f7abec29ebf1c50fcc05a0"

options_header = utils.get_headers(
'''
Host: api.busyluo.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type,x-app,x-time,x-token
Referer: https://www.busyluo.org/
Origin: https://www.busyluo.org
Connection: keep-alive
TE: Trailers
'''
)
#print(options_header)
#res = requests.options("https://api.busyluo.org/4.0/main/signin", headers=options_header)

# xtime = str(hex(int(time.time())).replace('0x', ''))

lecture_header ='''
Host: api.busyluo.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: vnd.busyluo.v8+json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
X-App: uni
X-Time: {}
X-Token: {}
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVkYzc2YWU3ODk1NTk5MTUwNGY1ZTg3NyIsImlhdCI6MTU3MzcxMjUzNSwiZXhwIjoxNTc2MzA0NTM1LCJpc3MiOiJ1cm46YXBpIn0.zI8H9EHPbUJJfKauY-jpKDQ-qN6M3ibxKurzP9zmxN0
Origin: https://www.busyluo.org
Connection: keep-alive
Referer: https://www.busyluo.org/courses/5d88845bf7a31c6d26799446/lectures/{}
TE: Trailers
'''

# 获取所有课
x_time = "5dcbc4ae" #get_time()
x_token = tokenjs.call('get_token', x_time)
all_lecture_header = utils.get_headers(lecture_header.format(x_time, x_token, "5d8ae9038bcb3b5f90f7fc4c"))


m3u8_header = '''
Host: media.busyluo.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Origin: https://www.busyluo.org
Connection: keep-alive
Referer: https://www.busyluo.org/courses/5d88845bf7a31c6d26799446/lectures/{}
'''

ts_header = '''
Host: media.busyluo.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Origin: https://www.busyluo.org
Connection: keep-alive
Referer: https://www.busyluo.org/courses/5d88845bf7a31c6d26799446/lectures/{}
'''
# '''
# If-Modified-Since: Fri, 22 Feb 2019 07:14:35 GMT
# If-None-Match: "Fotri1fDJ52n3XLGbW4HEyDkVs-M"
# '''

res = requests.get('https://api.busyluo.org/4.0/content/lectures?courseId=5d88845bf7a31c6d26799446', headers=all_lecture_header)
print('get lecture content size: {}'.format(len(res.content)))
lectures_content = res.content

# fo = open("lectures.json", "rb")
# lectures_content = fo.read()

all_lec_data = json.loads(lectures_content)

save_dir = "E:\\busyluo\\"


skip_sec = 0
if len(sys.argv) > 1:
    skip_sec = int(sys.argv[1])

try:
    for sec in all_lec_data:
        os.chdir(save_dir)
        sec_order = sec['order']
        if sec_order <= skip_sec:
            continue

        sec_name = "第 {} 讲 {}".format(sec_order, sec['name']).strip()
        
        sec_path = os.path.join(save_dir, sec_name)
        if not os.path.exists(sec_path):
            os.mkdir(sec_name)
        else:
            print(sec_name + " 目录已存在！")

        os.chdir(sec_name)

        print('开始下载章节： {}'.format(sec_name))

        for lec in sec['children']:
            os.chdir(save_dir)
            os.chdir(sec_name)

            lec_order = lec['order']
            lec_name = "{}.{} {}".format(sec_order, lec_order, lec['name']).replace('*', 'x').replace('?', '？')
            lec_path = os.path.join(os.getcwd(), lec_name)
            if not os.path.exists(lec_path):
                os.mkdir(lec_path)
            else:
                print("课时：{} 目录已存在！".format(lec_name))
                continue

            os.chdir(lec_name)

            lec_count = len(os.listdir())

            lec_id = lec['_id']
            x_time = get_time()
            x_token = tokenjs.call('get_token', x_time)
            req_header = utils.get_headers(lecture_header.format(x_time, x_token, lec_id))
            res = requests.get('https://api.busyluo.org/4.0/content/lectures/{}'.format(lec_id), headers=req_header)
            #print(res.content)

            lec_data = json.loads(res.content)
            video = lec_data['video']
            hls = video['hls']
            m3u8_pchigh = hls['pcHigh']
            #print(m3u8_pchigh)

            # get ts list
            m3u8_req_header = utils.get_headers(m3u8_header.format(lec_id))
            res = requests.get(m3u8_pchigh, headers=m3u8_req_header)
            #print(res.content)
            ts_list = utils.get_ts_list(str(res.content, encoding='utf8'))
            #print(ts_list)

            if lec_count >= len(ts_list):
                print("{} 已经下载完成！".format(lec_name))
                continue

            print('开始下载课时： {}, 共{}文件'.format(lec_name, len(ts_list)))
            # get ts
            for ts_name in ts_list:
                ts_path = os.path.join(save_dir, sec_name, lec_name, ts_name)
                if os.path.exists(ts_path):
                    fileinfo = os.stat(ts_path)
                    if fileinfo.st_size > 1024: # 1k
                        print("{} 已存在，跳过".format(ts_name))
                        continue
                ts_req_header = utils.get_headers(ts_header.format(lec_id))
                res = requests.get('https://media.busyluo.org/{}'.format(ts_name))
                with open(ts_path,'wb') as f:
                    f.write(res.content)
                print('write to {}'.format(ts_name))
except Exception as e:
    traceback.print_exc()
    print(e)
    exit()
    email = send_email.SendEmail(host='smtp.qq.com', user='busyluo@qq.com', password='xxxxxxxxxxx', port=465, sender='busyluo@qq.com', receive='2488@qq.com')
    email.connect_smtp_server(method='ssl')
    email.construct_email_obj(subject='python 通知')
    email.add_content(content=str(e))
    email.send_email()
    email.close()