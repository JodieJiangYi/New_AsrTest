# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from django.shortcuts import render, HttpResponse
import iflytek_asr_SDK, baidu_asr, Microsoft_asr, Google_asr, iflytek_asr_API
from models import Asr
import threading
import json
import wave
import contextlib
import Queue

queue = Queue.Queue()

def post_asr(request):
    ctx = {'errcode': "", 'filename': "", 'rlt1': "", 'rlt2': "", 'rlt3': "", 'rlt4': "", 'res_save': ""}
    language = 'Madarian'
    if request.method == 'GET':
        return render(request, 'post_asr.html')
    if request.POST:
        ctx['errcode'] = ""
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")
        f = wave.open(myFile, "rb")
        params = f.getparams()
        # 读取格式信息
        # 一次性返回所有的WAV文件的格式信息，它返回的是一个组元(tuple)：声道数, 量化位数（byte单位）, 采
        # 样频率, 采样点数, 压缩类型, 压缩类型的描述。wave模块只支持非压缩的数据，因此可以忽略最后两个信息
        nchannels, sampwidth, framerate, nframes = params[:4]
        with contextlib.closing(f) as f:
            frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        f.close()
        # print(params)

        if (nchannels == 1) and (duration <= 60) and (framerate == 16000):
            language = request.POST.get('Language')
            filepath = os.path.join("E:\\New_Project\\MyWorkspace\\New_Asrtest\\audio", myFile.name)
            print(filepath)
            ctx['filename'] = myFile.name
            destination = open(filepath, 'wb+')  # 打开特定的文件进行二进制的写操作
            for chunk in myFile.chunks():  # 分块写入文件
                destination.write(chunk)
            destination.close()

            # 开启线程组
            threads = []
            t1 = MyThread(iflytek, (filepath, language))
            threads.append(t1)
            t2 = MyThread(baidu, (filepath, language))
            threads.append(t2)
            t3 = MyThread(microsoft, (filepath, language))
            threads.append(t3)
            # t4 = MyThread(google, (filepath, language))
            # threads.append(t4)

            for t in threads:
                t.setDaemon(True)
                t.start()
            for t in threads:
                t.join()

            ctx['rlt1'] = t1.get_result()
            ctx['rlt2'] = t2.get_result()
            ctx['rlt3'] = t3.get_result()
            # ctx['rlt4'] = t4.get_result()
        else:
            ctx['errcode'] = "音频不符合条件"
            print("音频不符合条件")
        json_str = json.dumps(ctx)
        # print(json_str.encode("utf-8"))
        return HttpResponse(json_str)


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        threading.Thread.join(self)  # 等待线程执行完毕
        try:
            return self.result
        except Exception:
            return None


# def post_asr1(request):
#     # 接收POST请求数据
#     if request.POST:
#         ctx['res_save'] = ""
#         if request.POST.has_key('save'):
#             #保存音频文件名及四个相应识别结果
#             asr_model = Asr(filename=ctx['filename'], text1=ctx['rlt1'], text2=ctx['rlt2'], text3=ctx['rlt3'], text4=ctx['rlt4'])
#             asr_model.save()
#             ctx['res_save'] = "Saved successfully"
#     return render(request, "post_asr.html", ctx)


def iflytek(filepath, language):
    resiflytek = "fail"
    # print("iflytek"+language)
    if language == "Mandarian":
        # 讯飞webapi普通话识别
        resiflytek = iflytek_asr_API.recog_audio(filepath).encode("utf-8")
    if language == "Cantonese" or language == "English":
        # 讯飞SDK粤语、英语识别
        resiflytek = iflytek_asr_SDK.XF_text(filepath, language).encode("utf-8")
    print("iflytek:"+resiflytek)
    queue.put({'iflytek': resiflytek})
    return resiflytek


def baidu(filepath, language):
    # 百度API粤语识别
    token = baidu_asr.get_token()
    resbaidu = baidu_asr.use_cloud(filepath, token, language).encode("utf-8")
    print("baidu:"+resbaidu)
    queue.put({'baidu': resbaidu})
    return resbaidu


def microsoft(filepath, language):
    # Microsoft API粤语识别
    resmicro = Microsoft_asr.use_cloud(filepath, language).encode("utf-8")
    print("microsoft:"+resmicro)
    # ctx['rlt3'] = resmicro
    queue.put({'miscrosoft': resmicro})
    return resmicro


# def google(filepath, language):
#     # Google API粤语识别
#     resgoogle = Google_asr.use_cloud(filepath, language).encode("utf-8")
#     print(resgoogle)
#     # ctx['rlt4'] = resgoogle
#     queue.put({'google': resgoogle})
#     return resgoogle


# def iflytek_asr_intro(request):
#     return render(request, 'iflytek_asr.html', {})
#
#
# def baidu_asr_intro(request):
#     return render(request, 'iflytek_asr.html', {})