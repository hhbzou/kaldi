# -*- coding: utf-8 -*-
'''
识别一长段音频，误识别性能测试；
'''
import os
import time
import logging
import contextlib
import wave
from collections import defaultdict

# 相关配置信息
# adb 工具所在绝对路径：
dic_key = {'1': 'DengHuiZaiXiang', '2': 'JieDianHua', '3': 'JiXuBoFang', '4': 'NiHaoXiaoYi', '5': 'ShangYiShou',
           '6': 'ShengYinDaYiDian', '7': 'ShengYinXiaoYiDian', '8': 'TingZhiBoFang', '9': 'HelloXiaoGua',
           '10': 'XiaYiShou', '11': 'ZanTingBoFang'}
set_id_int = [1,2,3,4,5,6,7,8,9,10,11]
set_id = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'}
others = "None"
def __matchKeyWord__(id):
    if id in set_id:
        return dic_key[id]
    return others

def Exam(f,fN,expectRes):
    '''
    :param f: 测试wav音频名称
    :param fN:测试wav音频绝对名称
    :param expectRes:
    :return:
    '''
    keyMisCount = defaultdict(int)
    cmdStr = "./tdnn_tflite " + fN
    # print(fN)
    ret = os.popen(cmdStr)
    id = "0"
    realRes = ""
    COUNT = 0
    for i in ret.readlines():
        print(i)
        if "Trigger type:" in i :
            id = i.split(":")[1].strip("\n").strip(" ")
            realRes = __matchKeyWord__(id)
            if realRes == expectRes:
                logging.info("Right\texpect:%s\treal:%s\tfile:%s"%(expectRes,realRes,f))
            else:
                logging.info("Error\texpect:%s\treal:%s" % (expectRes, realRes))
                keyMisCount[id] += 1
                COUNT += 1
                logging.info("出现%d次误识别" % (COUNT))
    print("共出现%d次误识别" % (COUNT))
    for i in set_id_int:
        id = str(i)
        print((id + ":" + dic_key[id] + "\t" +"出现%d次误识别") % (keyMisCount[id]))
        logging.info((dic_key[id] + "\t" +"出现%d次误识别") % (keyMisCount[id]))
    return -1

def CountWavTim(fn):
    with contextlib.closing(wave.open(fn, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        wav_length = frames / float(rate)
    print(wav_length)

def error_wakeup_main():
    '''准确率离线测试
    :return:
    '''
    COUNT = 0
    right = 0
    error = 0
    audio_path = "../douluodaluWAV"

    for f in os.listdir(audio_path):
        fN = os.path.join(audio_path, f)
        print(f)
        expectRes = "None"
        Exam(f=f,fN=fN,expectRes=expectRes)

def __():
    error_wakeup_main()
logDir = "../log"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
curTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
logName = 'log-' + curTime + '.txt'
logging.basicConfig(filename=os.path.join(logDir, logName), level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logging.info("Begin Offline Exam")
logging.info("1m安静场景连续pcm文件测试")
__()
# main()
# ExamSingleWav("4976090-shangyishou-m-fast-11-anhui-057.wav")

# adbPath = "D:\\Desktop\\OFFLINPCM\\adb\\adb.exe"
