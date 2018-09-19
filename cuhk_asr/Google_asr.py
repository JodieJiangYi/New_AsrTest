#!usr/bin/python
# -*-coding:utf-8 -*-

import wave
import urllib, urllib2, pycurl
import base64
import json
import StringIO
import certifi


## post audio to server
def use_cloud(filepath, language):
    # srv_url = 'https://speech.googleapis.com/v1beta1/speech:syncrecognize'
    srv_url = 'https://speech.googleapis.com/v1beta1/speech:syncrecognize?key=AIzaSyCscYt_3d03IaijlwlVzI4gKIZsIcm3LGs'
    print("Starting Google ASR")
    audio_file = open(filepath, 'rb')
    audio_b64 = base64.b64encode(audio_file.read())
    audio_b64str = audio_b64.decode()
    audio_file.close()
    languageCode = 'cmn-Hans-CN'
    if language == 'Mandarian':
        languageCode = 'cmn-Hans-CN'
    elif language == 'Cantonese':
        languageCode = 'yue-Hant-HK'
    elif language == 'English':
        languageCode = 'en-US'
    voice = {
        "config":
            {
                # "encoding": "WAV",
                "encoding": "LINEAR16",
                "languageCode": languageCode,
            },

        "audio":
            {
                "content": audio_b64str
            }
    }
    # 将字典格式的voice编码为utf8
    voice = json.dumps(voice).encode('utf8')

    http_header = [
        'Content-Type: application/json',
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
    c.setopt(c.POSTFIELDS, voice)
    c.perform()
    string = buf.getvalue()
    print("google string"+string)
    string1 = json.loads(string)['results']
    string2 = string1[0]
    string3 = json.dumps(string2)
    string4 = json.loads(string3)["alternatives"]
    string5 = string4[0]
    string6 = json.dumps(string5)
    result = json.loads(string6)["transcript"]
    buf.close()
    return result

