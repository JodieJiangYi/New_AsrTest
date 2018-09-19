#!/usr/bin/python
# -*- coding: UTF-8 -*-
import urllib2
import time
import urllib
import json
import hashlib
import base64


def recog_audio(filepath):
    f = open(filepath, 'rb')
    file_content = f.read()
    base64_audio = base64.b64encode(file_content)
    body = urllib.urlencode({'audio': base64_audio})

    url = 'http://api.xfyun.cn/v1/service/v1/iat'
    api_key = 'd53e802ac59ee5e96ad5f9f4d5b3ca02'
    param = {"engine_type": "sms16k", "aue": "raw", "language": "en_us"}

    x_appid = '5b1e1fba'
    x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
    x_time = int(int(round(time.time() * 1000)) / 1000)
    x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib2.Request(url, body, x_header)
    result = urllib2.urlopen(req)
    result = result.read()
    final_result = json.loads(result)['data']
    return final_result
