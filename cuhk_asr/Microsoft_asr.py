#!usr/bin/python
# -*-coding:utf-8 -*-

import wave
import urllib, urllib2, pycurl
import base64
import json
import StringIO
import certifi


## post audio to server
def use_cloud(filepath, language_get):
    language = 'zh-CN'
    fp = wave.open(filepath, 'rb')  # 录音文件名
    ##已经录好音的语音片段
    nf = fp.getnframes()
    f_len = nf * 2
    audio_data = fp.readframes(nf)

    #    cuid = "1C-4D-70-06-C9-BC" #你的产品id
    print("Starting Microsoft ASR")
    if language_get == 'Mandarian':
        language = 'zh-CN'
    elif language_get == 'Cantonese':
        language = 'zh-HK'
    elif language_get == 'English':
        language = 'en-US'
    srv_url = 'https://speech.platform.bing.com/speech/recognition/dictation/cognitiveservices/v1?language=' + language +'&format=detailed'
    http_header = [
        'Accept: application/json;text/xml',
        'Content-Type: audio/wav; codec=audio/pcm; samplerate=16000',
        'Ocp-Apim-Subscription-Key:  eadd1bcd40324a60b8b34fc20a27a989',
        'Host: speech.platform.bing.com',
        'Transfer-Encoding: chunked',
        'Expect: 100-continue',
    ]

    buf = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(pycurl.URL, str(srv_url))  # curl doesn't support unicode
    c.setopt(c.HTTPHEADER, http_header)  # must be list, not dict
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)
    c.setopt(c.TIMEOUT, 30)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.POSTFIELDS, audio_data)
    c.setopt(c.POSTFIELDSIZE, f_len)
    c.perform()
    string = buf.getvalue()
    string1 = json.loads(string)['NBest']
    string2 = string1[0]
    string3 = json.dumps(string2)
    result = json.loads(string3)["Display"]
    buf.close()
    return result