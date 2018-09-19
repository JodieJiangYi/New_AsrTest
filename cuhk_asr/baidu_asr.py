#!usr/bin/python
# -*-coding:utf-8 -*-

import wave
import urllib, urllib2, pycurl
import base64
import json, StringIO
import ssl, sys


## get access token by api key &amp; secret key
## 获得token，需要填写你的apikey以及secretkey
def get_token():
    apiKey = "qZ0BGQMYX2H78ozyDFbex7Iv"
    secretKey = "TTnfAYOSgIQIvZDv3snSCsgwgYYCzLj1"
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    auth_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=qZ0BGQMYX2H78ozyDFbex7Iv&client_secret=TTnfAYOSgIQIvZDv3snSCsgwgYYCzLj1 '
    res = urllib2.urlopen(auth_url)
    json_data = res.read()
    return json.loads(json_data)['access_token']


## post audio to server
def use_cloud(filepath, token, language):
    fp = wave.open(filepath, 'rb')  # 录音文件名
    ##已经录好音的语音片段
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)
    dev_pid = '1537'

    if language == 'Mandarian':
        dev_pid = '1537'
    elif language == 'Cantonese':
        dev_pid = '1637'
    elif language == 'English':
        dev_pid = '1737'

    #    cuid = "1C-4D-70-06-C9-BC" #你的产品id
    print("Starting Baidu ASR")
    srv_url = 'http://vop.baidu.com/server_api?dev_pid=' + dev_pid + '&lan=ct&cuid=1C-4D-70-06-C9-BC&token=' + token
    http_header = [
        'Content-Type: audio/pcm; rate=16000',
        'Content-Length: %d' % f_len
    ]
    buf = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, str(srv_url))  # curl doesn't support unicode
    c.setopt(c.HTTPHEADER, http_header)  # must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform()
    string1 = buf.getvalue()
    prestring = json.loads(string1)['result']
    result = prestring[0]
    buf.close()
    return result
