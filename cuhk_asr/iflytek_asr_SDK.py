# -*- coding:utf-8 -*-
# ! /usr/bin/env python
from ctypes import *
import time
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

dll = cdll.LoadLibrary('./cuhk_asr/msc_x64.dll')
# dll = cdll.LoadLibrary("E:\\New_Project\\windowsSDK_iflytek\\bin\\msc_x64.dll")

login_params = b"appid = 5b1e2667, work_dir = ."

FRAME_LEN = 640  # Byte

MSP_SUCCESS = 0

MSP_AUDIO_SAMPLE_FIRST = 1
MSP_AUDIO_SAMPLE_CONTINUE = 2
MSP_AUDIO_SAMPLE_LAST = 4
MSP_REC_STATUS_COMPLETE = 5


# filename = "E:\\New_Project\\MyWorkspace\\AsrTest\\Upload\\new.wav"

class Msp:
    def __init__(self):
        pass

    def login(self):
        ret = dll.MSPLogin(None, None, login_params)
        # print('MSPLogin =>', ret)

    def logout(self):
        ret = dll.MSPLogout()
        # print('MSPLogout =>', ret)

    def isr(self, audiofile, session_begin_params):
        ret = c_int()
        sessionID = c_voidp()
        dll.QISRSessionBegin.restype = c_char_p
        sessionID = dll.QISRSessionBegin(None, session_begin_params, byref(ret))
        # print('QISRSessionBegin => sessionID:', sessionID, 'ret:', ret.value)

        # piceLne = FRAME_LEN * 20
        piceLne = 1638 * 2
        epStatus = c_int(0)
        recogStatus = c_int(0)

        wavFile = open(audiofile, 'rb')
        wavData = wavFile.read(piceLne)

        ret = dll.QISRAudioWrite(sessionID, wavData, len(wavData), MSP_AUDIO_SAMPLE_FIRST, byref(epStatus),
                                 byref(recogStatus))
        # print('len(wavData):', len(wavData), 'QISRAudioWrite ret:', ret, 'epStatus:', epStatus.value, 'recogStatus:',
        #       recogStatus.value)
        time.sleep(0.1)
        while wavData:
            wavData = wavFile.read(piceLne)

            if len(wavData) == 0:
                break

            ret = dll.QISRAudioWrite(sessionID, wavData, len(wavData), MSP_AUDIO_SAMPLE_CONTINUE, byref(epStatus),
                                     byref(recogStatus))
            # print('len(wavData):', len(wavData), 'QISRAudioWrite ret:', ret, 'epStatus:', epStatus.value, 'recogStatus:', recogStatus.value)
            time.sleep(0.1)
        wavFile.close()
        ret = dll.QISRAudioWrite(sessionID, None, 0, MSP_AUDIO_SAMPLE_LAST, byref(epStatus), byref(recogStatus))
        # print('len(wavData):', len(wavData), 'QISRAudioWrite ret:', ret, 'epStatus:', epStatus.value, 'recogStatus:', recogStatus.value)

        laststr = ''
        counter = 0
        while recogStatus.value != MSP_REC_STATUS_COMPLETE:
            ret = c_int()
            dll.QISRGetResult.restype = c_char_p
            retstr = dll.QISRGetResult(sessionID, byref(recogStatus), 0, byref(ret))
            if retstr is not None:
                laststr += retstr.decode()
                # print(laststr)
            # print('ret:'+ret)
            counter += 1
            time.sleep(0.1)
            counter += 1
            if counter == 300:
                laststr += 'fail'
                break

        laststr.decode('utf-8').encode('gb18030')
        ret = dll.QISRSessionEnd(sessionID, '\0')
        print('end ret: ', ret)
        return laststr


def XF_text(filepath, language):
    msp = Msp()
    msp.login()
    print("Starting iflytek ASR")
    if language == 'Cantonese':
        language = b"language = zh_cn, accent = cantonese,"
    elif language == 'English':
        language = b"language = en_us,"

    session_begin_params = b"sub = iat, domain = iat," + language + b"sample_rate = 16000, result_type = plain, result_encoding = utf8"
    text = msp.isr(filepath, session_begin_params)
    # msp.logout()
    return text
